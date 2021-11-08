"""Main module of kytos/pathfinder Kytos Network Application."""

from threading import Lock

from flask import jsonify, request
from kytos.core import KytosNApp, log, rest
from kytos.core.helpers import listen_to
from napps.kytos.pathfinder.graph import KytosGraph
# pylint: disable=import-error,no-self-use
from werkzeug.exceptions import BadRequest


class Main(KytosNApp):
    """
    Main class of kytos/pathfinder NApp.

    This class is the entry point for this napp.
    """

    def setup(self):
        """Create a graph to handle the nodes and edges."""
        self.graph = KytosGraph()
        self._topology = None
        self._lock = Lock()

    def execute(self):
        """Do nothing."""

    def shutdown(self):
        """Shutdown the napp."""

    def _filter_paths(self, paths, desired, undesired):
        """
        Apply filters to the paths list.

        Make sure that each path in the list has all the desired links and none
        of the undesired ones.
        """
        filtered_paths = []

        if desired:
            for link_id in desired:
                try:
                    endpoint_a = self._topology.links[link_id].endpoint_a.id
                    endpoint_b = self._topology.links[link_id].endpoint_b.id
                except KeyError:
                    return []

                for path in paths:
                    head = path["hops"][:-1]
                    tail = path["hops"][1:]
                    if ((endpoint_a, endpoint_b) in zip(head, tail)) or (
                        (endpoint_b, endpoint_a) in zip(head, tail)
                    ):
                        filtered_paths.append(path)
        else:
            filtered_paths = paths

        if undesired:
            for link_id in undesired:
                try:
                    endpoint_a = self._topology.links[link_id].endpoint_a.id
                    endpoint_b = self._topology.links[link_id].endpoint_b.id
                except KeyError:
                    continue

                for path in paths:
                    head = path["hops"][:-1]
                    tail = path["hops"][1:]
                    if ((endpoint_a, endpoint_b) in zip(head, tail)) or (
                        (endpoint_b, endpoint_a) in zip(head, tail)
                    ):

                        filtered_paths.remove(path)

        return filtered_paths

    def _filter_paths_le_cost(self, paths, max_cost):
        """Filter by paths where the cost is le <= max_cost."""
        if not max_cost:
            return paths
        return [path for path in paths if path["cost"] <= max_cost]

    def _validate_payload(self, data):
        """Validate shortest_path v2/ POST endpoint."""
        if data.get("desired_links"):
            if not isinstance(data["desired_links"], list):
                raise BadRequest(
                    f"TypeError: desired_links is supposed to be a list."
                    f" type: {type(data['desired_links'])}"
                )

        if data.get("undesired_links"):
            if not isinstance(data["undesired_links"], list):
                raise BadRequest(
                    f"TypeError: undesired_links is supposed to be a list."
                    f" type: {type(data['undesired_links'])}"
                )

        parameter = data.get("parameter")
        spf_attr = data.get("spf_attribute")
        if not spf_attr:
            spf_attr = parameter or "hop"
        data["spf_attribute"] = spf_attr

        if spf_attr not in self.graph.spf_edge_data_cbs:
            raise BadRequest(
                "Invalid 'spf_attribute'. Valid values: "
                f"{', '.join(self.graph.spf_edge_data_cbs.keys())}"
            )

        try:
            data["spf_max_paths"] = max(int(data.get("spf_max_paths", 2)), 1)
        except (TypeError, ValueError):
            raise BadRequest(
                f"spf_max_paths {data.get('spf_max_pahts')} must be an int"
            )

        spf_max_path_cost = data.get("spf_max_path_cost")
        if spf_max_path_cost:
            try:
                spf_max_path_cost = max(int(spf_max_path_cost), 1)
                data["spf_max_path_cost"] = spf_max_path_cost
            except (TypeError, ValueError):
                raise BadRequest(
                    f"spf_max_path_cost {data.get('spf_max_path_cost')} must"
                    " be an int"
                )

        data["mandatory_metrics"] = data.get("mandatory_metrics", {})
        data["flexible_metrics"] = data.get("flexible_metrics", {})

        try:
            minimum_hits = data.get("minimum_flexible_hits")
            if minimum_hits:
                minimum_hits = min(
                    len(data["flexible_metrics"]), max(0, int(minimum_hits))
                )
            data["minimum_flexible_hits"] = minimum_hits
        except (TypeError, ValueError):
            raise BadRequest(
                f"minimum_hits {data.get('minimum_flexible_hits')} must"
                " be an int"
            )

        return data

    @rest("v2/", methods=["POST"])
    def shortest_path(self):
        """Calculate the best path between the source and destination."""
        data = request.get_json()
        data = self._validate_payload(data)

        desired = data.get("desired_links")
        undesired = data.get("undesired_links")

        spf_attr = data.get("spf_attribute")
        spf_max_paths = data.get("spf_max_paths")
        spf_max_path_cost = data.get("spf_max_path_cost")
        mandatory_metrics = data.get("mandatory_metrics")
        flexible_metrics = data.get("flexible_metrics")
        minimum_hits = data.get("minimum_flexible_hits")
        log.debug(f"POST v2/ payload data: {data}")

        try:
            with self._lock:
                if any([mandatory_metrics, flexible_metrics]):
                    paths = self.graph.constrained_k_shortest_paths(
                        data["source"],
                        data["destination"],
                        weight=self.graph.spf_edge_data_cbs[spf_attr],
                        k=spf_max_paths,
                        minimum_hits=minimum_hits,
                        mandatory_metrics=mandatory_metrics,
                        flexible_metrics=flexible_metrics,
                    )
                else:
                    paths = self.graph.k_shortest_paths(
                        data["source"],
                        data["destination"],
                        weight=self.graph.spf_edge_data_cbs[spf_attr],
                        k=spf_max_paths,
                    )

                paths = self.graph.path_cost_builder(
                    paths,
                    weight=spf_attr,
                )
            log.debug(f"Found paths: {paths}")
        except TypeError as err:
            raise BadRequest(str(err))

        paths = self._filter_paths(paths, desired, undesired)
        paths = self._filter_paths_le_cost(paths, max_cost=spf_max_path_cost)
        log.debug(f"Filtered paths: {paths}")
        return jsonify({"paths": paths})

    @listen_to("kytos.topology.updated")
    def update_topology(self, event):
        """Update the graph when the network topology is updated."""
        if "topology" not in event.content:
            return
        topology = event.content["topology"]
        with self._lock:
            self._topology = topology
            self.graph.update_topology(topology)
        log.debug("Topology graph updated.")
