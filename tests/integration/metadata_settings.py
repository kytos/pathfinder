"""Module to overwrite all the needed methods to test the KytosGraph in graph.py"""
from tests.integration.test_results import TestResults


class MetadataSettings(TestResults):
    """Class to setups all the settings related to topology."""
    @staticmethod
    def generate_topology():
        """Generates a predetermined topology."""
        switches = {}
        interfaces = {}
        links = {}

        MetadataSettings.setting_switches_interfaces(interfaces, switches)

        MetadataSettings.setting_links(interfaces, links)

        MetadataSettings.adding_metadata(links)

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

        MetadataSettings.setting_switches_interfaces_1(interfaces, switches)

        MetadataSettings.setting_links_1(interfaces, links)

        MetadataSettings.adding_metadata_1(links)

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

        MetadataSettings.setting_switches_interfaces(interfaces, switches)

        MetadataSettings.setting_links(interfaces, links)

        MetadataSettings.adding_metadata_2(links)

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
