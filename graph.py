"""Module Graph of kytos/pathfinder Kytos Network Application."""

from kytos.core import log

try:
    import networkx as nx
    from networkx.exception import NodeNotFound, NetworkXNoPath
except ImportError:
    PACKAGE = 'networkx>=2.2'
    log.error(f"Package {PACKAGE} not found. Please 'pip install {PACKAGE}'")


class KytosGraph:
    """Class responsible for the graph generation."""

    def __init__(self):
        self.graph = nx.Graph()

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

        self._set_default_metadata(keys)

    def _set_default_metadata(self, keys):
        """Set metadata to all links.

        Set the value to zero for inexistent metadata in a link to make those
        irrelevant in pathfinding.
        """
        for key in keys:
            for endpoint_a, endpoint_b in self.graph.edges:
                if key not in self.graph[endpoint_a][endpoint_b]:
                    self.graph[endpoint_a][endpoint_b][key] = 0

    @staticmethod
    def _remove_switch_hops(circuit):
        """Remove switch hops from a circuit hops list."""
        for hop in circuit['hops']:
            if len(hop.split(':')) == 8:
                circuit['hops'].remove(hop)

    def shortest_paths(self, source, destination, parameter=None):
        """Calculate the shortest paths and return them."""
        try:
            paths = list(nx.shortest_simple_paths(self.graph,
                                                  source,
                                                  destination, parameter))
        except (NodeNotFound, NetworkXNoPath):
            return []
        return paths
