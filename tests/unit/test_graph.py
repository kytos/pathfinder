"""Test Graph methods."""
from unittest import TestCase
from unittest.mock import call, patch

from napps.kytos.pathfinder.graph import KytosGraph
from tests.helpers import get_topology_mock


# pylint: disable=arguments-differ, protected-access
class TestGraph(TestCase):
    """Tests for the Main class."""

    @patch('networkx.Graph')
    def setUp(self, mock_graph):
        """Execute steps before each tests."""
        self.mock_graph = mock_graph.return_value
        self.kytos_graph = KytosGraph()

    def test_clear(self):
        """Test clear."""
        self.kytos_graph.clear()

        self.mock_graph.clear.assert_called()

    @patch('napps.kytos.pathfinder.graph.KytosGraph.update_links')
    @patch('napps.kytos.pathfinder.graph.KytosGraph.update_nodes')
    def test_update_topology(self, *args):
        """Test update topology."""
        (mock_update_nodes, mock_update_links) = args
        topology = get_topology_mock()
        self.kytos_graph.update_topology(topology)

        self.mock_graph.clear.assert_called()
        mock_update_nodes.assert_called_with(topology.switches)
        mock_update_links.assert_called_with(topology.links)

    def test_update_nodes(self):
        """Test update nodes."""
        topology = get_topology_mock()
        self.kytos_graph.update_nodes(topology.switches)
        switch = topology.switches["00:00:00:00:00:00:00:01"]

        calls = [call(switch.id)]
        calls += [call(interface.id)
                  for interface in switch.interfaces.values()]
        self.mock_graph.add_node.assert_has_calls(calls)

        calls = [call(switch.id, interface.id)
                 for interface in switch.interfaces.values()]
        self.mock_graph.add_edge.assert_has_calls(calls)

    @patch('napps.kytos.pathfinder.graph.KytosGraph._set_default_metadata')
    def test_update_links(self, mock_set_default_metadata):
        """Test update nodes."""
        topology = get_topology_mock()
        self.kytos_graph.update_links(topology.links)

        keys = []
        all_metadata = [link.metadata for link in topology.links.values()]
        for metadata in all_metadata:
            keys.extend(key for key in metadata.keys())
        mock_set_default_metadata.assert_called_with(keys)

    def test_remove_switch_hops(self):
        """Test remove switch hops."""
        circuit = {"hops": ["00:00:00:00:00:00:00:01:1",
                            "00:00:00:00:00:00:00:01",
                            "00:00:00:00:00:00:00:01:2"]}

        self.kytos_graph._remove_switch_hops(circuit)

        expected_circuit = {"hops": ["00:00:00:00:00:00:00:01:1",
                                     "00:00:00:00:00:00:00:01:2"]}
        self.assertEqual(circuit, expected_circuit)

    @patch('networkx.shortest_simple_paths', return_value=["any"])
    def test_shortest_paths(self, mock_shortest_simple_paths):
        """Test shortest paths."""
        source, dest = "00:00:00:00:00:00:00:01:1", "00:00:00:00:00:00:00:02:2"
        shortest_paths = self.kytos_graph.shortest_paths(source, dest)

        mock_shortest_simple_paths.assert_called_with(self.kytos_graph.graph,
                                                      source, dest, None)
        self.assertEqual(shortest_paths, ["any"])
