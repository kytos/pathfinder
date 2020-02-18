"""Module Graph of kytos/pathfinder Kytos Network Application."""

import networkx as nx
from networkx.exception import NetworkXNoPath, NodeNotFound


class KytosGraph:
    """Class responsible for the graph generation."""

    def __init__(self):
        self.graph = nx.Graph()
        self._filter_fun_dict = {}
        def filterLEQ(metric):# Lower values are better
            return lambda x: (lambda y: y[2].get(metric,x) <= x)
        def filterGEQ(metric):# Higher values  are better
            return lambda x: (lambda y: y[2].get(metric,x) >= x)
        def filterEEQ(metric):# Equivalence
            return lambda x: (lambda y: y[2].get(metric,x) == x)


        self._filter_fun_dict["ownership"] = filterEEQ("ownership")
        self._filter_fun_dict["bandwidth"] = filterGEQ("bandwidth")
        self._filter_fun_dict["priority"] = filterGEQ("priority")
        self._filter_fun_dict["utilization"] = filterLEQ("utilization")
        self._filter_fun_dict["delay"] = filterLEQ("delay")
        

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

    def constrained_shortest_paths(self, source, destination, flexible=False,  **metrics):
        paths = []
        edges = self._filter_edges(**metrics)
        try:
            paths = list(nx.shortest_simple_paths(self.graph.edge_subgraph(edges),
                                                  source,
                                                  destination))
        except NetworkXNoPath:
            return []
        except NodeNotFound:
            if source == destination:
                if source in self.graph.nodes:
                    return [[source]]
        return paths

    def _filter_edges(self, **metrics):
        edges = self.graph.edges(data=True)
        for metric, value in metrics.items():
            fun0 = self._filter_fun_dict.get(metric, None)
            if fun0 != None:
                fun1 = fun0(value)
                edges = filter(fun1,edges)
        edges = ((u,v) for u,v,d in edges)
        return edges
    
    