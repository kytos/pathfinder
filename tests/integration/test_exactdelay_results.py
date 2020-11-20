from unittest import TestCase
from exactdelaypathfinder.core import ExactDelayPathfinder
import networkx as nx

class TestExactDelayResults(TestCase):
    def test_small_topology_search(self):
        """Test search function (Exact Path Algorithm) with a small-scale topology."""
        pathfinder = ExactDelayPathfinder()
        G = nx.Graph()
        
        # The following is a small-scale topology we will use to test the
        # algorithm's functionality and correctness. Modifying the nodes and edges (links)
        # of the graph (topology) will affect the outcome of the test which may result in a failure.
        nodes = ['User1', 'S2', 'S3', 'S4', 'S5', 'S6', 'User2']
        G.add_nodes_from(nodes)
        edges = [('User1', 'S2', {'delay': 10}), ('User1', 'S3', {'delay': 37}),
                ('S2', 'S4', {'delay': 24}), ('S3', 'S4', {'delay': 48}),
                ('S3', 'S6', {'delay': 96}), ('S4', 'S5', {'delay': 1}),
                ('S6', 'User2', {'delay': 84}), ('S5', 'User2', {'delay': 29})]

        G.add_edges_from(edges)

        # Create result variables and run the test search
        mock_result = []
        mock_result = pathfinder.search(G, 64, 'User1', 'User2')
        mock_first_result = mock_result[0]
        mock_expected = mock_first_result.get('total_delay') # extract first result
        # The first result should be an exact path with delay of 64
        self.assertEqual(mock_expected, 64)
