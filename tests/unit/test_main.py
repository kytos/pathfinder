"""Test Main methods."""
from unittest import TestCase
from unittest.mock import MagicMock, patch

from kytos.core.events import KytosEvent
from kytos.lib.helpers import get_controller_mock, get_test_client

from napps.kytos.pathfinder.main import Main
from tests.helpers import get_topology_mock


# pylint: disable=protected-access
class TestMain(TestCase):
    """Tests for the Main class."""

    def setUp(self):
        """Execute steps before each tests."""
        self.napp = Main(get_controller_mock())

    @patch('napps.kytos.pathfinder.graph.KytosGraph.update_topology')
    def test_update_topology(self, mock_update_topology):
        """Test update topology."""
        event = KytosEvent(name='kytos.topology.updated')
        self.napp.update_topology(event)
        self.assertIsNone(self.napp._topology)

        topology = get_topology_mock()
        event = KytosEvent(name='kytos.topology.updated',
                           content={'topology': topology})
        self.napp.update_topology(event)
        self.assertEqual(self.napp._topology, topology)
        mock_update_topology.assert_called_with(topology)

    @patch('napps.kytos.pathfinder.main.Main._filter_paths')
    @patch('napps.kytos.pathfinder.graph.KytosGraph.shortest_paths')
    def test_shortest_path(self, *args):
        """Test shortest path."""
        (mock_shortest_paths, mock_filter_paths) = args

        path = ["00:00:00:00:00:00:00:01:1", "00:00:00:00:00:00:00:01",
                "00:00:00:00:00:00:00:01:2"]
        mock_shortest_paths.return_value = path
        mock_filter_paths.return_value = {}

        api = get_test_client(self.napp.controller, self.napp)
        url = "http://127.0.0.1:8181/api/kytos/pathfinder/v2"
        data = {"source": "00:00:00:00:00:00:00:01:1",
                "destination": "00:00:00:00:00:00:00:01:2",
                "desired_links": ["1"],
                "undesired_links": ["2"],
                "parameter": "custom_weight"}
        response = api.open(url, method='POST', json=data)

        hops = [{'hops': addr} for addr in path]
        mock_filter_paths.assert_called_with(hops, data["desired_links"],
                                             data["undesired_links"])
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
