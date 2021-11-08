"""Test Graph methods."""
from unittest import TestCase
from unittest.mock import MagicMock, call, patch

from napps.kytos.pathfinder.graph import KytosGraph
from tests.helpers import (
    get_filter_links_fake,
    get_topology_mock,
    get_topology_with_metadata_mock,
)

# pylint: disable=arguments-differ, protected-access


class TestGraph(TestCase):
    """Tests for the Main class."""

    @patch("networkx.Graph")
    def setUp(self, mock_graph):
        """Execute steps before each tests."""
        self.mock_graph = mock_graph.return_value
        self.kytos_graph = KytosGraph()

    def test_clear(self):
        """Test clear."""
        self.kytos_graph.clear()

        self.mock_graph.clear.assert_called()

    def setting_update_topology(self, *args):
        """Set the primary elements needed to
        test the topology update process."""
        (mock_update_nodes, mock_update_links) = args
        topology = get_topology_mock()
        self.kytos_graph.update_topology(topology)

        self.mock_graph.clear.assert_called()

        return mock_update_nodes, mock_update_links, topology

    @patch("napps.kytos.pathfinder.graph.KytosGraph.update_links")
    @patch("napps.kytos.pathfinder.graph.KytosGraph.update_nodes")
    def test_update_topology_switches(self, *args):
        """Test update topology."""
        mock_update_nodes, _, topology = self.setting_update_topology(*args)
        mock_update_nodes.assert_called_with(topology.switches)

    @patch("napps.kytos.pathfinder.graph.KytosGraph.update_links")
    @patch("napps.kytos.pathfinder.graph.KytosGraph.update_nodes")
    def test_update_topology_links(self, *args):
        """Test update topology."""
        _, mock_update_links, topology = self.setting_update_topology(*args)
        mock_update_links.assert_called_with(topology.links)

    def test_update_nodes(self):
        """Test update nodes."""
        topology = get_topology_mock()
        self.kytos_graph.update_nodes(topology.switches)
        switch = topology.switches["00:00:00:00:00:00:00:01"]

        calls = [call(switch.id)]
        calls += [
            call(interface.id) for interface in switch.interfaces.values()
        ]
        self.mock_graph.add_node.assert_has_calls(calls)

        calls = [
            call(switch.id, interface.id)
            for interface in switch.interfaces.values()
        ]

        self.mock_graph.add_edge.assert_has_calls(calls)

    def test_update_nodes_2(self):
        """Test update nodes."""

        effect = MagicMock(side_effect=AttributeError)

        topology = get_topology_mock()
        with self.assertRaises(Exception):
            with patch.object(self.mock_graph, "add_node", effect):
                self.kytos_graph.update_nodes(topology.switches)

        self.assertRaises(AttributeError)

    def test_remove_switch_hops(self):
        """Test remove switch hops."""
        circuit = {
            "hops": [
                "00:00:00:00:00:00:00:01:1",
                "00:00:00:00:00:00:00:01",
                "00:00:00:00:00:00:00:01:2",
            ]
        }

        self.kytos_graph._remove_switch_hops(circuit)

        expected_circuit = {
            "hops": ["00:00:00:00:00:00:00:01:1", "00:00:00:00:00:00:00:01:2"]
        }
        self.assertEqual(circuit, expected_circuit)

    @patch("networkx.shortest_simple_paths", return_value=["any"])
    def test_shortest_paths(self, mock_shortest_simple_paths):
        """Test shortest paths."""
        source, dest = "00:00:00:00:00:00:00:01:1", "00:00:00:00:00:00:00:02:2"
        k_shortest_paths = self.kytos_graph.k_shortest_paths(source, dest)

        mock_shortest_simple_paths.assert_called_with(
            self.kytos_graph.graph, source, dest, weight=None
        )
        self.assertEqual(k_shortest_paths, ["any"])

    @patch("napps.kytos.pathfinder.graph.combinations", autospec=True)
    def test_constrained_k_shortest_paths(self, mock_combinations):
        """Test shortest constrained paths."""
        source, dest = "00:00:00:00:00:00:00:01:1", "00:00:00:00:00:00:00:02:2"
        minimum_hits = 1
        mandatory_metrics = {"bandwidth": 100}
        flexible_metrics = {"utilization": 2}
        mock_combinations.return_value = [(("utilization", 2),)]
        constrained_k_shortest_paths = [["path1"], ["path2"]]

        self.kytos_graph.graph.edge_subgraph = MagicMock(return_value=None)
        self.kytos_graph.k_shortest_paths = MagicMock(
            return_value=constrained_k_shortest_paths
        )
        self.kytos_graph._filter_links = MagicMock(
            side_effect=get_filter_links_fake
        )
        k_shortest_paths = self.kytos_graph.constrained_k_shortest_paths(
            source,
            dest,
            minimum_hits=minimum_hits,
            mandatory_metrics=mandatory_metrics,
            flexible_metrics=flexible_metrics,
        )

        self.kytos_graph.k_shortest_paths.assert_has_calls(
            [
                call(
                    source,
                    dest,
                    weight=None,
                    k=1,
                    graph=None,
                )
            ]
        )
        self.kytos_graph._filter_links.assert_called()
        for constrained_path in k_shortest_paths:
            assert constrained_path["hops"] in constrained_k_shortest_paths
            assert constrained_path["metrics"] == {
                "bandwidth": 100,
                "utilization": 2,
            }

    def test_get_link_metadata(self):
        """Test metadata retrieval."""
        topology = get_topology_with_metadata_mock()
        self.kytos_graph.update_nodes(topology.switches)
        self.kytos_graph.update_links(topology.links)
        endpoint_a = "S1:1"
        endpoint_b = "S2:1"
        metadata = {"reliability": 5, "bandwidth": 100, "delay": 105}
        self.kytos_graph.get_link_metadata = MagicMock(return_value=metadata)

        result = self.kytos_graph.get_link_metadata(endpoint_a, endpoint_b)

        assert result == metadata
