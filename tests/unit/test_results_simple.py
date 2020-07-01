"""Module to test the KytosGraph in graph.py."""
from kytos.core.link import Link

# module under test
from tests.unit.test_results import TestResults


class TestResultsSimple(TestResults):
    """Tests for the graph class.

    Tests if the paths returned have only legal edges.
    """

    def test_path1(self):
        """Tests a simple, possible path"""
        results = self.get_path_constrained("S1", "S2")
        self.assertNotEqual(results, [])

    def test_path2(self):
        """Tests a simple, impossible path"""
        results = self.get_path_constrained("S1", "S4")
        self.assertEqual(results, [])

    def test_path3(self):
        """Tests a path to self again"""
        results = self.get_path_constrained("S1", "S1")
        self.assertNotEqual(results, [])

    def test_path4(self):
        """Tests constrained path to self again"""
        results = self.get_path_constrained(
            "S5", "S5", base={"ownership": "blue"})
        for result in results:
            self.assertNotEqual([], result["paths"])
            self.assertIn(['S5'], result["paths"])

    def test_path5(self):
        """Tests constrained path to self again"""
        results = self.get_path_constrained(
            "S5", "S5", flexible={"priority": 5})
        for result in results:
            self.assertNotEqual([], result["paths"])
            self.assertIn(['S5'], result["paths"])

    @staticmethod
    def generate_topology():
        """Generates a predetermined topology"""
        switches = {}
        interfaces = {}
        links = {}

        TestResults.create_switch("S1", switches)
        TestResults.add_interfaces(2, switches["S1"], interfaces)

        TestResults.create_switch("S2", switches)
        TestResults.add_interfaces(3, switches["S2"], interfaces)

        TestResults.create_switch("S3", switches)
        TestResults.add_interfaces(2, switches["S3"], interfaces)

        TestResults.create_switch("S4", switches)
        TestResults.add_interfaces(2, switches["S4"], interfaces)

        TestResults.create_switch("S5", switches)

        links["S1:1<->S2:1"] = Link(interfaces["S1:1"], interfaces["S2:1"])
        links["S1:1<->S2:1"].extend_metadata(
            {"bandwidth": 50, "ownership": "red"})

        links["S3:1<->S2:2"] = Link(interfaces["S3:1"], interfaces["S2:2"])
        links["S3:1<->S2:2"].extend_metadata(
            {"bandwidth": 51, "ownership": "blue"})

        links["S1:2<->S3:2"] = Link(interfaces["S1:2"], interfaces["S3:2"])
        links["S1:2<->S3:2"].extend_metadata(
            {"bandwidth": 49, "ownership": "blue"})

        return (switches, links)
