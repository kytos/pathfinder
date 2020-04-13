"""Module Graph of kytos/pathfinder Kytos Network Application."""

from kytos.core import log

try:
    import networkx as nx
    from networkx.exception import NodeNotFound, NetworkXNoPath
except ImportError:
    PACKAGE = 'networkx>=2.2'
    log.error(f"Package {PACKAGE} not found. Please 'pip install {PACKAGE}'")

from itertools import combinations

class Filter:
    def __init__(self, filter_type, filter_function):
        self._filter_type = filter_type
        self._filter_fun = filter_function

    def run(self,value, items):
        if isinstance(value, self._filter_type):
            fun0 = self._filter_fun(value)
            return filter(fun0, items)
        else:
            raise TypeError(f"Expected type: {self._filter_type}")



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


        self._filter_fun_dict["ownership"] = Filter(str,filterEEQ("ownership"))
        self._filter_fun_dict["bandwidth"] = Filter((int,float),filterGEQ("bandwidth"))
        self._filter_fun_dict["priority"] = Filter((int,float),filterGEQ("priority"))
        self._filter_fun_dict["reliability"] = Filter((int,float),filterGEQ("reliability"))
        self._filter_fun_dict["utilization"] = Filter((int,float),filterLEQ("utilization"))
        self._filter_fun_dict["delay"] = Filter((int,float),filterLEQ("delay"))
        self._path_fun = nx.all_shortest_paths
        

    def set_path_fun(self, path_fun):
        self._path_fun = path_fun

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
            paths = list(self._path_fun(self.graph,
                                        source, destination, parameter))
        except (NodeNotFound, NetworkXNoPath):
            return []
        return paths

    def constrained_flexible_paths(self, source, destination, metrics, flexible_metrics, flexible = None):
        default_edge_list = self.graph.edges(data=True)
        default_edge_list = self._filter_edges(default_edge_list,**metrics)
        length = len(flexible_metrics)
        if flexible is None:
            flexible = length
        flexible = max(0,flexible)
        flexible = min(length,flexible)
        results = []
        stop = False
        for i in range(0,flexible+1):
            if stop:
                break
            y = combinations(flexible_metrics.items(),length-i)
            for x in y:
                tempDict = {}
                for k,v in x:
                    tempDict[k] = v
                edges = self._filter_edges(default_edge_list,**tempDict)
                edges = ((u,v) for u,v,d in edges)
                res0 = self._constrained_shortest_paths(source,destination,edges)
                if res0 != []:
                    results.append({"paths":res0, "metrics":{**metrics, **tempDict}})
                    stop = True
        return results

    def _constrained_shortest_paths(self, source, destination, edges):
        paths = []
        try:
            paths = list(self._path_fun(self.graph.edge_subgraph(edges),
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
            fil = self._filter_fun_dict.get(metric, None)
            if fil != None:
                try:
                    edges = fil.run(value,edges)
                except TypeError as err:
                    raise TypeError(f"Error in {metric} filter: {err}")
        return edges
