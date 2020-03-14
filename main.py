"""Main module of kytos/pathfinder Kytos Network Application."""

from flask import jsonify, request
from kytos.core import KytosNApp, log, rest
from kytos.core.helpers import listen_to

# pylint: disable=import-error
from napps.kytos.pathfinder.graph import KytosGraph

# pylint: enable=import-error


class Main(KytosNApp):
    """Main class of kytos/pathfinder NApp.

    This class is the entry point for this napp.
    """

    def setup(self):
        """Create a graph to handle the nodes and edges."""
        self.graph = KytosGraph()
        self._topology = None

    def execute(self):
        """Do nothing."""

    def shutdown(self):
        """Shutdown the napp."""

    def _filter_paths(self, paths, desired, undesired):
        """Apply filters to the paths list.

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
                    head = path['hops'][:-1]
                    tail = path['hops'][1:]
                    if (((endpoint_a, endpoint_b) in zip(head, tail)) or
                            ((endpoint_b, endpoint_a) in zip(head, tail))):
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
                    head = path['hops'][:-1]
                    tail = path['hops'][1:]
                    if (((endpoint_a, endpoint_b) in zip(head, tail)) or
                            ((endpoint_b, endpoint_a) in zip(head, tail))):

                        filtered_paths.remove(path)

        return filtered_paths

    @rest('v2/', methods=['POST'])
    def shortest_path(self):
        """Calculate the best path between the source and destination."""
        data = request.get_json()

        desired = data.get('desired_links')
        undesired = data.get('undesired_links')
        parameter = data.get('parameter')

        paths = []
        for path in self.graph.shortest_paths(data['source'],
                                              data['destination'],
                                              parameter):

            paths.append({'hops': path})

        paths = self._filter_paths(paths, desired, undesired)
        return jsonify({'paths': paths})

    @rest('v3/', methods=['POST'])
    def shortest_constrained_path(self):
        """Get the set of shortest paths between the source and destination."""
        data = request.get_json()

        source = data.get('source')
        destination = data.get('destination')
        flexible = data.get('flexible', False)
        metrics = data.get('metrics',{})

        paths = self.graph.shortest_paths(source, destination,
                                              parameter)

        paths = self._filter_paths(paths, desired, undesired)
        return jsonify({'paths': paths})

    @listen_to('kytos.topology.updated')
    def update_topology(self, event):
        """Update the graph when the network topology was updated.

        Clear the current graph and create a new with the most topoly updated.
        """
        if 'topology' not in event.content:
            return
        topology = event.content['topology']
        self._topology = topology
        self.graph.update_topology(topology)
        log.debug('Topology graph updated.')
