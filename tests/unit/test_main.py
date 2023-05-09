"""Test Main methods."""

from unittest.mock import MagicMock, patch
from datetime import timedelta

from kytos.core.events import KytosEvent
from kytos.lib.helpers import get_controller_mock, get_test_client

# pylint: disable=import-error
from napps.kytos.pathfinder.main import Main
from tests.helpers import get_topology_mock, get_topology_with_metadata


# pylint: disable=protected-access
class TestMain:
    """Tests for the Main class."""

    def setup_method(self):
        """Execute steps before each tests."""
        self.controller = get_controller_mock()
        self.napp = Main(self.controller)
        self.api_client = get_test_client(self.controller, self.napp)
        self.endpoint = "kytos/pathfinder/v3/"

    def test_update_topology_success_case(self):
        """Test update topology method to success case."""
        topology = get_topology_mock()
        event = KytosEvent(
            name="kytos.topology.updated", content={"topology": topology}
        )
        self.napp.update_topology(event)
        assert self.napp._topology == topology

    def test_update_topology_events_out_of_order(self):
        """Test update topology events out of order.

        If a subsequent older event is sent, then the topology
        shouldn't get updated.
        """
        topology = get_topology_mock()
        assert self.napp._topology_updated_at is None
        first_event = KytosEvent(
            name="kytos.topology.updated", content={"topology": topology}
        )
        self.napp.update_topology(first_event)
        assert self.napp._topology_updated_at == first_event.timestamp
        assert self.napp._topology == topology

        second_topology = get_topology_mock()
        second_event = KytosEvent(
            name="kytos.topology.updated", content={"topology": second_topology}
        )
        second_event.timestamp = first_event.timestamp - timedelta(seconds=10)
        self.napp.update_topology(second_event)
        assert self.napp._topology == topology

    def test_update_topology_failure_case(self):
        """Test update topology method to failure case."""
        event = KytosEvent(name="kytos.topology.updated")
        self.napp.update_topology(event)
        assert not self.napp._topology

    def setting_shortest_path_mocked(self, mock_shortest_paths):
        """Set the primary elements needed to test the retrieving
        process of the shortest path under a mocked approach."""
        self.napp._topology = get_topology_mock()
        path = ["00:00:00:00:00:00:00:01:1", "00:00:00:00:00:00:00:02:1"]
        mock_shortest_paths.return_value = [path]
        return path

    async def test_shortest_path_response(self, monkeypatch, event_loop):
        """Test shortest path."""
        self.napp.controller.loop = event_loop
        cost_mocked_value = 1
        mock_path_cost = MagicMock(return_value=cost_mocked_value)
        monkeypatch.setattr("napps.kytos.pathfinder.graph."
                            "KytosGraph._path_cost", mock_path_cost)
        mock_shortest_paths = MagicMock()
        monkeypatch.setattr("napps.kytos.pathfinder.graph."
                            "KytosGraph.k_shortest_paths", mock_shortest_paths)
        path = self.setting_shortest_path_mocked(mock_shortest_paths)
        data = {
            "source": "00:00:00:00:00:00:00:01:1",
            "destination": "00:00:00:00:00:00:00:02:1",
        }
        response = await self.api_client.post(self.endpoint, json=data)
        assert response.status_code == 200
        expected_response = {
            "paths": [{"hops": path, "cost": cost_mocked_value}]
        }
        assert response.json() == expected_response

    async def test_shortest_path_response_status_code(
        self, monkeypatch, event_loop
    ):
        """Test shortest path."""
        self.napp.controller.loop = event_loop
        cost_mocked_value = 1
        mock_path_cost = MagicMock(return_value=cost_mocked_value)
        monkeypatch.setattr("napps.kytos.pathfinder.graph."
                            "KytosGraph._path_cost", mock_path_cost)
        mock_shortest_paths = MagicMock()
        monkeypatch.setattr("napps.kytos.pathfinder.graph."
                            "KytosGraph.k_shortest_paths", mock_shortest_paths)
        _ = self.setting_shortest_path_mocked(mock_shortest_paths)
        data = {
            "source": "00:00:00:00:00:00:00:01:1",
            "destination": "00:00:00:00:00:00:00:02:1",
        }
        response = await self.api_client.post(self.endpoint, json=data)
        assert response.status_code == 200

    async def setting_shortest_constrained_path_mocked(
        self, mock_constrained_k_shortest_paths
    ):
        """Set the primary elements needed to test the retrieving process
        of the shortest constrained path under a mocked approach."""
        source = "00:00:00:00:00:00:00:01:1"
        destination = "00:00:00:00:00:00:00:02:1"
        path = [source, destination]
        mandatory_metrics = {"ownership": "bob"}
        fle_metrics = {"delay": 30}
        metrics = {**mandatory_metrics, **fle_metrics}
        mock_constrained_k_shortest_paths.return_value = [
            {"hops": path, "metrics": metrics}
        ]
        data = {
            "source": "00:00:00:00:00:00:00:01:1",
            "destination": "00:00:00:00:00:00:00:02:1",
            "mandatory_metrics": {"ownership": "bob"},
            "flexible_metrics": {"delay": 30},
            "minimum_flexible_hits": 1,
        }
        response = await self.api_client.post(self.endpoint, json=data)

        return response, metrics, path

    async def test_shortest_constrained_path_response(
        self, monkeypatch, event_loop
    ):
        """Test constrained flexible paths."""
        self.napp.controller.loop = event_loop
        mock_path_cost = MagicMock(return_value=1)
        monkeypatch.setattr("napps.kytos.pathfinder.graph."
                            "KytosGraph._path_cost", mock_path_cost)
        mock_k = MagicMock()
        monkeypatch.setattr("napps.kytos.pathfinder.graph."
                            "KytosGraph.constrained_k_shortest_paths", mock_k)
        (
            response,
            metrics,
            path,
        ) = await self.setting_shortest_constrained_path_mocked(mock_k)
        expected_response = [
            {"metrics": metrics, "hops": path, "cost": 1}
        ]
        assert response.json()["paths"][0] == expected_response[0]

    async def test_shortest_constrained_path_response_status_code(
        self, monkeypatch, event_loop
    ):
        """Test constrained flexible paths."""
        self.napp.controller.loop = event_loop
        mock_path_cost = MagicMock(return_value=1)
        monkeypatch.setattr("napps.kytos.pathfinder.graph."
                            "KytosGraph._path_cost", mock_path_cost)
        mock_k = MagicMock()
        monkeypatch.setattr("napps.kytos.pathfinder.graph."
                            "KytosGraph.k_shortest_paths", mock_k)
        response, _, _ = await self.setting_shortest_constrained_path_mocked(
            mock_k
        )
        assert response.status_code == 200

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
        edges = [
            (link.endpoint_a.id, link.endpoint_b.id)
            for link in self.napp._topology.links.values()
        ]
        self.napp.graph.graph.edges = edges

        undesired = ["1"]
        non_excluded_edges = self.napp._non_excluded_edges(undesired)
        assert non_excluded_edges == [
            ("00:00:00:00:00:00:00:01:2", "00:00:00:00:00:00:00:03:1"),
            ("00:00:00:00:00:00:00:02:2", "00:00:00:00:00:00:00:03:2"),
        ]

        undesired = ["3"]
        non_excluded_edges = self.napp._non_excluded_edges(undesired)
        assert non_excluded_edges == [
            ('00:00:00:00:00:00:00:01:1', '00:00:00:00:00:00:00:02:1'),
            ("00:00:00:00:00:00:00:01:2", "00:00:00:00:00:00:00:03:1"),
        ]

        undesired = ["1", "3"]
        non_excluded_edges = self.napp._non_excluded_edges(undesired)
        assert non_excluded_edges == [
            ('00:00:00:00:00:00:00:01:2', '00:00:00:00:00:00:00:03:1'),
        ]

        undesired = ["1", "2", "3"]
        non_excluded_edges = self.napp._non_excluded_edges(undesired)
        assert not non_excluded_edges

        undesired = []
        non_excluded_edges = self.napp._non_excluded_edges(undesired)
        assert non_excluded_edges == [
            ('00:00:00:00:00:00:00:01:1', '00:00:00:00:00:00:00:02:1'),
            ("00:00:00:00:00:00:00:01:2", "00:00:00:00:00:00:00:03:1"),
            ("00:00:00:00:00:00:00:02:2", "00:00:00:00:00:00:00:03:2"),
        ]

        undesired = ["1", "2", "3"]
        self.napp._topology = None
        non_excluded_edges = self.napp._non_excluded_edges(undesired)
        assert not non_excluded_edges

    def setting_path(self):
        """Set the primary elements needed to test the topology
        update process under a "real-simulated" scenario."""
        topology = get_topology_with_metadata()
        event = KytosEvent(
            name="kytos.topology.updated", content={"topology": topology}
        )
        self.napp.update_topology(event)

    async def test_update_links_changed(self):
        """Test update_links_metadata_changed."""
        self.napp.graph.update_link_metadata = MagicMock()
        self.napp.controller.buffers.app.put = MagicMock()
        event = KytosEvent(
            name="kytos.topology.links.metadata.added",
            content={"link": MagicMock(), "metadata": {}}
        )
        self.napp.update_links_metadata_changed(event)
        assert self.napp.graph.update_link_metadata.call_count == 1
        assert self.napp.controller.buffers.app.put.call_count == 0

    async def test_update_links_changed_out_of_order(self):
        """Test update_links_metadata_changed out of order."""
        self.napp.graph.update_link_metadata = MagicMock()
        self.napp.controller.buffers.app.put = MagicMock()
        link = MagicMock(id="1")
        assert link.id not in self.napp._links_updated_at
        event = KytosEvent(
            name="kytos.topology.links.metadata.added",
            content={"link": link, "metadata": {}}
        )
        self.napp.update_links_metadata_changed(event)
        assert self.napp.graph.update_link_metadata.call_count == 1
        assert self.napp.controller.buffers.app.put.call_count == 0
        assert self.napp._links_updated_at[link.id] == event.timestamp

        second_event = KytosEvent(
            name="kytos.topology.links.metadata.added",
            content={"link": link, "metadata": {}}
        )
        second_event.timestamp = event.timestamp - timedelta(seconds=10)
        self.napp.update_links_metadata_changed(second_event)
        assert self.napp.graph.update_link_metadata.call_count == 1
        assert self.napp.controller.buffers.app.put.call_count == 0
        assert self.napp._links_updated_at[link.id] == event.timestamp

    async def test_update_links_changed_key_error(self):
        """Test update_links_metadata_changed key_error."""
        self.napp.graph.update_link_metadata = MagicMock()
        self.napp.controller.buffers.app.put = MagicMock()
        event = KytosEvent(
            name="kytos.topology.links.metadata.added",
            content={"link": MagicMock()}
        )
        self.napp.update_links_metadata_changed(event)
        assert self.napp.graph.update_link_metadata.call_count == 1
        assert self.napp.controller.buffers.app.put.call_count == 1

    async def test_shortest_path(self, event_loop):
        """Test shortest path."""
        self.napp.controller.loop = event_loop
        self.setting_path()
        source, destination = "User1", "User4"
        data = {"source": source, "destination": destination}
        response = await self.api_client.post(self.endpoint, json=data)

        for path in response.json()["paths"]:
            assert source == path["hops"][0]
            assert destination == path["hops"][-1]

    async def setting_shortest_constrained_path_exception(self, side_effect):
        """Set the primary elements needed to test the shortest
        constrained path behavior under exception actions."""
        self.setting_path()
        with patch(
            "napps.kytos.pathfinder.graph.KytosGraph."
            "constrained_k_shortest_paths",
            side_effect=side_effect,
        ):
            data = {
                "source": "00:00:00:00:00:00:00:01:1",
                "destination": "00:00:00:00:00:00:00:02:1",
                "mandatory_metrics": {"ownership": "bob"},
                "flexible_metrics": {"delay": 30},
                "minimum_flexible_hits": 1,
            }
            response = await self.api_client.post(self.endpoint, json=data)
        return response

    async def test_shortest_constrained_path_400_exception(self, event_loop):
        """Test shortest path."""
        self.napp.controller.loop = event_loop
        res = await self.setting_shortest_constrained_path_exception(TypeError)
        assert res.status_code == 400
