"""Module to test the KytosGraph in graph.py."""
from itertools import combinations

from tests.integration.edges_settings import EdgesSettings


class TestPathsEdges(EdgesSettings):
    """TestPathsEdges."""

    def test_k_shortest_paths_among_users(self):
        """Tests paths between all users using unconstrained path algorithm."""
        combos = combinations(["User1", "User2", "User3", "User4"], 2)
        self.initializer()

        for source, destination in combos:
            paths = self.graph.k_shortest_paths(source, destination)
            assert paths
            for path in paths:
                assert path[0] == source
                assert path[-1] == destination

    def test_constrained_k_shortest_paths_among_users(self):
        """Tests paths between all users using constrained path algorithm,
        with no constraints set.
        """
        combos = combinations(["User1", "User2", "User3", "User4"], 2)
        self.initializer()

        for source, destination in combos:
            paths = self.graph.constrained_k_shortest_paths(
                source, destination
            )
            assert paths
            for path in paths:
                assert path["hops"][0] == source
                assert path["hops"][-1] == destination

    def test_cspf_delay_spf_attribute_between_u1_u4(self):
        self.initializer()
        source = "User1"
        destination = "User4"
        spf_attribute = "delay"
        paths = self.graph.constrained_k_shortest_paths(
            source, destination, weight=spf_attribute
        )
        assert paths
        for path in paths:
            assert path["hops"][0] == source
            assert path["hops"][-1] == destination
        paths = self.graph._path_cost_builder(paths, weight=spf_attribute)
        assert paths[0]["cost"] == 105 + 1 + 1

    def test_cspf_reliability_between_u1_u2(self):
        self.initializer()
        source = "User1"
        destination = "User2"
        paths = self.graph.constrained_k_shortest_paths(
            source, destination, mandatory_metrics={"reliability": 10}
        )
        assert not paths

        paths = self.graph.constrained_k_shortest_paths(
            source, destination, mandatory_metrics={"reliability": 3}
        )
        assert paths

        for path in paths:
            assert path["hops"][0] == source
            assert path["hops"][-1] == destination
            assert path["metrics"] == {"reliability": 3}
        paths = self.graph._path_cost_builder(paths)
        assert paths[0]["cost"] == 12

    def test_cspf_bandwidth_between_u1_u4(self):
        self.initializer()
        source = "User1"
        destination = "User4"
        spf_attribute = "delay"
        paths = self.graph.constrained_k_shortest_paths(
            source,
            destination,
            weight=spf_attribute,
            mandatory_metrics={"bandwidth": 200},
        )
        assert not paths

        paths = self.graph.constrained_k_shortest_paths(
            source,
            destination,
            weight=spf_attribute,
            mandatory_metrics={"bandwidth": 100},
        )
        assert paths

        for path in paths:
            assert path["hops"][0] == source
            assert path["hops"][-1] == destination
            assert path["metrics"] == {"bandwidth": 100}
        paths = self.graph._path_cost_builder(paths, weight=spf_attribute)
        assert paths[0]["cost"] == 122

    def test_cspf_delay_between_u2_u3(self):
        self.initializer()
        source = "User2"
        destination = "User3"

        paths = self.graph.constrained_k_shortest_paths(
            source, destination, mandatory_metrics={"delay": 1}
        )
        assert not paths

        paths = self.graph.constrained_k_shortest_paths(
            source, destination, mandatory_metrics={"delay": 50}
        )
        assert paths
        for path in paths:
            assert path["hops"][0] == source
            assert path["hops"][-1] == destination
        paths = self.graph._path_cost_builder(paths)
        assert paths[0]["cost"] >= 3

    def test_cspf_ownership_between_s4_s6(self):
        self.initializer()
        source = "S6:2"
        destination = "S4:2"

        paths = self.graph.constrained_k_shortest_paths(
            source, destination, mandatory_metrics={"ownership": "B"}
        )
        assert not paths

        paths = self.graph.constrained_k_shortest_paths(
            source, destination, mandatory_metrics={"ownership": "A"}
        )
        assert paths
        for path in paths:
            assert path["hops"][0] == source
            assert path["hops"][-1] == destination
        paths = self.graph._path_cost_builder(paths)
        assert paths[0]["cost"] >= 3

    def test_cspf_flexible_between_s4_s6(self):
        self.initializer()
        source = "S6:2"
        destination = "S4:2"

        paths = self.graph.constrained_k_shortest_paths(
            source,
            destination,
            mandatory_metrics={"reliability": 2},
            flexible_metrics={"bandwidth": 60},
            minimium_hits=1,
        )
        assert paths
        for path in paths:
            assert path["hops"][0] == source
            assert path["hops"][-1] == destination
        paths = self.graph._path_cost_builder(paths)
        assert paths[0]["cost"] >= 3

    def test_cspf_paths_mandatory_with_flexible(self):
        """Tests paths between all users using constrained path algorithm,
        with the delay constraint set to 50, the bandwidth constraint
        set to 100, the reliability constraint set to 3, and the ownership
        constraint set to 'B'

        Tests conducted with all but ownership flexible
        """
        combos = combinations(["User1", "User2", "User3", "User4"], 2)
        self.initializer()

        for source, destination in combos:
            paths = self.graph.constrained_k_shortest_paths(
                source,
                destination,
                mandatory_metrics={"ownership": "B"},
                flexible_metrics={
                    "delay": 50,
                    "bandwidth": 100,
                    "reliability": 3,
                },
            )
            for path in paths:
                # delay = 50 checks
                if "delay" in path["metrics"]:
                    self.assertNotIn("S1:1", path["hops"])
                    self.assertNotIn("S2:1", path["hops"])
                    self.assertNotIn("S3:1", path["hops"])
                    self.assertNotIn("S5:1", path["hops"])
                    self.assertNotIn("S4:2", path["hops"])
                    self.assertNotIn("User1:2", path["hops"])
                    self.assertNotIn("S5:5", path["hops"])
                    self.assertNotIn("S8:2", path["hops"])
                    self.assertNotIn("S5:6", path["hops"])
                    self.assertNotIn("User1:3", path["hops"])
                    self.assertNotIn("S6:3", path["hops"])
                    self.assertNotIn("S9:1", path["hops"])
                    self.assertNotIn("S6:4", path["hops"])
                    self.assertNotIn("S9:2", path["hops"])
                    self.assertNotIn("S6:5", path["hops"])
                    self.assertNotIn("S10:1", path["hops"])
                    self.assertNotIn("S8:5", path["hops"])
                    self.assertNotIn("S9:4", path["hops"])
                    self.assertNotIn("User1:4", path["hops"])
                    self.assertNotIn("User4:3", path["hops"])

                # bandwidth = 100 checks
                if "bandwidth" in path["metrics"]:
                    self.assertNotIn("S3:1", path["hops"])
                    self.assertNotIn("S5:1", path["hops"])
                    self.assertNotIn("User1:4", path["hops"])
                    self.assertNotIn("User4:3", path["hops"])

                # reliability = 3 checks
                if "reliability" in path["metrics"]:
                    self.assertNotIn("S4:1", path["hops"])
                    self.assertNotIn("S5:2", path["hops"])
                    self.assertNotIn("S5:3", path["hops"])
                    self.assertNotIn("S6:1", path["hops"])

                # ownership = "B" checks
                self.assertIn("ownership", path["metrics"])
                self.assertNotIn("S4:1", path["hops"])
                self.assertNotIn("S5:2", path["hops"])
                self.assertNotIn("S4:2", path["hops"])
                self.assertNotIn("User1:2", path["hops"])
                self.assertNotIn("S5:4", path["hops"])
                self.assertNotIn("S6:2", path["hops"])
                self.assertNotIn("S6:5", path["hops"])
                self.assertNotIn("S10:1", path["hops"])
                self.assertNotIn("S8:6", path["hops"])
                self.assertNotIn("S10:2", path["hops"])
                self.assertNotIn("S10:3", path["hops"])
                self.assertNotIn("User2:1", path["hops"])

    def test_ownership_type_error(self):
        """Tests that TypeError."""
        self.initializer()

        with self.assertRaises(TypeError):
            self.graph.constrained_k_shortest_paths(
                "User1", "User2", mandatory_metrics={"ownership": 1}
            )
