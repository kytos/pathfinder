"""Module to test the KytosGraph in graph.py."""
from unittest import TestCase
from unittest.mock import Mock
from itertools import combinations

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
        """Tests paths between all users using unconstrained path alogrithm."""
        self.setup()
        combos = combinations(["User1","User2","User3","User4"],2)
        for point_a, point_b in combos:
            result = self.get_path(point_a,point_b)
            self.assertNotEqual(result, [])

    def test_path2(self):
        """Tests paths between all users using constrained path algorithm,
        with no constraints set."""
        self.setup()
        combos = combinations(["User1","User2","User3","User4"],2)
        for point_a, point_b in combos:
            result = self.get_path_constrained(point_a,point_b)
            self.assertNotEqual(result, [])

    def test_path3(self):
        """Tests paths between all users using constrained path algorithm,
        with the ownership constraint set to B."""
        self.setup()
        combos = combinations(["User1","User2","User3","User4"],2)
        for point_a, point_b in combos:
            result = self.get_path_constrained(point_a, point_b, False, ownership = "B")
            for path in result:
                self.assertNotIn("S4:1", path)
                self.assertNotIn("S5:2", path)
                self.assertNotIn("S4:2", path)
                self.assertNotIn("User1:2", path)
                self.assertNotIn("S5:4", path)
                self.assertNotIn("S6:2", path)
                self.assertNotIn("S6:5", path)
                self.assertNotIn("S10:1", path)
                self.assertNotIn("S8:6", path)
                self.assertNotIn("S10:2", path)
                self.assertNotIn("S10:3", path)
                self.assertNotIn("User2:1", path)

    def test_path4(self):
        """Tests paths between all users using constrained path algorithm,
        with the reliability constraint set to 3."""
        self.setup()
        combos = combinations(["User1","User2","User3","User4"],2)
        for point_a, point_b in combos:
            result = self.get_path_constrained(point_a, point_b, False, reliability = 3)
            for path in result:
                self.assertNotIn("S4:1", path)
                self.assertNotIn("S5:2", path)
                self.assertNotIn("S5:3", path)
                self.assertNotIn("S6:1", path)

    def test_path5(self):
        """Tests paths between all users using constrained path algorithm,
        with the bandwidth contraint set to 100."""
        self.setup()
        combos = combinations(["User1","User2","User3","User4"],2)
        for point_a, point_b in combos:
            result = self.get_path_constrained(point_a, point_b, False, bandwidth = 100)
            for path in result:
                self.assertNotIn("S3:1", path)
                self.assertNotIn("S5:1", path)
                self.assertNotIn("User1:4", path)
                self.assertNotIn("User4:3", path)

    def test_path6(self):
        """Tests paths between all users using constrained path algorithm,
        with the delay constraint set to 50."""
        self.setup()
        combos = combinations(["User1","User2","User3","User4"],2)
        for point_a, point_b in combos:
            result = self.get_path_constrained(point_a, point_b, False, delay = 50)
            for path in result:
                self.assertNotIn("S1:1", path)
                self.assertNotIn("S2:1", path)
                self.assertNotIn("S3:1", path)
                self.assertNotIn("S5:1", path)
                self.assertNotIn("S4:2", path)
                self.assertNotIn("User1:2", path)
                self.assertNotIn("S5:5", path)
                self.assertNotIn("S8:2", path)
                self.assertNotIn("S5:6", path)
                self.assertNotIn("User1:3", path)
                self.assertNotIn("S6:3", path)
                self.assertNotIn("S9:1", path)
                self.assertNotIn("S6:4", path)
                self.assertNotIn("S9:2", path)
                self.assertNotIn("S6:5", path)
                self.assertNotIn("S10:1", path)
                self.assertNotIn("S8:5", path)
                self.assertNotIn("S9:4", path)
                self.assertNotIn("User1:4", path)
                self.assertNotIn("User4:3", path)
            

    @staticmethod
    def generateTopology():
        """Generates a predetermined topology"""
        switches = {}
        interfaces = {}
        links = {}

        TestKytosGraph.createSwitch("S1", switches)
        TestKytosGraph.addInterfaces(2, switches["S1"], interfaces)

        TestKytosGraph.createSwitch("S2", switches)
        TestKytosGraph.addInterfaces(2, switches["S2"], interfaces)

        TestKytosGraph.createSwitch("S3", switches)
        TestKytosGraph.addInterfaces(6, switches["S3"], interfaces)

        TestKytosGraph.createSwitch("S4", switches)
        TestKytosGraph.addInterfaces(2, switches["S4"], interfaces)

        TestKytosGraph.createSwitch("S5", switches)
        TestKytosGraph.addInterfaces(6, switches["S5"], interfaces)

        TestKytosGraph.createSwitch("S6", switches)
        TestKytosGraph.addInterfaces(5, switches["S6"], interfaces)

        TestKytosGraph.createSwitch("S7", switches)
        TestKytosGraph.addInterfaces(2, switches["S7"], interfaces)

        TestKytosGraph.createSwitch("S8", switches)
        TestKytosGraph.addInterfaces(8, switches["S8"], interfaces)

        TestKytosGraph.createSwitch("S9", switches)
        TestKytosGraph.addInterfaces(4, switches["S9"], interfaces)

        TestKytosGraph.createSwitch("S10", switches)
        TestKytosGraph.addInterfaces(3, switches["S10"], interfaces)

        TestKytosGraph.createSwitch("S11", switches)
        TestKytosGraph.addInterfaces(3, switches["S11"], interfaces)

        TestKytosGraph.createSwitch("User1", switches)
        TestKytosGraph.addInterfaces(4, switches["User1"], interfaces)

        TestKytosGraph.createSwitch("User2", switches)
        TestKytosGraph.addInterfaces(2, switches["User2"], interfaces)

        TestKytosGraph.createSwitch("User3", switches)
        TestKytosGraph.addInterfaces(2, switches["User3"], interfaces)

        TestKytosGraph.createSwitch("User4", switches)
        TestKytosGraph.addInterfaces(3, switches["User4"], interfaces)

        links["S1:1<->S2:1"] = Link(interfaces["S1:1"], interfaces["S2:1"])
        links["S1:1<->S2:1"].extend_metadata({"reliability": 5, "bandwidth": 100, "delay": 105})

        links["S1:2<->User1:1"] = Link(interfaces["S1:2"], interfaces["User1:1"])
        links["S1:2<->User1:1"].extend_metadata({"reliability": 5, "bandwidth": 100, "delay": 1})

        links["S2:2<->User4:1"] = Link(interfaces["S2:2"], interfaces["User4:1"])
        links["S2:2<->User4:1"].extend_metadata({"reliability": 5, "bandwidth": 100, "delay": 10})

        links["S3:1<->S5:1"] = Link(interfaces["S3:1"], interfaces["S5:1"])
        links["S3:1<->S5:1"].extend_metadata({"reliability": 5, "bandwidth": 10, "delay": 112})

        links["S3:2<->S7:1"] = Link(interfaces["S3:2"], interfaces["S7:1"])
        links["S3:2<->S7:1"].extend_metadata({"reliability": 5, "bandwidth": 100, "delay": 1})

        links["S3:3<->S8:1"] = Link(interfaces["S3:3"], interfaces["S8:1"])
        links["S3:3<->S8:1"].extend_metadata({"reliability": 5, "bandwidth": 100, "delay": 1})

        links["S3:4<->S11:1"] = Link(interfaces["S3:4"], interfaces["S11:1"])
        links["S3:4<->S11:1"].extend_metadata({"reliability": 3, "bandwidth": 100, "delay": 6})

        links["S3:5<->User3:1"] = Link(interfaces["S3:5"], interfaces["User3:1"])
        links["S3:5<->User3:1"].extend_metadata({"reliability": 5, "bandwidth": 100, "delay": 1})

        links["S3:6<->User4:2"] = Link(interfaces["S3:6"], interfaces["User4:2"])
        links["S3:6<->User4:2"].extend_metadata({"reliability": 5, "bandwidth": 100, "delay": 10})

        links["S4:1<->S5:2"] = Link(interfaces["S4:1"], interfaces["S5:2"])
        links["S4:1<->S5:2"].extend_metadata({"reliability": 1, "bandwidth": 100, "delay": 30, "ownership": "A"})

        links["S4:2<->User1:2"] = Link(interfaces["S4:2"], interfaces["User1:2"])
        links["S4:2<->User1:2"].extend_metadata({"reliability": 3, "bandwidth": 100, "delay": 110, "ownership": "A"})

        links["S5:3<->S6:1"] = Link(interfaces["S5:3"], interfaces["S6:1"])
        links["S5:3<->S6:1"].extend_metadata({"reliability": 1, "bandwidth": 100, "delay": 40})

        links["S5:4<->S6:2"] = Link(interfaces["S5:4"], interfaces["S6:2"])
        links["S5:4<->S6:2"].extend_metadata({"reliability": 3, "bandwidth": 100, "delay": 40, "ownership": "A"})

        links["S5:5<->S8:2"] = Link(interfaces["S5:5"], interfaces["S8:2"])
        links["S5:5<->S8:2"].extend_metadata({"reliability": 5, "bandwidth": 100, "delay": 112})

        links["S5:6<->User1:3"] = Link(interfaces["S5:6"], interfaces["User1:3"])
        links["S5:6<->User1:3"].extend_metadata({"reliability": 3, "bandwidth": 100, "delay": 60})

        links["S6:3<->S9:1"] = Link(interfaces["S6:3"], interfaces["S9:1"])
        links["S6:3<->S9:1"].extend_metadata({"reliability": 3,"bandwidth": 100, "delay":60})

        links["S6:4<->S9:2"] = Link(interfaces["S6:4"], interfaces["S9:2"])
        links["S6:4<->S9:2"].extend_metadata({"reliability": 5,"bandwidth": 100, "delay":62})

        links["S6:5<->S10:1"] = Link(interfaces["S6:5"], interfaces["S10:1"])
        links["S6:5<->S10:1"].extend_metadata({"bandwidth": 100, "delay":108, "ownership":"A"})

        links["S7:2<->S8:3"] = Link(interfaces["S7:2"], interfaces["S8:3"])
        links["S7:2<->S8:3"].extend_metadata({"reliability": 5, "bandwidth": 100, "delay": 1})

        links["S8:4<->S9:3"] = Link(interfaces["S8:4"], interfaces["S9:3"])
        links["S8:4<->S9:3"].extend_metadata({"reliability": 3,"bandwidth": 100, "delay":32})

        links["S8:5<->S9:4"] = Link(interfaces["S8:5"], interfaces["S9:4"])
        links["S8:5<->S9:4"].extend_metadata({"reliability": 3,"bandwidth": 100, "delay":110})

        links["S8:6<->S10:2"] = Link(interfaces["S8:6"], interfaces["S10:2"])
        links["S8:6<->S10:2"].extend_metadata({"reliability": 5, "bandwidth": 100, "ownership":"A"})

        links["S8:7<->S11:2"] = Link(interfaces["S8:7"], interfaces["S11:2"])
        links["S8:7<->S11:2"].extend_metadata({"reliability": 3, "bandwidth": 100, "delay": 7})

        links["S8:8<->User3:2"] = Link(interfaces["S8:8"], interfaces["User3:2"])
        links["S8:8<->User3:2"].extend_metadata({"reliability": 5, "bandwidth": 100, "delay": 1})

        links["S10:3<->User2:1"] = Link(interfaces["S10:3"], interfaces["User2:1"])
        links["S10:3<->User2:1"].extend_metadata({"reliability": 3, "bandwidth": 100, "delay": 10, "ownership":"A"})

        links["S11:3<->User2:2"] = Link(interfaces["S11:3"], interfaces["User2:2"])
        links["S11:3<->User2:2"].extend_metadata({"reliability": 3, "bandwidth": 100, "delay": 6})

        links["User1:4<->User4:3"] = Link(interfaces["User1:4"], interfaces["User4:3"])
        links["User1:4<->User4:3"].extend_metadata({"reliability": 5, "bandwidth": 10, "delay": 105})

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

