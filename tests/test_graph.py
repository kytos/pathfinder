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

class TestKytosGraph(TestCase):

    def setup(self):
        """Setup for most tests"""
        switches, links = self.generateTopology()
        self.graph = KytosGraph()
        self.graph.clear()
        self.graph.update_nodes(switches)
        self.graph.update_links(links)
        self.graph.set_path_fun(nx.shortest_simple_paths)

    def get_path(self, source, destination):
        print(f"Attempting path between {source} and {destination}.")
        results = self.graph.shortest_paths(source,destination)
        print(f"Results: {results}")
        return results

    def get_path_constrained(self, source, destination, flexible = 0, **metrics):
        print(f"Attempting path between {source} and {destination}.")
        print(f"Filtering with the following metrics: {metrics}")
        print(f"Flexible is set to {flexible}")
        results = self.graph.constrained_flexible_paths(source,destination,flexible,**metrics)
        print(f"Results: {results}")
        return results

    def test_setup(self):
        """Provides information on default test setup"""
        self.setup()
        print("Nodes in graph")
        for node in self.graph.graph.nodes:
            print(node)
        print("Edges in graph")
        for edge in self.graph.graph.edges(data=True):
            print(edge)

    @staticmethod
    def generateTopology():
        """Generates a predetermined topology"""
        switches = {}
        interfaces = {}
        links = {}
        return (switches,links)

    @staticmethod
    def createSwitch(name,switches):
        switches[name] = Switch(name)
        print("Creating Switch: ", name)

    @staticmethod
    def addInterfaces(count,switch,interfaces):
        for x in range(1,count + 1):
            str1 = "{}:{}".format(switch.dpid,x)
            print("Creating Interface: ", str1)
            iFace = Interface(str1,x,switch)
            interfaces[str1] = iFace
            switch.update_interface(iFace)

