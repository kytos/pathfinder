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
from kytos.core import KytosEvent

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
        result = self.graph.shortest_paths(source,destination)
        print(f"Path result: {result}")
        return result

    def get_path_constrained(self, source, destination, flexible = False, **metrics):
        print(f"Attempting path between {source} and {destination}.")
        print(f"Filtering with the following metrics: {metrics}")
        print(f"Flexible is set to {flexible}")
        if flexible:
            result = self.graph.constrained_flexible(source,destination,**metrics)
        else:
            result = self.graph.constrained_shortest_paths(source,destination, **metrics)
        print(f"Path result: {result}")
        return result

    def test_setup(self):
        """Provides information on default test setup"""
        self.setup()
        print("Nodes in graph")
        for node in self.graph.graph.nodes:
            print(node)
        print("Edges in graph")
        for edge in self.graph.graph.edges(data=True):
            print(edge)
    
    def test_path1(self):
        """Tests a simple, definetly possible path"""
        self.setup()
        result = self.get_path("S1","S2")
        self.assertNotEqual(result, [])

    def test_constrained_path1(self):
        """Tests a simple, definetly possible path"""
        self.setup()
        result = self.get_path_constrained("S1","S2")
        self.assertNotEqual(result, [])

    def test_path2(self):
        """Tests a simple, impossible path"""
        self.setup()
        result = self.get_path("S1","S4")
        self.assertEqual(result, [])

    def test_constrained_path2(self):
        """Tests a simple, impossible path"""
        self.setup()
        result = self.get_path_constrained("S1","S4")
        self.assertEqual(result, [])

    def test_path3(self):
        """Tests a path to self"""
        self.setup()
        result = self.get_path("S4","S4")
        self.assertNotEqual(result, [])

    def test_constrained_path3(self):
        """Tests a path to self"""
        self.setup()
        result = self.get_path_constrained("S4","S4")
        self.assertNotEqual(result, [])

    def test_path4(self):
        """Tests a path to self again"""
        self.setup()
        result = self.get_path("S1","S1")
        self.assertNotEqual(result, [])

    def test_constrained_path4(self):
        """Tests a path to self again"""
        self.setup()
        result = self.get_path_constrained("S1","S1")
        self.assertNotEqual(result, [])

    def test_constrained_path5(self):
        """Tests constrained path"""
        self.setup()
        result = self.get_path_constrained("S1","S3", False, bandwidth = 50)
        self.assertNotIn(['S1', 'S1:2', 'S3:2', 'S3'], result)

    def test_constrained_path6(self):
        """Tests constrained path"""
        self.setup()
        result = self.get_path_constrained("S1","S2", False, ownership = "red")
        self.assertNotIn(['S1', 'S1:2', 'S3:2', 'S3', 'S3:1', 'S2:2', 'S2'],result)

    def test_constrained_path7(self):
        """Tests constrained path"""
        self.setup()
        result = self.get_path_constrained("S1","S2", False, ownership = "blue")
        self.assertNotIn(['S1', 'S1:1', 'S2:1', 'S2'],result)

    def test_constrained_path8(self):
        """Tests constrained path, to self AGAIN"""
        self.setup()
        result = self.get_path_constrained("S5","S5", False, ownership = "blue")
        self.assertNotEqual([],result)
        self.assertIn(['S5'],result)

    def test_constrained_path9(self):
        """Tests constrained path"""
        self.setup()
        result = self.get_path_constrained("S1","S2", True, ownership = "blue")

    @staticmethod
    def generateTopology():
        """Generates a predetermined topology"""
        switches = {}
        interfaces = {}

        TestKytosGraph.createSwitch("S1",switches)
        TestKytosGraph.addInterfaces(2, switches["S1"], interfaces)

        TestKytosGraph.createSwitch("S2",switches)
        TestKytosGraph.addInterfaces(3, switches["S2"], interfaces)

        TestKytosGraph.createSwitch("S3",switches)
        TestKytosGraph.addInterfaces(2, switches["S3"], interfaces)

        TestKytosGraph.createSwitch("S4",switches)
        TestKytosGraph.addInterfaces(2, switches["S4"], interfaces)

        TestKytosGraph.createSwitch("S5",switches)

        links = {}

        links["S1:1<->S2:1"] = Link(interfaces["S1:1"], interfaces["S2:1"])
        links["S1:1<->S2:1"].extend_metadata({"bandwidth":50,"ownership":"red"})

        links["S3:1<->S2:2"] = Link(interfaces["S3:1"], interfaces["S2:2"])
        links["S3:1<->S2:2"].extend_metadata({"bandwidth":51,"ownership":"blue"})

        links["S1:2<->S3:2"] = Link(interfaces["S1:2"], interfaces["S3:2"])
        links["S1:2<->S3:2"].extend_metadata({"bandwidth":49,"ownership":"blue"}) 

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

