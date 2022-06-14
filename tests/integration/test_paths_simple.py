"""Module to test the KytosGraph in graph.py."""
from kytos.core.link import Link

# module under test
# pylint: disable=import-error
from tests.integration.test_paths import TestPaths


class TestPathsSimple(TestPaths):
    """Tests for the graph class.

    Tests if the paths returned have only legal edges.
    """

    def test_path_s1_s2(self):
        """Tests a simple, possible path"""
        self.initializer()

        source = "S1"
        destination = "S2"
        results = self.graph.constrained_k_shortest_paths("S1", "S2")

        assert results
        for result in results:
            path = result["hops"]
            assert source == path[0]
            assert destination == path[-1]

    def test_path_s1_s4(self):
        """Tests a simple, impossible path"""
        self.initializer()

        assert not self.graph.constrained_k_shortest_paths("S1", "S4")

    def test_path_to_self(self):
        """Tests a path to self again"""
        self.initializer()
        results = self.graph.constrained_k_shortest_paths("S1", "S1")

        assert results
        for result in results:
            path = result["hops"]
            assert path[0] == "S1"
            assert path[-1] == "S1"

    def test_path_s1_s3_constrained_red(self):
        """Tests path from s1 to s3 constrained ownership red"""
        self.initializer()

        source = "S1"
        destination = "S3"
        results = self.graph.constrained_k_shortest_paths(
            source, destination, mandatory_metrics={"ownership": "red"}
        )
        assert not results

    def test_path_s1_s3_constrained_blue(self):
        """Tests path from s1 to s3 constrained ownership blue"""
        self.initializer()

        source = "S1"
        destination = "S3"
        results = self.graph.constrained_k_shortest_paths(
            source, destination, mandatory_metrics={"ownership": "blue"}
        )
        assert results

        for result in results:
            path = result["hops"]
            assert source == path[0]
            assert destination == path[-1]

    def test_path_s1_s3_constrained_bandwidth(self):
        """Tests path from s1 to s3 constrained bandwdith, the best path
        is supposed to be via s2"""

        self.initializer()

        source = "S1"
        destination = "S3"
        results = self.graph.constrained_k_shortest_paths(
            source, destination, mandatory_metrics={"bandwidth": 50}
        )

        assert results

        for result in results:
            path = result["hops"]
            assert source == path[0]
            assert "S2" in path
            assert destination == path[-1]

    @staticmethod
    def generate_topology():
        """Generates a predetermined topology. Topology 1"""
        switches = {}
        interfaces = {}
        links = {}

        TestPaths.create_switch("S1", switches)
        TestPaths.add_interfaces(2, switches["S1"], interfaces)

        TestPaths.create_switch("S2", switches)
        TestPaths.add_interfaces(3, switches["S2"], interfaces)

        TestPaths.create_switch("S3", switches)
        TestPaths.add_interfaces(2, switches["S3"], interfaces)

        TestPaths.create_switch("S4", switches)
        TestPaths.add_interfaces(2, switches["S4"], interfaces)

        TestPaths.create_switch("S5", switches)

        links["S1:1<->S2:1"] = Link(interfaces["S1:1"], interfaces["S2:1"])
        links["S1:1<->S2:1"].extend_metadata(
            {"bandwidth": 50, "ownership": "red"}
        )

        links["S3:1<->S2:2"] = Link(interfaces["S3:1"], interfaces["S2:2"])
        links["S3:1<->S2:2"].extend_metadata(
            {"bandwidth": 51, "ownership": "blue"}
        )

        links["S1:2<->S3:2"] = Link(interfaces["S1:2"], interfaces["S3:2"])
        links["S1:2<->S3:2"].extend_metadata(
            {"bandwidth": 49, "ownership": "blue"}
        )

        for link in links.values():
            link.enable()
            link.activate()

        return switches, links
