"""Module to test the KytosGraph in graph.py."""
from unittest import TestCase
from unittest.mock import Mock

import networkx as nx

# module under test
from graph import KytosGraph

# Core modules to import
from kytos.core.switch import Switch
from kytos.core.interface import Interface
from kytos.core.link import Link

class TestSearchResults(TestCase):

    def setup(self):
        """Setup for most tests"""
        switches, links = self.generateTopology()
        self.graph = KytosGraph()
        self.graph.clear()
        self.graph.update_nodes(switches)
        self.graph.update_links(links)
        self.graph.set_path_fun(nx.shortest_simple_paths)

    def get_path(self, source, destination):
        results = self.graph.shortest_paths(source,destination)
        return results

    def get_path_constrained(self, source, destination, flexible = 0, **metrics):
        results = self.graph.constrained_flexible_paths(source, destination,{},metrics,flexible)
        return results

    def get_path_constrained2(self, source, destination, metrics, flexible_metrics):
        return self.graph.constrained_flexible_paths(source, destination, metrics, flexible_metrics)

    def test_setup(self):
        """Provides information on default test setup"""
        self.setup()

    @staticmethod
    def generateTopology():
        """Generates a predetermined topology"""
        switches = {}
        links = {}
        return (switches,links)

    @staticmethod
    def createSwitch(name,switches):
        switches[name] = Switch(name)

    @staticmethod
    def addInterfaces(count,switch,interfaces):
        for x in range(1,count + 1):
            str1 = "{}:{}".format(switch.dpid,x)
            iFace = Interface(str1,x,switch)
            interfaces[str1] = iFace
            switch.update_interface(iFace)

    @staticmethod
    def createLink(interface_a, interface_b, interfaces, links):
        compounded = "{}|{}".format(interface_a, interface_b)
        final_name = compounded
        links[final_name] = Link(interfaces[interface_a], interfaces[interface_b])

    @staticmethod
    def addMetadataToLink(interface_a, interface_b, metrics, links):
        compounded = "{}|{}".format(interface_a, interface_b)
        links[compounded].extend_metadata(metrics)
