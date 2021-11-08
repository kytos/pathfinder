"""Test Main methods."""

from unittest import TestCase
from unittest.mock import patch

from kytos.core.events import KytosEvent
from kytos.lib.helpers import get_controller_mock, get_test_client

from napps.kytos.pathfinder.main import Main
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
        event = KytosEvent(
            name="kytos.topology.updated", content={"topology": topology}
        )
        self.napp.update_topology(event)

        self.assertEqual(self.napp._topology, topology)

    def test_update_topology_failure_case(self):
        """Test update topology method to failure case."""
        event = KytosEvent(name="kytos.topology.updated")
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

    @patch("napps.kytos.pathfinder.graph.KytosGraph._path_cost")
    @patch("napps.kytos.pathfinder.graph.KytosGraph.k_shortest_paths")
    def test_shortest_path_response(self, mock_shortest_paths, path_cost):
        """Test shortest path."""
        cost_mocked_value = 1
        path_cost.return_value = cost_mocked_value
        api, path = self.setting_shortest_path_mocked(mock_shortest_paths)
        url = "http://127.0.0.1:8181/api/kytos/pathfinder/v2"
        data = {
            "source": "00:00:00:00:00:00:00:01:1",
            "destination": "00:00:00:00:00:00:00:02:1",
            "desired_links": ["1"],
            "undesired_links": None,
        }
        response = api.open(url, method="POST", json=data)

        expected_response = {
            "paths": [{"hops": path, "cost": cost_mocked_value}]
        }
        self.assertEqual(response.json, expected_response)

    @patch("napps.kytos.pathfinder.graph.KytosGraph._path_cost")
    @patch("napps.kytos.pathfinder.graph.KytosGraph.k_shortest_paths")
    def test_shortest_path_response_status_code(
        self, mock_shortest_paths, path_cost
    ):
        """Test shortest path."""
        path_cost.return_value = 1
        api, _ = self.setting_shortest_path_mocked(mock_shortest_paths)
        url = "http://127.0.0.1:8181/api/kytos/pathfinder/v2"
        data = {
            "source": "00:00:00:00:00:00:00:01:1",
            "destination": "00:00:00:00:00:00:00:02:1",
            "desired_links": ["1"],
            "undesired_links": None,
        }
        response = api.open(url, method="POST", json=data)

        self.assertEqual(response.status_code, 200)

    def setting_shortest_constrained_path_mocked(
        self, mock_constrained_k_shortest_paths
    ):
        """Set the primary elements needed to test the retrieving process
        of the shortest constrained path under a mocked approach."""
        source = "00:00:00:00:00:00:00:01:1"
        destination = "00:00:00:00:00:00:00:02:1"
        path = [source, destination]
        base_metrics = {"ownership": "bob"}
        fle_metrics = {"delay": 30}
        metrics = {**base_metrics, **fle_metrics}
        mock_constrained_k_shortest_paths.return_value = [
            {"hops": [path], "metrics": metrics}
        ]

        api = get_test_client(self.napp.controller, self.napp)
        url = "http://127.0.0.1:8181/api/kytos/pathfinder/v2/"
        data = {
            "source": "00:00:00:00:00:00:00:01:1",
            "destination": "00:00:00:00:00:00:00:02:1",
            "base_metrics": {"ownership": "bob"},
            "flexible_metrics": {"delay": 30},
            "minimum_flexible_hits": 1,
        }
        response = api.open(url, method="POST", json=data)

        return response, metrics, path

    @patch("napps.kytos.pathfinder.graph.KytosGraph._path_cost")
    @patch(
        "napps.kytos.pathfinder.graph.KytosGraph.constrained_k_shortest_paths",
        autospec=True,
    )
    def test_shortest_constrained_path_response(
        self, mock_constrained_k_shortest_paths, path_cost
    ):
        """Test constrained flexible paths."""
        cost_mocked_value = 1
        path_cost.return_value = cost_mocked_value
        (
            response,
            metrics,
            path,
        ) = self.setting_shortest_constrained_path_mocked(
            mock_constrained_k_shortest_paths
        )
        expected_response = [
            {"metrics": metrics, "hops": [path], "cost": cost_mocked_value}
        ]

        self.assertDictEqual(response.json["paths"][0], expected_response[0])

    @patch("napps.kytos.pathfinder.graph.KytosGraph._path_cost")
    @patch(
        "napps.kytos.pathfinder.graph.KytosGraph.constrained_k_shortest_paths",
        autospec=True,
    )
    def test_shortest_constrained_path_response_status_code(
        self, mock_constrained_k_shortest_paths, path_cost
    ):
        """Test constrained flexible paths."""
        path_cost.return_value = 1
        response, _, _ = self.setting_shortest_constrained_path_mocked(
            mock_constrained_k_shortest_paths
        )

        self.assertEqual(response.status_code, 200)

    def test_filter_paths_response_on_desired(self):
        """Test filter paths."""
        self.napp._topology = get_topology_mock()
        paths = [
            {
                "hops": [
                    "00:00:00:00:00:00:00:01:1",
                    "00:00:00:00:00:00:00:02:1",
                ]
            }
        ]
        desired, undesired = ["1"], None

        filtered_paths = self.napp._filter_paths(paths, desired, undesired)
        self.assertEqual(filtered_paths, paths)

    def test_filter_paths_le_cost_response(self):
        """Test filter paths."""
        self.napp._topology = get_topology_mock()
        paths = [
            {
                "hops": [
                    "00:00:00:00:00:00:00:01:1",
                    "00:00:00:00:00:00:00:01",
                    "00:00:00:00:00:00:00:02:1",
                    "00:00:00:00:00:00:00:02",
                    "00:00:00:00:00:00:00:02:2",
                    "00:00:00:00:00:00:00:04",
                    "00:00:00:00:00:00:00:04:1",
                ],
                "cost": 6,
            },
            {
                "hops": [
                    "00:00:00:00:00:00:00:01:1",
                    "00:00:00:00:00:00:00:01",
                    "00:00:00:00:00:00:00:04",
                    "00:00:00:00:00:00:00:04:1",
                ],
                "cost": 3,
            },
        ]
        filtered_paths = self.napp._filter_paths_le_cost(paths, 3)
        assert len(filtered_paths) == 1
        assert filtered_paths[0]["cost"] == 3

    def test_filter_paths_response_on_undesired(self):
        """Test filter paths."""
        self.napp._topology = get_topology_mock()
        paths = [
            {
                "hops": [
                    "00:00:00:00:00:00:00:01:2",
                    "00:00:00:00:00:00:00:03:1",
                ]
            }
        ]
        desired, undesired = None, ["2"]
        filtered_paths = self.napp._filter_paths(paths, desired, undesired)
        self.assertEqual(filtered_paths, [])

    def setting_path(self):
        """Set the primary elements needed to test the topology
        update process under a "real-simulated" scenario."""
        topology = get_topology_with_metadata()
        event = KytosEvent(
            name="kytos.topology.updated", content={"topology": topology}
        )
        self.napp.update_topology(event)

    def test_shortest_path(self):
        """Test shortest path."""
        self.setting_path()

        api = get_test_client(self.napp.controller, self.napp)
        url = "http://127.0.0.1:8181/api/kytos/pathfinder/v2/"

        source, destination = "User1", "User4"
        data = {"source": source, "destination": destination}

        response = api.open(url, method="POST", json=data)

        for path in response.json["paths"]:
            assert source == path["hops"][0]
            assert destination == path["hops"][-1]

    def setting_shortest_constrained_path_exception(self, side_effect):
        """Set the primary elements needed to test the shortest
        constrained path behavior under exception actions."""
        self.setting_path()
        api = get_test_client(self.napp.controller, self.napp)

        with patch(
            "napps.kytos.pathfinder.graph.KytosGraph."
            "constrained_k_shortest_paths",
            side_effect=side_effect,
        ):
            url = "http://127.0.0.1:8181/api/kytos/pathfinder/v2/"

            data = {
                "source": "00:00:00:00:00:00:00:01:1",
                "destination": "00:00:00:00:00:00:00:02:1",
                "base_metrics": {"ownership": "bob"},
                "flexible_metrics": {"delay": 30},
                "minimum_flexible_hits": 1,
            }

            response = api.open(url, method="POST", json=data)

        return response

    def test_shortest_constrained_path_400_exception(self):
        """Test shortest path."""
        response = self.setting_shortest_constrained_path_exception(TypeError)

        self.assertEqual(response.status_code, 400)
