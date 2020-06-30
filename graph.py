"""Module Graph of kytos/pathfinder Kytos Network Application."""

from itertools import combinations

from kytos.core import log

try:
    import networkx as nx
    from networkx.exception import NodeNotFound, NetworkXNoPath
except ImportError:
    PACKAGE = 'networkx>=2.2'
    log.error(f"Package {PACKAGE} not found. Please 'pip install {PACKAGE}'")


class Filter:
    """Class responsible for removing items with disqualifying values."""

    def __init__(self, filter_type, filter_function):
        self._filter_type = filter_type
        self._filter_function = filter_function

    def run(self, value, items):
        """Filter out items. Filter chosen is picked at runtime."""
        if isinstance(value, self._filter_type):
            return filter(self._filter_function(value), items)

        raise TypeError(f"Expected type: {self._filter_type}")


class KytosGraph:
    """Class responsible for the graph generation."""

    def __init__(self):
        self.graph = nx.Graph()
        self._filter_functions = {}

        def filter_leq(metric):  # Lower values are better
            return lambda x: (lambda y: y[2].get(metric, x) <= x)

        def filter_geq(metric):  # Higher values are better
            return lambda x: (lambda y: y[2].get(metric, x) >= x)

        def filter_eeq(metric):  # Equivalence
            return lambda x: (lambda y: y[2].get(metric, x) == x)

        self._filter_functions["ownership"] = Filter(
            str, filter_eeq("ownership"))
        self._filter_functions["bandwidth"] = Filter(
            (int, float), filter_geq("bandwidth"))
        self._filter_functions["priority"] = Filter(
            (int, float), filter_geq("priority"))
        self._filter_functions["reliability"] = Filter(
            (int, float), filter_geq("reliability"))
        self._filter_functions["utilization"] = Filter(
            (int, float), filter_leq("utilization"))
        self._filter_functions["delay"] = Filter(
            (int, float), filter_leq("delay"))
        self._path_function = nx.all_shortest_paths

    def set_path_function(self, path_fun):
        """Set the shortest path function."""
        self._path_function = path_fun

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
                self.graph.add_node(node.id)

                for interface in node.interfaces.values():
                    self.graph.add_node(interface.id)
                    self.graph.add_edge(node.id, interface.id)

            except AttributeError:
                pass

    def update_links(self, links):
        """Update all links inside the graph."""
        keys = []
        for link in links.values():
            if link.is_active():
                self.graph.add_edge(link.endpoint_a.id, link.endpoint_b.id)
                for key, value in link.metadata.items():
                    keys.append(key)
                    endpoint_a = link.endpoint_a.id
                    endpoint_b = link.endpoint_b.id
                    self.graph[endpoint_a][endpoint_b][key] = value

    def get_metadata_from_link(self, endpoint_a, endpoint_b):
        """Return the metadata of a link."""
        return self.graph.edges[endpoint_a, endpoint_b]

    @staticmethod
    def _remove_switch_hops(circuit):
        """Remove switch hops from a circuit hops list."""
        for hop in circuit['hops']:
            if len(hop.split(':')) == 8:
                circuit['hops'].remove(hop)

    def shortest_paths(self, source, destination, parameter=None):
        """Calculate the shortest paths and return them."""
        try:
            paths = list(self._path_function(self.graph,
                                             source, destination, parameter))
        except (NodeNotFound, NetworkXNoPath):
            return []
        return paths

    def constrained_flexible_paths(self, source, destination,
                                   depth=None, **metrics):
        """Calculate the constrained shortest paths with flexibility."""
        base = metrics.get("base", {})
        flexible = metrics.get("flexible", {})
        # Retrive subgraph with edges that meet base requirements.
        default_edge_list = list(self._filter_edges(
            self.graph.edges(data=True), **base))
        length = len(flexible)
        if depth is None:
            depth = length
        depth = min(length, max(0, depth))
        results = []
        paths = []
        i = 0
        # Create "sub-subgraphs" from original subgraph by trimming edges
        # that fail to meet flexible requirements. Search for a shortest
        # path in each of these graphs, until at least one is found.
        while (paths == [] and i in range(0, depth+1)):
            for combo in combinations(flexible.items(), length-i):
                additional = dict(combo)
                paths = self._constrained_shortest_paths(
                    source, destination, ((u, v) for u, v, d in
                                          self._filter_edges(default_edge_list,
                                                             **additional)))
                if paths != []:
                    results.append(
                        {"paths": paths, "metrics": {**base, **additional}})
            i = i + 1
        return results

    def _constrained_shortest_paths(self, source, destination, edges):
        paths = []
        try:
            paths = list(self._path_function(self.graph.edge_subgraph(edges),
                                             source, destination))
        except NetworkXNoPath:
            pass
        except NodeNotFound:
            if source == destination:
                if source in self.graph.nodes:
                    paths = [[source]]
        return paths

    def _filter_edges(self, edges, **metrics):
        for metric, value in metrics.items():
            filter_ = self._filter_functions.get(metric, None)
            if filter_ is not None:
                try:
                    edges = filter_.run(value, edges)
                except TypeError as err:
                    raise TypeError(f"Error in {metric} filter: {err}")
        return edges
