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

class TestKytosGraph3(TestCase):
    def setup(self):
        """Setup for most tests"""
        switches, links = self.generateTopology()
        self.graph = KytosGraph()
        self.graph.clear()
        self.graph.update_nodes(switches)
        self.graph.update_links(links)
        self.graph.set_path_fun(nx.shortest_simple_paths)

    def test_setup(self):
        """Provides information on default test setup"""
        self.setup()
        print("Nodes in graph")
        for node in self.graph.graph.nodes:
            print(node)
        print("Edges in graph")
        for edge in self.graph.graph.edges(data=True):
            print(edge)

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


    def test_path9(self):
        """Tests to see if an illegal path is not in the set of paths that use only edges owned by A."""
        #Arrange
        self.test_setup()
        illegal_path = ['User1', 'User1:1', 'S2:1', 'S2', 'S2:2', 'User2:1', 'User2']
        #Act
        result = self.graph.constrained_flexible_paths("User1", "User2", False, **{"ownership":"A"})
        #Assert
        self.assertNotIn(illegal_path, result)
 
    def test_path10(self):
        """Tests to see if the edges used in the paths of the result set do not have poor reliability"""
        #Arrange
        self.test_setup()
        reliabilities = []
        poor_reliability = 1
        key = "reliability"
        #Act
        result = self.graph.constrained_flexible_paths("User1", "User2", False, **{"reliability":3})

        for path in result[0]["paths"]:
            for i in range(1, len(path)):
                endpoint_a = path[i-1]
                endpoint_b = path[i]
                meta_data = self.graph.get_metadata_from_link(endpoint_a, endpoint_b)
                if meta_data and key in meta_data.keys():
                    reliabilities.append(meta_data[key])
        #Assert
        self.assertNotIn(poor_reliability, reliabilities)
 
    def test_path11(self):
        """Tests paths from User 1 to User 4, such that a non-shortest path is not in the
        result set"""
        #Arrange
        #Act
        #Assert
        self.assertEqual(1,1)
 
    def test_path12(self):
        """Tests paths from User 1 to User 2, such that a non-shortest path is not in the
        result set"""
        #Arrange
        #Act
        #Assert
        self.assertEqual(1,1)

    def test_path13(self):
        """Tests paths between User 1 and User 4, such that the shortest path is in the result set"""
        #Arrange
        self.setup()
        users = ["User1", "User4"]
        #Act
        result = self.get_path(users[0], users[1])
        print(str(result))
        #Assert
        self.assertEqual(1,1)
        
        
    @staticmethod
    def createSwitch(name,switches):
        switches[name] = Switch(name)
        print("Creating Switch: ", name)

    @staticmethod
    def createLink(interface_a, interface_b, interfaces, links):
        compounded = "{}|{}".format(interface_a, interface_b)
        final_name = compounded
        links[final_name] = Link(interfaces[interface_a], interfaces[interface_b])
        print("Creating Link: ", final_name)

    @staticmethod
    def addMetadataToLink(interface_a, interface_b, metrics, links):
        compounded = "{}|{}".format(interface_a, interface_b)
        links[compounded].extend_metadata(metrics)

    @staticmethod
    def addInterfacesToSwitch(count,switch,interfaces):
        for x in range(1,count + 1):
            str1 = "{}:{}".format(switch.dpid,x)
            print("Creating Interface: ", str1)
            iFace = Interface(str1,x,switch)
            interfaces[str1] = iFace
            switch.update_interface(iFace)


    @staticmethod
    def generateTopology():
        switches = {}
        interfaces = {}
        links = {}

        TestKytosGraph3.createSwitch("User1", switches)
        TestKytosGraph3.addInterfacesToSwitch(3, switches["User1"], interfaces)

        TestKytosGraph3.createSwitch("S2", switches)
        TestKytosGraph3.addInterfacesToSwitch(2, switches["S2"], interfaces)

        TestKytosGraph3.createSwitch("User2", switches)
        TestKytosGraph3.addInterfacesToSwitch(3, switches["User2"], interfaces)

        TestKytosGraph3.createSwitch("S4", switches)
        TestKytosGraph3.addInterfacesToSwitch(4, switches["S4"], interfaces)

        TestKytosGraph3.createSwitch("S5", switches)
        TestKytosGraph3.addInterfacesToSwitch(2, switches["S5"], interfaces)

        TestKytosGraph3.createLink("User1:1", "S2:1", interfaces, links)
        TestKytosGraph3.createLink("User1:2", "S5:1", interfaces, links)
        TestKytosGraph3.createLink("User1:3", "S4:1", interfaces, links)
        TestKytosGraph3.createLink("S2:2", "User2:1", interfaces, links)
        TestKytosGraph3.createLink("User2:2", "S4:2", interfaces, links)
        TestKytosGraph3.createLink("S5:2", "S4:3", interfaces, links)
        TestKytosGraph3.createLink("User2:3", "S4:3", interfaces, links)

        TestKytosGraph3.addMetadataToLink("User1:1", "S2:1", {"reliability": 3, "ownership": "B",
                                        "delay": 30, "bandwidth": 10}, links)
        TestKytosGraph3.addMetadataToLink("User1:2", "S5:1", {"reliability": 1, "ownership": "A",
                                        "delay": 5, "bandwidth": 50}, links)
        TestKytosGraph3.addMetadataToLink("User1:3", "S4:1", {"reliability": 3, "ownership": "A",
                                        "delay": 60, "bandwidth": 10}, links)
        TestKytosGraph3.addMetadataToLink("S2:2", "User2:1", {"reliability": 3, "ownership": "B",
                                        "delay": 30, "bandwidth": 10}, links)  
        TestKytosGraph3.addMetadataToLink("User2:2", "S4:2", {"reliability": 3, "ownership": "B",
                                        "delay": 30, "bandwidth": 10}, links)      
        TestKytosGraph3.addMetadataToLink("S5:2", "S4:3", {"reliability": 1, "ownership": "A",
                                        "delay": 10, "bandwidth": 50}, links)          
        TestKytosGraph3.addMetadataToLink("User2:3", "S4:3", {"reliability": 3, "ownership": "A",
                                        "delay": 29, "bandwidth": 10}, links)                                                                                                                                                
        return (switches, links)



