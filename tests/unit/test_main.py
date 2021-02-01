"""Test Main methods."""

from unittest import TestCase
from unittest.mock import patch

from kytos.core.events import KytosEvent
from kytos.lib.helpers import get_controller_mock, get_test_client

# from napps.kytos.pathfinder.main import Main
from main import Main
from tests.helpers import get_topology_mock, get_topology_with_metadata


# pylint: disable=protected-access
class TestMain(TestCase):
    """Tests for the Main class."""

    def setUp(self):
        """Execute steps before each tests."""
        self.napp = Main(get_controller_mock())

    def test_update_topology_success_case(self):
        """Test update topology method to success case."""
        topology = get_topology_mock()
        event = KytosEvent(name='kytos.topology.updated',
                           content={'topology': topology})
        self.napp.update_topology(event)

        self.assertEqual(self.napp._topology, topology)

    def test_update_topology_failure_case(self):
        """Test update topology method to failure case."""
        event = KytosEvent(name='kytos.topology.updated')
        self.napp.update_topology(event)

        self.assertIsNone(self.napp._topology)

    @patch('napps.kytos.pathfinder.graph.KytosGraph.shortest_paths')
    def test_shortest_path(self, mock_shortest_paths):
        """Test shortest path."""
        self.napp._topology = get_topology_mock()
        path = ["00:00:00:00:00:00:00:01:1", "00:00:00:00:00:00:00:02:1"]
        mock_shortest_paths.return_value = [path]

        api = get_test_client(self.napp.controller, self.napp)
        url = "http://127.0.0.1:8181/api/kytos/pathfinder/v2"
        data = {"source": "00:00:00:00:00:00:00:01:1",
                "destination": "00:00:00:00:00:00:00:02:1",
                "desired_links": ["1"],
                "undesired_links": None}
        response = api.open(url, method='POST', json=data)

        expected_response = {'paths': [{'hops': path}]}
        self.assertEqual(response.json, expected_response)
        self.assertEqual(response.status_code, 200)

    @patch('napps.kytos.pathfinder.graph.KytosGraph.' +
           'constrained_flexible_paths', autospec=True)
    def test_shortest_constrained_path(self, mock_constrained_flexible_paths):
        """Test constrained flexible paths."""
        source = "00:00:00:00:00:00:00:01:1"
        destination = "00:00:00:00:00:00:00:02:1"
        path = [source, destination]
        base_metrics = {"ownership": "bob"}
        fle_metrics = {"delay": 30}
        metrics = {**base_metrics, **fle_metrics}
        mock_constrained_flexible_paths.return_value = [
            {"paths": [path], "metrics": metrics}]

        api = get_test_client(self.napp.controller, self.napp)
        url = "http://127.0.0.1:8181/api/kytos/pathfinder/v2/" +\
            "best-constrained-paths"
        data = {"source": "00:00:00:00:00:00:00:01:1",
                "destination": "00:00:00:00:00:00:00:02:1",
                "base_metrics": {"ownership": "bob"},
                "flexible_metrics": {"delay": 30},
                "minimum_flexible_hits": 1}
        response = api.open(url, method='POST', json=data)
        expected_response = [{"metrics": metrics, "paths": [path]}]

        self.assertEqual(response.json, expected_response)
        self.assertEqual(response.status_code, 200)

    def test_filter_paths(self):
        """Test filter paths."""
        self.napp._topology = get_topology_mock()
        paths = [{"hops": ["00:00:00:00:00:00:00:01:1",
                           "00:00:00:00:00:00:00:02:1"]}]
        desired, undesired = ["1"], None

        filtered_paths = self.napp._filter_paths(paths, desired, undesired)
        self.assertEqual(filtered_paths, paths)

        paths = [{"hops": ["00:00:00:00:00:00:00:01:2",
                           "00:00:00:00:00:00:00:03:1"]}]
        desired, undesired = None, ["2"]
        filtered_paths = self.napp._filter_paths(paths, desired, undesired)
        self.assertEqual(filtered_paths, [])
