"""Module to test the KytosGraph in graph.py."""

# module under test
from tests.unit.test_results import TestResults


class TestResultsMetadata(TestResults):
    """Tests for the graph class."""

    def test_path1(self):
        """Tests to see if the edges used in the paths of the result set
        do not have poor reliability"""

        self.test_setup()
        reliabilities = []
        requirements = {"reliability": 3}
        poor_reliability = 1

        result = self.get_path_constrained("User1", "User2", base=requirements)

        if result:
            for path in result[0]["paths"]:
                for i in range(1, len(path)):
                    endpoint_a = path[i - 1]
                    endpoint_b = path[i]
                    meta_data = self.graph.get_metadata_from_link(
                        endpoint_a, endpoint_b)
                    if meta_data and "reliability" in meta_data.keys():
                        reliabilities.append(meta_data["reliability"])

        self.assertNotIn(poor_reliability, reliabilities)

    def test_path2(self):
        """Tests to see if the edges used in the paths from User 1 to User 2
        have less than 30 delay."""

        self.test_setup()
        delays = []
        requirements = {"delay": 29}

        result = self.get_path_constrained(
            "User1", "User2", base=requirements)

        if result:
            for path in result[0]["paths"]:
                for i in range(1, len(path)):
                    endpoint_a = path[i - 1]
                    endpoint_b = path[i]
                    meta_data = self.graph.get_metadata_from_link(
                        endpoint_a, endpoint_b)
                    if meta_data and "delay" in meta_data.keys():
                        delays.append(meta_data["delay"])

        for delay in delays:
            self.assertEqual(delay > requirements["delay"], False)

    def test_path3(self):
        """Tests to see if the edges used in the paths from User 1 to User 2
        have at least 20 bandwidth."""

        self.test_setup()
        bandwidths = []
        requirements = {"bandwidth": 20}

        result = self.get_path_constrained(
            "User1", "User2", base=requirements)

        if result:
            for path in result[0]["paths"]:
                for i in range(1, len(path)):
                    endpoint_a = path[i - 1]
                    endpoint_b = path[i]
                    meta_data = self.graph.get_metadata_from_link(
                        endpoint_a, endpoint_b)
                    if meta_data and "bandwidth" in meta_data.keys():
                        bandwidths.append(meta_data["bandwidth"])

        for bandwidth in bandwidths:
            self.assertEqual(bandwidth < requirements["bandwidth"], False)

    def test_path3(self):
        """Tests to see if the edges used in the paths from User 1 to User 2
        have at least 20 bandwidth and under 30 delay."""

        self.test_setup()
        bandwidths = []
        delays = []
        requirements = {"bandwidth": 20, "delay": 29}

        result = self.get_path_constrained(
            "User1", "User2", base=requirements)

        if result:
            for path in result[0]["paths"]:
                for i in range(1, len(path)):
                    endpoint_a = path[i - 1]
                    endpoint_b = path[i]
                    meta_data = self.graph.get_metadata_from_link(
                        endpoint_a, endpoint_b)
                    if meta_data and "bandwidth" in meta_data.keys():
                        bandwidths.append(meta_data["bandwidth"])
                    elif meta_data and "delay" in meta_data.keys():
                        delays.append(meta_data["delay"])

        for bandwidth in bandwidths:
            self.assertEqual(bandwidth < requirements["bandwidth"], False)

        for delay in delays:
            self.assertEqual(delay > requirements["delay"], False)

    @staticmethod
    def generate_topology():
        """Generates a predetermined topology"""
        switches = {}
        interfaces = {}
        links = {}

        TestResults.create_switch("User1", switches)
        TestResults.add_interfaces(3, switches["User1"], interfaces)

        TestResults.create_switch("S2", switches)
        TestResults.add_interfaces(2, switches["S2"], interfaces)

        TestResults.create_switch("User2", switches)
        TestResults.add_interfaces(3, switches["User2"], interfaces)

        TestResults.create_switch("S4", switches)
        TestResults.add_interfaces(4, switches["S4"], interfaces)

        TestResults.create_switch("S5", switches)
        TestResults.add_interfaces(2, switches["S5"], interfaces)

        TestResults.create_link("User1:1", "S2:1", interfaces, links)
        TestResults.create_link("User1:2", "S5:1", interfaces, links)
        TestResults.create_link("User1:3", "S4:1", interfaces, links)
        TestResults.create_link("S2:2", "User2:1", interfaces, links)
        TestResults.create_link("User2:2", "S4:2", interfaces, links)
        TestResults.create_link("S5:2", "S4:3", interfaces, links)
        TestResults.create_link("User2:3", "S4:4", interfaces, links)

        TestResults.add_metadata_to_link(
            "User1:1", "S2:1", {
                "reliability": 3, "ownership": "B", "delay": 30,
                "bandwidth": 20}, links)
        TestResults.add_metadata_to_link(
            "User1:2", "S5:1", {
                "reliability": 1, "ownership": "A", "delay": 5,
                "bandwidth": 50}, links)
        TestResults.add_metadata_to_link(
            "User1:3", "S4:1", {
                "reliability": 3, "ownership": "A", "delay": 60,
                "bandwidth": 10}, links)
        TestResults.add_metadata_to_link(
            "S2:2", "User2:1", {
                "reliability": 3, "ownership": "B", "delay": 30,
                "bandwidth": 20}, links)
        TestResults.add_metadata_to_link(
            "User2:2", "S4:2", {
                "reliability": 3, "ownership": "B", "delay": 30,
                "bandwidth": 10}, links)
        TestResults.add_metadata_to_link(
            "S5:2", "S4:3", {
                "reliability": 1, "ownership": "A", "delay": 10,
                "bandwidth": 50}, links)
        TestResults.add_metadata_to_link(
            "User2:3", "S4:4", {
                "reliability": 3, "ownership": "A", "delay": 29,
                "bandwidth": 20}, links)

        return (switches, links)
