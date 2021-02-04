"""Module to test the Pathfinder algorithm
performance with some constrains."""

from unittest import TestCase
from exactdelaypathfinder.core import ExactDelayPathfinder
import networkx as nx


class TestExactDelayResults(TestCase):
    """Tests for the Exact Delay result constrain."""

    def setUp(self):
        self.pathfinder = ExactDelayPathfinder()
        self.G = nx.Graph()

    def test_edpf_can_show_best_path_first(self):
        """Test search function to see if the first result is the best one."""

        # The following is a small-scale topology we will use to test the
        # algorithm's functionality and correctness. Modifying the nodes and edges (links)
        # of the graph (topology) will affect the outcome of the test which may result in a failure.
        nodes = ['User1', 'S2', 'S3', 'S4', 'S5', 'S6', 'User2']
        self.G.add_nodes_from(nodes)
        edges = [('User1', 'S2', {'delay': 10}), ('User1', 'S3', {'delay': 37}),
                 ('S2', 'S4', {'delay': 24}), ('S3', 'S4', {'delay': 48}),
                 ('S3', 'S6', {'delay': 96}), ('S4', 'S5', {'delay': 1}),
                 ('S6', 'User2', {'delay': 84}), ('S5', 'User2', {'delay': 29})]

        self.G.add_edges_from(edges)

        # Create result variables and run the test search
        result = []
        result = self.pathfinder.search(self.G, 64, 'User1', 'User2')
        first_result = result[0]
        actual = first_result.get('total_delay')  # extract first result

        # The first result should be an exact path with delay of 64
        self.assertEqual(64, actual)

    def test_edpf_can_show_empty_result(self):
        """Test search function to see if it can return an empty result."""

        edges = [('User1', 'S2', {'delay': 10}), ('User1', 'S3', {'delay': 37}),
                 ('S2', 'S4', {'delay': 24}), ('S3', 'S4', {'delay': 48}),
                 ('S3', 'S6', {'delay': 96}), ('S4', 'S5', {'delay': 1}),
                 ('S6', 'User2', {'delay': 84}), ('S5', 'User2', {'delay': 29})]

        self.G.add_edges_from(edges)

        # Create isolated node. This node is not connected to another node.
        isolated_nodes = ['S7']
        self.G.add_nodes_from(isolated_nodes)

        result = []

        # Find path to the unreachable node - impossible
        result = self.pathfinder.search(self.G, 64, 'User1', 'S7')
        self.assertEqual([], result)
