"""Module to test the KytosGraph in graph.py."""

# module under test
from tests.integration.test_results import TestResults


class TestResultsMetadata(TestResults):
    """Tests for the graph class.

    Tests if the metadata in search result edges have passing values.
    """

    def test_path_constrained_user_user(self):
        """Test to see if there is a constrained
        path between User - User."""
        self.initializer()
        result = self.get_path_constrained("User1", "User2")
        self.assertNotEqual(result, [], True)

    def test_path_constrained_user_switch(self):
        """Test to see if there is a constrained
        path between User - Switch."""
        self.initializer()
        result = self.get_path_constrained("User1", "S4")
        self.assertNotEqual(result, [], True)

    def test_path_constrained_switch_switch(self):
        """Test to see if there is a constrained
        path between Switch - Switch."""
        self.initializer()
        result = self.get_path_constrained("S2", "S4")
        self.assertNotEqual(result, [], True)

    def test_no_path_constrained_user_user(self):
        """Test to see if there is NOT a constrained
        path between User - User."""
        self.initializer()
        result = self.get_path_constrained("User1", "User3")
        self.assertEqual(result, [], True)

    def test_path_constrained_user_user_t1(self):
        """Test to see if there is a constrained path between
        User - User using the 2nd topology variant."""
        self.initializer(val=1)
        result = self.get_path_constrained("User1", "User3")
        self.assertNotEqual(result, [], True)

    def test_no_path_constrained_user_user_t1(self):
        """Test to see if there is NOT a constrained path between
        User - User using the 2nd topology variant."""
        self.initializer(val=1)
        result = self.get_path_constrained("User1", "User2")
        self.assertEqual(result, [], True)

    def test_no_path_constrained_switch_switch_t1(self):
        """Test to see if there is NOT a constrained path between
        Switch - Switch using the 2nd topology variant."""
        self.initializer(val=1)
        result = self.get_path_constrained("S1", "S2")
        self.assertEqual(result, [], True)

    def test_path_constrained_user_user_t2(self):
        """Test to see if there is a constrained path between
        User - User using the 3rd topology variant."""
        self.initializer(val=2)
        result = self.get_path_constrained("User1", "User2")
        self.assertNotEqual(result, [], True)

    def test_path_constrained_user_switch_t2(self):
        """Test to see if there is a constrained path between
        User - Switch using the 3rd topology variant."""
        self.initializer(val=2)
        result = self.get_path_constrained("User1", "S4")
        self.assertNotEqual(result, [], True)

    def test_path_constrained_switch_switch_t2(self):
        """Test to see if there is a constrained path between
        two switches using the 3rd topology variant."""
        self.initializer(val=2)
        result = self.get_path_constrained("S2", "S4")
        self.assertNotEqual(result, [], True)

    def test_path_constrained_reliability(self):
        """Tests to see if the edges used in the paths
        of the result set do not have poor reliability
        """
        requirements = {"reliability": 3}

        self.initializer()

        result = self.get_path_constrained("User1", "User2", base=requirements)

        self.assertNotEqual(result, [])

    def test_no_path_constrained_reliability(self):
        """Tests to see if the edges used in the paths
        of the result set do not have poor reliability
        """
        requirements = {"reliability": 3}

        self.initializer()

        result = self.get_path_constrained("User1", "User3", base=requirements)

        self.assertEqual(result, [])

    def test_path_constrained_reliability_detailed(self):
        """Tests to see if the edges used in the paths
        of the result set do not have poor reliability
        """
        reliabilities = []
        requirements = {"reliability": 3}
        poor_reliability = 1

        self.initializer()

        result = self.get_path_constrained("User1", "User2", base=requirements)

        if result:
            for path in result[0]["paths"]:
                for i in range(1, len(path)):
                    endpoint_a = path[i - 1]
                    endpoint_b = path[i]
                    meta_data = self.graph.get_link_metadata(
                        endpoint_a, endpoint_b)
                    if meta_data and "reliability" in meta_data.keys():
                        reliabilities.append(meta_data["reliability"])

            self.assertNotIn(poor_reliability, reliabilities)

        else:
            self.assertNotEqual(result, [])

    def test_path_constrained_delay(self):
        """Tests to see if the edges used in the paths
        from User 1 to User 2 have less than 30 delay.
        """
        delays = []
        requirements = {"delay": 29}

        self.initializer()

        result = self.get_path_constrained("User1", "User2", base=requirements)

        if result:
            for path in result[0]["paths"]:
                for i in range(1, len(path)):
                    endpoint_a = path[i - 1]
                    endpoint_b = path[i]
                    meta_data = self.graph.get_link_metadata(
                        endpoint_a, endpoint_b)
                    if meta_data and "delay" in meta_data.keys():
                        delays.append(meta_data["delay"])

        if not delays:
            self.assertNotEqual(delays, [])

        valid = True
        for delay in delays:
            if delay > requirements["delay"]:
                valid = False
                break

        self.assertEqual(valid, True)

    def test_path_constrained_bandwidth_detailed(self):
        """Tests to see if the edges used in the paths
        from User 1 to User 2 have at least 20 bandwidth.
        """
        bandwidths = []
        requirements = {"bandwidth": 20}

        self.initializer()

        result = self.get_path_constrained("User1", "User2", base=requirements)

        if result:
            for path in result[0]["paths"]:
                for i in range(1, len(path)):
                    endpoint_a = path[i - 1]
                    endpoint_b = path[i]
                    meta_data = self.graph.get_link_metadata(
                        endpoint_a, endpoint_b)
                    if meta_data and "bandwidth" in meta_data.keys():
                        bandwidths.append(meta_data["bandwidth"])

            # for bandwidth in bandwidths:
            #     self.assertEqual(bandwidth < requirements["bandwidth"], False)
            valid = True
            for bandwidth in bandwidths:
                if bandwidth < requirements["bandwidth"]:
                    valid = False
                    break

            self.assertEqual(valid, True)

    def test_path_constrained_bandwidth_detailed_t2(self):
        """Tests to see if the edges used in the paths
        from User 1 to User 2 have at least 20 bandwidth.
        """
        bandwidths = []
        requirements = {"bandwidth": 20}

        self.initializer(val=2)

        result = self.get_path_constrained("User1", "User2", base=requirements)

        if result:
            for path in result[0]["paths"]:
                for i in range(1, len(path)):
                    endpoint_a = path[i - 1]
                    endpoint_b = path[i]
                    meta_data = self.graph.get_link_metadata(
                        endpoint_a, endpoint_b)
                    if meta_data and "bandwidth" in meta_data.keys():
                        bandwidths.append(meta_data["bandwidth"])

            for bandwidth in bandwidths:
                self.assertEqual(bandwidth < requirements["bandwidth"], False)

    def test_path_constrained_bandwidth_delay(self):
        """Tests to see if the edges used in the paths from User 1
        to User 2 have at least 20 bandwidth and under 30 delay.
        """
        bandwidths = []
        delays = []
        requirements = {"bandwidth": 20, "delay": 29}

        self.initializer()

        result = self.get_path_constrained("User1", "User2", base=requirements)

        if result:
            for path in result[0]["paths"]:
                for i in range(1, len(path)):
                    endpoint_a = path[i - 1]
                    endpoint_b = path[i]
                    meta_data = self.graph.get_link_metadata(
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
        """Generates a predetermined topology."""
        switches = {}
        interfaces = {}
        links = {}

        TestResultsMetadata.setting_switches_interfaces(interfaces, switches)

        TestResultsMetadata.setting_links(interfaces, links)

        TestResultsMetadata.adding_metadata(links)

        return switches, links

    @staticmethod
    def setting_switches_interfaces(interfaces, switches):
        """Generates the switches in a a predetermined topology."""
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

    @staticmethod
    def setting_links(interfaces, links):
        """Generates the links in a a predetermined topology."""
        TestResults.create_link("User1:1", "S2:1", interfaces, links)

        TestResults.create_link("User1:2", "S5:1", interfaces, links)

        TestResults.create_link("User1:3", "S4:1", interfaces, links)

        TestResults.create_link("S2:2", "User2:1", interfaces, links)

        TestResults.create_link("User2:2", "S4:2", interfaces, links)

        TestResults.create_link("S5:2", "S4:3", interfaces, links)

        TestResults.create_link("User2:3", "S4:4", interfaces, links)

    @staticmethod
    def adding_metadata(links):
        """Add the links' metadata in a a predetermined topology."""
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

    @staticmethod
    def generate_topology_1():
        """Generates a predetermined topology
        - 2nd Variant."""
        switches = {}
        interfaces = {}
        links = {}

        TestResultsMetadata.setting_switches_interfaces_1(interfaces, switches)

        TestResultsMetadata.setting_links_1(interfaces, links)

        TestResultsMetadata.adding_metadata_1(links)

        return switches, links

    @staticmethod
    def setting_switches_interfaces_1(interfaces, switches):
        """Generates the switches in a a predetermined topology
        - 2nd variant."""
        TestResults.create_switch("User1", switches)
        TestResults.add_interfaces(2, switches["User1"], interfaces)

        TestResults.create_switch("User2", switches)
        TestResults.add_interfaces(2, switches["User2"], interfaces)

        TestResults.create_switch("User3", switches)
        TestResults.add_interfaces(2, switches["User3"], interfaces)

        TestResults.create_switch("S1", switches)
        TestResults.add_interfaces(1, switches["S1"], interfaces)

        TestResults.create_switch("S2", switches)
        TestResults.add_interfaces(1, switches["S2"], interfaces)

        TestResults.create_switch("S3", switches)
        TestResults.add_interfaces(2, switches["S3"], interfaces)

    @staticmethod
    def setting_links_1(interfaces, links):
        """Generates the links in a a predetermined topology
        - 2nd Variant."""
        TestResults.create_link("User1:1", "S1:1", interfaces, links)

        TestResults.create_link("User1:2", "S3:1", interfaces, links)

        TestResults.create_link("User2:1", "S2:1", interfaces, links)

        TestResults.create_link("User3:1", "S3:2", interfaces, links)

    @staticmethod
    def adding_metadata_1(links):
        """Add the links' metadata in a a predetermined topology
        - 2nd Variant."""
        TestResults.add_metadata_to_link(
            "User1:1", "S1:1", {
                "reliability": 3, "ownership": "B", "delay": 30,
                "bandwidth": 20}, links)

        TestResults.add_metadata_to_link(
            "User1:2", "S3:1", {
                "reliability": 1, "ownership": "A", "delay": 5,
                "bandwidth": 50}, links)

        TestResults.add_metadata_to_link(
            "User2:1", "S2:1", {
                "reliability": 3, "ownership": "A", "delay": 60,
                "bandwidth": 10}, links)

        TestResults.add_metadata_to_link(
            "User3:1", "S3:2", {
                "reliability": 3, "ownership": "B", "delay": 30,
                "bandwidth": 20}, links)

    @staticmethod
    def generate_topology_2():
        """Generates a predetermined topology
        - 3rd Variant."""
        switches = {}
        interfaces = {}
        links = {}

        TestResultsMetadata.setting_switches_interfaces(interfaces, switches)

        TestResultsMetadata.setting_links(interfaces, links)

        TestResultsMetadata.adding_metadata_2(links)

        return switches, links

    @staticmethod
    def adding_metadata_2(links):
        """Add the links' metadata in a a predetermined topology
        - 3rd Variant."""
        TestResults.add_metadata_to_link(
            "User1:1", "S2:1", {
                "reliability": 3, "ownership": "B",
                "bandwidth": 20}, links)

        TestResults.add_metadata_to_link(
            "User1:2", "S5:1", {
                "reliability": 1, "delay": 5,
                "bandwidth": 50}, links)

        TestResults.add_metadata_to_link(
            "User1:3", "S4:1", {
                "ownership": "A", "delay": 60,
                "bandwidth": 10}, links)

        TestResults.add_metadata_to_link(
            "S2:2", "User2:1", {
                "reliability": 3,
                "bandwidth": 20}, links)

        TestResults.add_metadata_to_link(
            "User2:2", "S4:2", {
                "ownership": "B",
                "bandwidth": 10}, links)

        TestResults.add_metadata_to_link(
            "S5:2", "S4:3", {
                "delay": 10,
                "bandwidth": 50}, links)

        TestResults.add_metadata_to_link(
            "User2:3", "S4:4", {
                "bandwidth": 20}, links)
