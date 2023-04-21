"""Main module of kytos/pathfinder Kytos Network Application."""

from threading import Lock
from typing import Generator

from kytos.core import KytosEvent, KytosNApp, log, rest
from kytos.core.helpers import listen_to
from kytos.core.rest_api import (HTTPException, JSONResponse, Request,
                                 get_json_or_400)
from napps.kytos.pathfinder.graph import KytosGraph


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
        self._topology_updated_at = None
        self._links_updated_at = {}

    def execute(self):
        """Do nothing."""

    def shutdown(self):
        """Shutdown the napp."""

    def _filter_paths_le_cost(self, paths, max_cost):
        """Filter by paths where the cost is le <= max_cost."""
        if not max_cost:
            return paths
        return [path for path in paths if path["cost"] <= max_cost]

    def _map_endpoints_from_link_ids(self, link_ids: list[str]) -> dict:
        """Map endpoints from link ids."""
        endpoints = {}
        for link_id in link_ids:
            try:
                link = self._topology.links[link_id]
                endpoint_a, endpoint_b = link.endpoint_a, link.endpoint_b
                endpoints[(endpoint_a.id, endpoint_b.id)] = link
            except KeyError:
                pass
        return endpoints

    def _find_all_link_ids(
        self, paths: list[dict], link_ids: list[str]
    ) -> Generator[int, None, None]:
        """Find indexes of the paths that contain all link ids."""
        endpoints_links = self._map_endpoints_from_link_ids(link_ids)
        if not endpoints_links:
            return None
        endpoint_keys = set(endpoints_links.keys())
        for idx, path in enumerate(paths):
            head, tail, found_endpoints = path["hops"][:-1], path["hops"][1:], set()
            for endpoint_a, endpoint_b in zip(head, tail):
                if (endpoint_a, endpoint_b) in endpoints_links:
                    found_endpoints.add((endpoint_a, endpoint_b))
                if (endpoint_b, endpoint_a) in endpoints_links:
                    found_endpoints.add((endpoint_b, endpoint_a))
            if found_endpoints == endpoint_keys:
                yield idx
        return None

    def _find_any_link_ids(
        self, paths: list[dict], link_ids: list[str]
    ) -> Generator[int, None, None]:
        """Find indexes of the paths that contain any of the link ids."""
        endpoints_links = self._map_endpoints_from_link_ids(link_ids)
        if not endpoints_links:
            return None
        for idx, path in enumerate(paths):
            head, tail, found = path["hops"][:-1], path["hops"][1:], False
            for endpoint_a, endpoint_b in zip(head, tail):
                if any(
                    (
                        (endpoint_a, endpoint_b) in endpoints_links,
                        (endpoint_b, endpoint_a) in endpoints_links,
                    )
                ):
                    found = True
                    break
            if found:
                yield idx
        return None

    def _filter_paths_undesired_links(
        self, paths: list[dict], undesired: list[str]
    ) -> list[dict]:
        """Filter by undesired_links, it performs a logical OR."""
        if not undesired:
            return paths
        excluded_indexes = set(self._find_any_link_ids(paths, undesired))
        return [path for idx, path in enumerate(paths) if idx not in excluded_indexes]

    def _filter_paths_desired_links(
        self, paths: list[dict], desired: list[str]
    ) -> list[dict]:
        """Filter by desired_links, it performs a logical AND."""
        if not desired:
            return paths
        included_indexes = set(self._find_all_link_ids(paths, desired))
        return [path for idx, path in enumerate(paths) if idx in included_indexes]

    def _validate_payload(self, data):
        """Validate shortest_path v2/ POST endpoint."""
        if data.get("desired_links"):
            if not isinstance(data["desired_links"], list):
                raise HTTPException(
                    400,
                    f"TypeError: desired_links is supposed to be a list."
                    f" type: {type(data['desired_links'])}"
                )

        if data.get("undesired_links"):
            if not isinstance(data["undesired_links"], list):
                raise HTTPException(
                    400,
                    f"TypeError: undesired_links is supposed to be a list."
                    f" type: {type(data['undesired_links'])}"
                )

        parameter = data.get("parameter")
        spf_attr = data.get("spf_attribute")
        if not spf_attr:
            spf_attr = parameter or "hop"
        data["spf_attribute"] = spf_attr

        if spf_attr not in self.graph.spf_edge_data_cbs:
            raise HTTPException(
                400,
                "Invalid 'spf_attribute'. Valid values: "
                f"{', '.join(self.graph.spf_edge_data_cbs.keys())}"
            )

        try:
            data["spf_max_paths"] = max(int(data.get("spf_max_paths", 2)), 1)
        except (TypeError, ValueError):
            raise HTTPException(
                400,
                f"spf_max_paths {data.get('spf_max_pahts')} must be an int"
            )

        spf_max_path_cost = data.get("spf_max_path_cost")
        if spf_max_path_cost:
            try:
                spf_max_path_cost = max(int(spf_max_path_cost), 1)
                data["spf_max_path_cost"] = spf_max_path_cost
            except (TypeError, ValueError):
                raise HTTPException(
                    400,
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
            raise HTTPException(
                400,
                f"minimum_hits {data.get('minimum_flexible_hits')} must be an int"
            )

        return data

    @rest("v2/", methods=["POST"])
    def shortest_path(self, request: Request) -> JSONResponse:
        """Calculate the best path between the source and destination."""
        data = get_json_or_400(request)
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
            raise HTTPException(400, str(err))

        paths = self._filter_paths_le_cost(paths, max_cost=spf_max_path_cost)
        paths = self._filter_paths_undesired_links(paths, undesired)
        paths = self._filter_paths_desired_links(paths, desired)
        log.debug(f"Filtered paths: {paths}")
        return JSONResponse({"paths": paths})

    @listen_to(
        "kytos.topology.updated",
        "kytos/topology.current",
        "kytos/topology.topology_loaded",
    )
    def on_topology_updated(self, event):
        """Update the graph when the network topology is updated."""
        self.update_topology(event)

    def update_topology(self, event):
        """Update the graph when the network topology is updated."""
        if "topology" not in event.content:
            return
        topology = event.content["topology"]
        with self._lock:
            if (
                self._topology_updated_at
                and self._topology_updated_at > event.timestamp
            ):
                return
            self._topology = topology
            self._topology_updated_at = event.timestamp
            self.graph.update_topology(topology)
        switches = list(topology.switches.keys())
        links = list(topology.links.keys())
        log.debug(f"Topology graph updated with switches: {switches}, links: {links}.")

    def update_links_metadata_changed(self, event) -> None:
        """Update the graph when links' metadata are added or removed."""
        link = event.content["link"]
        try:
            with self._lock:
                if (
                    link.id in self._links_updated_at
                    and self._links_updated_at[link.id] > event.timestamp
                ):
                    return
                self.graph.update_link_metadata(link)
                self._links_updated_at[link.id] = event.timestamp
            metadata = event.content["metadata"]
            log.debug(f"Topology graph updated link id: {link.id} metadata: {metadata}")
        except KeyError as exc:
            log.warning(
                f"Unexpected KeyError {str(exc)} on event {event}."
                " pathfinder will reconciliate the topology"
            )
            self.controller.buffers.app.put(KytosEvent(name="kytos/topology.get"))

    @listen_to("kytos/topology.links.metadata.(added|removed)")
    def on_links_metadata_changed(self, event):
        """Update the graph when links' metadata are added or removed."""
        self.update_links_metadata_changed(event)
