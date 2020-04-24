"""Module to test the KytosGraph in graph.py."""
from unittest import TestCase
from unittest.mock import Mock

import networkx as nx

# module under test
from graph import KytosGraph

from tests.test_graph import TestKytosGraph

# Core modules to import
from kytos.core.switch import Switch
from kytos.core.interface import Interface
from kytos.core.link import Link

class TestGraph3(TestKytosGraph):

    def test_path9(self):
        """Tests to see if an illegal path is not in the set of paths that use only edges owned by A."""
        #Arrange
        self.test_setup()
        illegal_path = ['User1', 'User1:1', 'S2:1', 'S2', 'S2:2', 'User2:1', 'User2']
        #Act
        result = self.get_path_constrained("User1", "User2", 0, ownership = 'A')
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
        result = self.get_path_constrained("User1", "User2", 0, reliability = 3)

        if result:
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
        """Tests to see if the edges used in the paths from User 1 to User 2 have less than 30 delay."""
        #Arrange
        self.test_setup()
        delays = []
        delay_cap = 29
        key = "delay"
        has_bad_delay = False
        
        #Act
        result = self.get_path_constrained("User1", "User2", 0, delay = delay_cap)

        if result:
            for path in result[0]["paths"]:
                for i in range(1, len(path)):
                    endpoint_a = path[i-1]
                    endpoint_b = path[i]
                    meta_data = self.graph.get_metadata_from_link(endpoint_a, endpoint_b)
                    if meta_data and key in meta_data.keys():
                        delays.append(meta_data[key])

        #Assert
        for delay in delays:
            has_bad_delay = delay > delay_cap
            self.assertEqual(has_bad_delay, False)
 
    def test_path12(self):
        """Tests to see if the edges used in the paths from User 1 to User 2 have at least 20 bandwidth."""
        #Arrange
        self.test_setup()
        bandwidths = []
        bandwidth_floor = 20
        key = "bandwidth"
        has_bad_bandwidth = False
        
        #Act
        result = self.get_path_constrained("User1", "User2", 0, bandwidth = bandwidth_floor)

        if result:
            for path in result[0]["paths"]:
                for i in range(1, len(path)):
                    endpoint_a = path[i-1]
                    endpoint_b = path[i]
                    meta_data = self.graph.get_metadata_from_link(endpoint_a, endpoint_b)
                    if meta_data and key in meta_data.keys():
                        bandwidths.append(meta_data[key])

        #Assert
        for bandwidth in bandwidths:
            has_bad_bandwidth = bandwidth < bandwidth_floor
            self.assertEqual(has_bad_bandwidth, False)

    def test_path13(self):
        """Tests to see if the edges used in the paths from User 1 to User 2 have at least 20 bandwidth
        and under 30 delay."""
        #Arrange
        self.test_setup()
        bandwidths = []
        delays = []
        bandwidth_floor = 20
        key_a = "bandwidth"
        delay_cap = 29
        key_b = "delay"
        has_bad_bandwidth = False
        has_bad_delay = False

        #Act
        result = self.get_path_constrained("User1", "User2", 0, bandwidth = bandwidth_floor, delay = delay_cap)

        if result:
            for path in result[0]["paths"]:
                for i in range(1, len(path)):
                    endpoint_a = path[i-1]
                    endpoint_b = path[i]
                    meta_data = self.graph.get_metadata_from_link(endpoint_a, endpoint_b)
                    if meta_data and key_a in meta_data.keys():
                        bandwidths.append(meta_data[key_a])
                    elif meta_data and key_b in meta_data.keys():
                        delays.append(meta_data[key_b])
        
        #Assert
        for bandwidth in bandwidths:
            has_bad_bandwidth = bandwidth < bandwidth_floor
            self.assertEqual(has_bad_bandwidth, False)

        for delay in delays:
            has_bad_delay = delay > delay_cap
            self.assertEqual(has_bad_delay, False)

    @staticmethod
    def createLink(interface_a, interface_b, interfaces, links):
        compounded = "{}|{}".format(interface_a, interface_b)
        final_name = compounded
        links[final_name] = Link(interfaces[interface_a], interfaces[interface_b])

    @staticmethod
    def addMetadataToLink(interface_a, interface_b, metrics, links):
        compounded = "{}|{}".format(interface_a, interface_b)
        links[compounded].extend_metadata(metrics)

    @staticmethod
    def generateTopology():
        switches = {}
        interfaces = {}
        links = {}

        TestKytosGraph.createSwitch("User1", switches)
        TestKytosGraph.addInterfaces(3, switches["User1"], interfaces)

        TestKytosGraph.createSwitch("S2", switches)
        TestKytosGraph.addInterfaces(2, switches["S2"], interfaces)

        TestKytosGraph.createSwitch("User2", switches)
        TestKytosGraph.addInterfaces(3, switches["User2"], interfaces)

        TestKytosGraph.createSwitch("S4", switches)
        TestKytosGraph.addInterfaces(4, switches["S4"], interfaces)

        TestKytosGraph.createSwitch("S5", switches)
        TestKytosGraph.addInterfaces(2, switches["S5"], interfaces)

        TestGraph3.createLink("User1:1", "S2:1", interfaces, links)
        TestGraph3.createLink("User1:2", "S5:1", interfaces, links)
        TestGraph3.createLink("User1:3", "S4:1", interfaces, links)
        TestGraph3.createLink("S2:2", "User2:1", interfaces, links)
        TestGraph3.createLink("User2:2", "S4:2", interfaces, links)
        TestGraph3.createLink("S5:2", "S4:3", interfaces, links)
        TestGraph3.createLink("User2:3", "S4:3", interfaces, links)

        TestGraph3.addMetadataToLink("User1:1", "S2:1", {"reliability": 3, "ownership": "B",
                                        "delay": 30, "bandwidth": 20}, links)
        TestGraph3.addMetadataToLink("User1:2", "S5:1", {"reliability": 1, "ownership": "A",
                                        "delay": 5, "bandwidth": 50}, links)
        TestGraph3.addMetadataToLink("User1:3", "S4:1", {"reliability": 3, "ownership": "A",
                                        "delay": 60, "bandwidth": 10}, links)
        TestGraph3.addMetadataToLink("S2:2", "User2:1", {"reliability": 3, "ownership": "B",
                                        "delay": 30, "bandwidth": 20}, links)  
        TestGraph3.addMetadataToLink("User2:2", "S4:2", {"reliability": 3, "ownership": "B",
                                        "delay": 30, "bandwidth": 10}, links)      
        TestGraph3.addMetadataToLink("S5:2", "S4:3", {"reliability": 1, "ownership": "A",
                                        "delay": 10, "bandwidth": 50}, links)          
        TestGraph3.addMetadataToLink("User2:3", "S4:3", {"reliability": 3, "ownership": "A",
                                        "delay": 29, "bandwidth": 20}, links)                                                                                                                                                
        
        return (switches, links)
