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

    def setting_shortest_path_mocked(self, mock_shortest_paths):
        """Set the primary elements needed to test the retrieving
        process of the shortest path under a mocked approach."""
        self.napp._topology = get_topology_mock()
        path = ["00:00:00:00:00:00:00:01:1", "00:00:00:00:00:00:00:02:1"]
        mock_shortest_paths.return_value = [path]

        api = get_test_client(self.napp.controller, self.napp)

        return api, path

    @patch('graph.KytosGraph.shortest_paths')
    def test_shortest_path_path_response(self, mock_shortest_paths):
        """Test shortest path."""
        api, path = self.setting_shortest_path_mocked(mock_shortest_paths)
        url = "http://127.0.0.1:8181/api/kytos/pathfinder/v2"
        data = {"source": "00:00:00:00:00:00:00:01:1",
                "destination": "00:00:00:00:00:00:00:02:1",
                "desired_links": ["1"],
                "undesired_links": None}
        response = api.open(url, method='POST', json=data)

        expected_response = {'paths': [{'hops': path}]}
        self.assertEqual(response.json, expected_response)

    @patch('graph.KytosGraph.shortest_paths')
    def test_shortest_path_response_status_code(self, mock_shortest_paths):
        """Test shortest path."""
        api, _ = self.setting_shortest_path_mocked(mock_shortest_paths)
        url = "http://127.0.0.1:8181/api/kytos/pathfinder/v2"
        data = {"source": "00:00:00:00:00:00:00:01:1",
                "destination": "00:00:00:00:00:00:00:02:1",
                "desired_links": ["1"],
                "undesired_links": None}
        response = api.open(url, method='POST', json=data)

        self.assertEqual(response.status_code, 200)

    def setting_shortest_constrained_path_mocked(self, mock_constrained_flexible_paths):
        """Set the primary elements needed to test the retrieving process
        of the shortest constrained path under a mocked approach."""
        source = "00:00:00:00:00:00:00:01:1"
        destination = "00:00:00:00:00:00:00:02:1"
        path = [source, destination]
        base_metrics = {"ownership": "bob"}
        fle_metrics = {"delay": 30}
        metrics = {**base_metrics, **fle_metrics}
        mock_constrained_flexible_paths.return_value = [
            {"paths": [path], "metrics": metrics}]

        api = get_test_client(self.napp.controller, self.napp)
        url = "http://127.0.0.1:8181/api/kytos/pathfinder/v2/" + \
              "best-constrained-paths"
        data = {"source": "00:00:00:00:00:00:00:01:1",
                "destination": "00:00:00:00:00:00:00:02:1",
                "base_metrics": {"ownership": "bob"},
                "flexible_metrics": {"delay": 30},
                "minimum_flexible_hits": 1}
        response = api.open(url, method='POST', json=data)

        return response, metrics, path

    @patch('graph.KytosGraph.constrained_flexible_paths', autospec=True)
    def test_shortest_constrained_path_response(self, mock_constrained_flexible_paths):
        """Test constrained flexible paths."""
        response, metrics, path = \
            self.setting_shortest_constrained_path_mocked(
                mock_constrained_flexible_paths)
        expected_response = [{"metrics": metrics, "paths": [path]}]

        self.assertEqual(response.json, expected_response)

    # @patch('napps.kytos.pathfinder.graph.KytosGraph.' +
    #        'constrained_flexible_paths', autospec=True)
    @patch('graph.KytosGraph.constrained_flexible_paths', autospec=True)
    def test_shortest_constrained_path_response_status_code(self, mock_constrained_flexible_paths):
        """Test constrained flexible paths."""
        response, _, _ = \
            self.setting_shortest_constrained_path_mocked(
                mock_constrained_flexible_paths)

        self.assertEqual(response.status_code, 200)

    def test_filter_paths_response_on_desired(self):
        """Test filter paths."""
        self.napp._topology = get_topology_mock()
        paths = [{"hops": ["00:00:00:00:00:00:00:01:1",
                           "00:00:00:00:00:00:00:02:1"]}]
        desired, undesired = ["1"], None

        filtered_paths = self.napp._filter_paths(paths, desired, undesired)
        self.assertEqual(filtered_paths, paths)

    def test_filter_paths_response_on_undesired(self):
        """Test filter paths."""
        self.napp._topology = get_topology_mock()
        paths = [{"hops": ["00:00:00:00:00:00:00:01:2",
                           "00:00:00:00:00:00:00:03:1"]}]
        desired, undesired = None, ["2"]
        filtered_paths = self.napp._filter_paths(paths, desired, undesired)
        self.assertEqual(filtered_paths, [])

    def setting_path(self):
        """Set the primary elements needed to test the topology
        update process under a "real-simulated" scenario."""
        topology = get_topology_with_metadata()
        event = KytosEvent(name='kytos.topology.updated',
                           content={'topology': topology})
        self.napp.update_topology(event)

    def test_shortest_path(self):
        """Test shortest path."""
        self.setting_path()

        api = get_test_client(self.napp.controller, self.napp)
        url = "http://127.0.0.1:8181/api/kytos/pathfinder/v2/" + \
              "path-exact-delay"

        data = {"source": "User1",
                "destination": "User4",
                "delay": 30}

        response = api.open(url, method='POST', json=data)
        paths = [{"path": ["User1", "User1:4", "User4:3", "User4"],
                  "total_delay": 105},
                 {"path": ["User1", "User1:1", "S1:2", "S1", "S1:1",
                           "S2:1", "S2", "S2:2", "User4:1", "User4"],
                  "total_delay": 116}]

        self.assertEqual(paths, response.json['Exact Path Result'])

    def setting_shortest_path_exception(self):
        """Set the primary elements needed to test the
        shortest path behavior under exception actions."""
        api = get_test_client(self.napp.controller, self.napp)
        url = "http://127.0.0.1:8181/api/kytos/pathfinder/v2/" + \
              "path-exact-delay"

        data = {"source": "User1",
                "destination": "User4",
                "delay": 30}

        return api, url, data

    def test_shortest_path_broader_exception(self):
        """Test shortest path."""
        api, url, data = self.setting_shortest_path_exception()
        with patch('graph.KytosGraph.exact_path', side_effect=Exception):
            response = api.open(url, method='POST', json=data)

        self.assertIsNotNone(response.json.get('exception'))

    def test_shortest_path_specific_exception(self):
        """Test shortest path."""
        api, url, data = self.setting_shortest_path_exception()

        with patch('graph.KytosGraph.exact_path', side_effect=TypeError):
            response = api.open(url, method='POST', json=data)

        self.assertIsNotNone(response.json.get('exception'))

    def setting_shortest_constrained_path_exception(self, side_effect):
        """Set the primary elements needed to test the shortest
        constrained path behavior under exception actions."""
        self.setting_path()
        api = get_test_client(self.napp.controller, self.napp)

        with patch('graph.KytosGraph.constrained_flexible_paths', side_effect=side_effect):
            url = "http://127.0.0.1:8181/api/kytos/pathfinder/v2/" + \
                  "best-constrained-paths"

            data = {"source": "00:00:00:00:00:00:00:01:1",
                    "destination": "00:00:00:00:00:00:00:02:1",
                    "base_metrics": {"ownership": "bob"},
                    "flexible_metrics": {"delay": 30},
                    "minimum_flexible_hits": 1}

            response = api.open(url, method='POST', json=data)

        return response

    def test_shortest_constrained_path_400_exception(self):
        """Test shortest path."""
        response = self.setting_shortest_constrained_path_exception(TypeError)

        self.assertEqual(response.status_code, 400)

    def test_shortest_constrained_path_500_exception(self):
        """Test shortest path."""
        response = self.setting_shortest_constrained_path_exception(Exception)

        self.assertEqual(response.status_code, 500)
