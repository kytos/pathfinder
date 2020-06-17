"""Module to test the KytosGraph in graph.py."""
# Core modules to import
from kytos.core.link import Link

# module under test
from tests.unit.test_search_results import TestSearchResults


class TestSearchResults1(TestSearchResults):
    """Tests for the graph class."""

    def test_path1(self):
        """Tests a simple, definetly possible path"""
        self.setup()
        results = self.get_path("S1", "S2")
        self.assertNotEqual(results, [])

    def test_constrained_path1(self):
        """Tests a simple, definetly possible path"""
        self.setup()
        results = self.get_path_constrained("S1", "S2")
        self.assertNotEqual(results, [])

    def test_path2(self):
        """Tests a simple, impossible path"""
        self.setup()
        results = self.get_path("S1", "S4")
        self.assertEqual(results, [])

    def test_constrained_path2(self):
        """Tests a simple, impossible path"""
        self.setup()
        results = self.get_path_constrained("S1", "S4")
        self.assertEqual(results, [])

    def test_path3(self):
        """Tests a path to self"""
        self.setup()
        results = self.get_path("S4", "S4")
        self.assertNotEqual(results, [])

    def test_constrained_path3(self):
        """Tests a path to self"""
        self.setup()
        results = self.get_path_constrained("S4", "S4")
        self.assertNotEqual(results, [])

    def test_path4(self):
        """Tests a path to self again"""
        self.setup()
        results = self.get_path("S1", "S1")
        self.assertNotEqual(results, [])

    def test_constrained_path4(self):
        """Tests a path to self again"""
        self.setup()
        results = self.get_path_constrained("S1", "S1")
        self.assertNotEqual(results, [])

    def test_constrained_path5(self):
        """Tests constrained path"""
        self.setup()
        results = self.get_path_constrained("S1", "S3", 0, bandwidth=50)
        for result in results:
            self.assertNotIn(['S1', 'S1:2', 'S3:2', 'S3'], result["paths"])

    def test_constrained_path6(self):
        """Tests constrained path"""
        self.setup()
        results = self.get_path_constrained("S1", "S2", 0, ownership="red")
        for result in results:
            self.assertNotIn(['S1', 'S1:2', 'S3:2', 'S3',
                              'S3:1', 'S2:2', 'S2'], result["paths"])

    def test_constrained_path7(self):
        """Tests constrained path"""
        self.setup()
        results = self.get_path_constrained("S1", "S2", 0, ownership="blue")
        for result in results:
            self.assertNotIn(['S1', 'S1:1', 'S2:1', 'S2'], result["paths"])

    def test_constrained_path8(self):
        """Tests constrained path, to self AGAIN"""
        self.setup()
        results = self.get_path_constrained("S5", "S5", 0, ownership="blue")
        for result in results:
            self.assertNotEqual([], result["paths"])
            self.assertIn(['S5'], result["paths"])

    def test_constrained_path9(self):
        """Tests constrained path"""
        self.setup()
        results = self.get_path_constrained("S1", "S2", 1, ownership="blue")
        for result in results:
            self.assertNotIn(['S1', 'S1:1', 'S2:1', 'S2'], result["paths"])

    @staticmethod
    def generate_topology():
        """Generates a predetermined topology"""
        switches = {}
        interfaces = {}
        links = {}

        TestSearchResults.create_switch("S1", switches)
        TestSearchResults.add_interfaces(2, switches["S1"], interfaces)

        TestSearchResults.create_switch("S2", switches)
        TestSearchResults.add_interfaces(3, switches["S2"], interfaces)

        TestSearchResults.create_switch("S3", switches)
        TestSearchResults.add_interfaces(2, switches["S3"], interfaces)

        TestSearchResults.create_switch("S4", switches)
        TestSearchResults.add_interfaces(2, switches["S4"], interfaces)

        TestSearchResults.create_switch("S5", switches)

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
