"""Module to test the KytosGraph in graph.py."""
from unittest import TestCase
from unittest.mock import Mock

import networkx as nx
from kytos.core.interface import Interface
from kytos.core.link import Link
# Core modules to import
from kytos.core.switch import Switch

# module under test
from graph import KytosGraph


class TestSearchResults(TestCase):

    def setup(self):
        """Setup for most tests"""
        switches, links = self.generate_topology()
        self.graph = KytosGraph()
        self.graph.clear()
        self.graph.update_nodes(switches)
        self.graph.update_links(links)
        self.graph.set_path_fun(nx.shortest_simple_paths)

    def get_path(self, source, destination):
        '''Return the shortest path'''
        results = self.graph.shortest_paths(source, destination)
        return results

    def get_path_constrained(self, source, destination, flexible=0, **metrics):
        '''Return the constrained shortest path'''
        results = self.graph.constrained_flexible_paths(
            source, destination, {}, metrics, flexible)
        return results

    def get_path_constrained2(self, source, destination, metrics,
                              flexible_metrics):
        '''Return the constrained shortest path'''
        return self.graph.constrained_flexible_paths(source, destination,
                                                     metrics, flexible_metrics)

    def test_setup(self):
        """Provides information on default test setup"""
        self.setup()

    @staticmethod
    def generate_topology():
        """Generates a predetermined topology"""
        switches = {}
        links = {}
        return (switches, links)

    @staticmethod
    def create_switch(name, switches):
        '''Add a new switch to the list of switches'''
        switches[name] = Switch(name)

    @staticmethod
    def add_interfaces(count, switch, interfaces):
        '''Add a new interface to the list of interfaces'''
        for i in range(1, count + 1):
            str1 = "{}:{}".format(switch.dpid, i)
            interface = Interface(str1, i, switch)
            interfaces[str1] = interface
            switch.update_interface(interface)

    @staticmethod
    def create_link(interface_a, interface_b, interfaces, links):
        '''Add a new link between two interfaces into the list of links'''
        compounded = "{}|{}".format(interface_a, interface_b)
        final_name = compounded
        links[final_name] = Link(
            interfaces[interface_a], interfaces[interface_b])

    @staticmethod
    def add_metadata_to_link(interface_a, interface_b, metrics, links):
        '''Add metadata to an existing link in the list of links'''
        compounded = "{}|{}".format(interface_a, interface_b)
        links[compounded].extend_metadata(metrics)
