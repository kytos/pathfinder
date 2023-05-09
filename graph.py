"""Module Graph of kytos/pathfinder Kytos Network Application."""

# pylint: disable=too-many-arguments,too-many-locals
from itertools import combinations, islice

from kytos.core import log
from kytos.core.common import EntityStatus
from napps.kytos.pathfinder.utils import (filter_ge, filter_in, filter_le,
                                          lazy_filter, nx_edge_data_delay,
                                          nx_edge_data_priority,
                                          nx_edge_data_weight)

try:
    import networkx as nx
    from networkx.exception import NetworkXNoPath, NodeNotFound
except ImportError:
    PACKAGE = "networkx==2.5.1"
    log.error(f"Package {PACKAGE} not found. Please 'pip install {PACKAGE}'")


class KytosGraph:
    """Class responsible for the graph generation."""

    def __init__(self):
        self.graph = nx.Graph()
        self._filter_functions = {
            "ownership": lazy_filter(str, filter_in("ownership")),
            "bandwidth": lazy_filter((int, float), filter_ge("bandwidth")),
            "reliability": lazy_filter((int, float), filter_ge("reliability")),
            "priority": lazy_filter((int, float), filter_le("priority")),
            "utilization": lazy_filter((int, float), filter_le("utilization")),
            "delay": lazy_filter((int, float), filter_le("delay")),
        }
        self.spf_edge_data_cbs = {
            "hop": nx_edge_data_weight,
            "delay": nx_edge_data_delay,
            "priority": nx_edge_data_priority,
        }

    def clear(self):
        """Remove all nodes and links registered."""
        self.graph.clear()

    def update_topology(self, topology):
        """Update all nodes and links inside the graph."""
        self.graph.clear()
        self.update_nodes(topology.switches)
        self.update_links(topology.links)

    def update_nodes(self, nodes):
        """Update all nodes inside the graph."""
        for node in nodes.values():
            try:
                if node.status != EntityStatus.UP:
                    continue
                self.graph.add_node(node.id)

                for interface in node.interfaces.values():
                    if interface.status == EntityStatus.UP:
                        self.graph.add_node(interface.id)
                        self.graph.add_edge(node.id, interface.id)

            except AttributeError as err:
                raise TypeError(
                    f"Error when updating nodes inside the graph: {str(err)}"
                )

    def update_links(self, links):
        """Update all links inside the graph."""
        for link in links.values():
            if link.status == EntityStatus.UP:
                self.graph.add_edge(link.endpoint_a.id, link.endpoint_b.id)
                self.update_link_metadata(link)

    def update_link_metadata(self, link):
        """Update link metadata."""
        for key, value in link.metadata.items():
            if key not in self._filter_functions:
                continue
            endpoint_a = link.endpoint_a.id
            endpoint_b = link.endpoint_b.id
            self.graph[endpoint_a][endpoint_b][key] = value

    def get_link_metadata(self, endpoint_a, endpoint_b):
        """Return the metadata of a link."""
        return self.graph.get_edge_data(endpoint_a, endpoint_b)

    @staticmethod
    def _remove_switch_hops(circuit):
        """Remove switch hops from a circuit hops list."""
        for hop in circuit["hops"]:
            if len(hop.split(":")) == 8:
                circuit["hops"].remove(hop)

    def _path_cost(self, path, weight="hop", default_cost=1):
        """Compute the path cost given an attribute."""
        cost = 0
        for node, nbr in nx.utils.pairwise(path):
            cost += self.graph[node][nbr].get(weight, default_cost)
        return cost

    def path_cost_builder(self, paths, weight="hop", default_weight=1):
        """Build the cost of a path given a list of paths."""
        paths_acc = []
        for path in paths:
            if isinstance(path, list):
                paths_acc.append(
                    {
                        "hops": path,
                        "cost": self._path_cost(
                            path, weight=weight, default_cost=default_weight
                        ),
                    }
                )
            elif isinstance(path, dict):
                path["cost"] = self._path_cost(
                    path["hops"], weight=weight, default_cost=default_weight
                )
                paths_acc.append(path)
            else:
                raise TypeError(
                    f"type: '{type(path)}' must be be either list or dict. "
                    f"path: {path}"
                )
        return paths_acc

    def k_shortest_paths(
        self, source, destination, weight=None, k=1, graph=None
    ):
        """
        Compute up to k shortest paths and return them.

        This procedure is based on algorithm by Jin Y. Yen [1].
        Since Yen's algorithm calls Dijkstra's up to k times, the time
        complexity will be proportional to K * Dijkstra's, average
        O(K(|V| + |E|)logV), assuming it's using a heap, where V is the
        number of vertices and E number of egdes.

        References
        ----------
        .. [1] Jin Y. Yen, "Finding the K Shortest Loopless Paths in a
           Network", Management Science, Vol. 17, No. 11, Theory Series
           (Jul., 1971), pp. 712-716.
        """
        try:
            return list(
                islice(
                    nx.shortest_simple_paths(
                        graph or self.graph,
                        source,
                        destination,
                        weight=weight,
                    ),
                    k,
                )
            )
        except (NodeNotFound, NetworkXNoPath):
            return []

    def constrained_k_shortest_paths(
        self,
        source,
        destination,
        weight=None,
        k=1,
        graph=None,
        minimum_hits=None,
        **metrics,
    ):
        """Calculate the constrained shortest paths with flexibility."""
        graph = graph or self.graph
        mandatory_metrics = metrics.get("mandatory_metrics", {})
        flexible_metrics = metrics.get("flexible_metrics", {})
        first_pass_links = list(
            self._filter_links(
                graph.edges(data=True), **mandatory_metrics
            )
        )
        length = len(flexible_metrics)
        if minimum_hits is None:
            minimum_hits = 0
        minimum_hits = min(length, max(0, minimum_hits))

        paths = []
        for i in range(length, minimum_hits - 1, -1):
            for combo in combinations(flexible_metrics.items(), i):
                additional = dict(combo)
                filtered_links = self._filter_links(
                    first_pass_links, **additional
                )
                filtered_links = ((u, v) for u, v, d in filtered_links)
                for path in self.k_shortest_paths(
                    source,
                    destination,
                    weight=weight,
                    k=k,
                    graph=graph.edge_subgraph(filtered_links),
                ):
                    paths.append(
                        {
                            "hops": path,
                            "metrics": {**mandatory_metrics, **additional},
                        }
                    )
                if len(paths) == k:
                    return paths
            if paths:
                return paths
        return paths

    def _filter_links(self, links, **metrics):
        for metric, value in metrics.items():
            filter_func = self._filter_functions.get(metric, None)
            if filter_func is not None:
                try:
                    links = filter_func(value, links)
                except TypeError as err:
                    raise TypeError(
                        f"Error in {metric} value: {value} err: {err}"
                    )
        return links
