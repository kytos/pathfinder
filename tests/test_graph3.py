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

class TestKytosGraph3(TestKytosGraph):
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
        result = self.graph.constrained_flexible_paths("User1", "User2", False, **{key: 3})

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
        #Act
        result = self.graph.constrained_flexible_paths("User1", "User2", False, **{key: delay_cap})

        if result:
            for path in result[0]["paths"]:
                for i in range(1, len(path)):
                    endpoint_a = path[i-1]
                    endpoint_b = path[i]
                    meta_data = self.graph.get_metadata_from_link(endpoint_a, endpoint_b)
                    if meta_data and key in meta_data.keys():
                        delays.append(meta_data[key])

        has_bad_delay = False

        for delay in delays:
            has_bad_delay = delay > delay_cap

        #Assert
        self.assertEqual(has_bad_delay, False)
 
    def test_path12(self):
        """Tests to see if the edges used in the paths from User 1 to User 2 have at least 20 bandwidth."""
        #Arrange
        self.test_setup()
        bandwidths = []
        bandwidth_floor = 20
        key = "bandwidth"
        #Act
        result = self.graph.constrained_flexible_paths("User1", "User2", False, **{key: bandwidth_floor})

        if result:
            for path in result[0]["paths"]:
                for i in range(1, len(path)):
                    endpoint_a = path[i-1]
                    endpoint_b = path[i]
                    meta_data = self.graph.get_metadata_from_link(endpoint_a, endpoint_b)
                    if meta_data and key in meta_data.keys():
                        bandwidths.append(meta_data[key])

        has_bad_bandwidth = False

        for bandwidth in bandwidths:
            has_bad_bandwidth = bandwidth < bandwidth_floor

        #Assert
        self.assertEqual(has_bad_bandwidth, False)

    def test_path13(self):
        """Tests to see if the edges used in the paths from User 1 to User 2 have at least 20 bandwidth
        and under 30 delay."""
        #Arrange
        self.test_setup()
        metrics = []
        bandwidth_floor = 20
        key_a = "bandwidth"
        delay_cap = 29
        key_b = "delay"

        #Act
        result = self.graph.constrained_flexible_paths("User1", "User2", False, **{key_a: bandwidth_floor, key_b: delay_cap})

        if result:
            for path in result[0]["paths"]:
                for i in range(1, len(path)):
                    endpoint_a = path[i-1]
                    endpoint_b = path[i]
                    meta_data = self.graph.get_metadata_from_link(endpoint_a, endpoint_b)
                    if meta_data and key in meta_data.keys():
                        metrics.append(meta_data[key])

        has_bad_bandwidth = False
        has_bad_delay = False

        for metric in metrics:
            has_bad_bandwidth = metric[key_a] < bandwidth_floor
            has_bad_delay = metric[key_b] > delay_cap
        
        has_bad_metrics = has_bad_bandwidth or has_bad_delay
        #Assert
        self.assertEqual(has_bad_metrics, False)
        
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
                                        "delay": 30, "bandwidth": 20}, links)
        TestKytosGraph3.addMetadataToLink("User1:2", "S5:1", {"reliability": 1, "ownership": "A",
                                        "delay": 5, "bandwidth": 50}, links)
        TestKytosGraph3.addMetadataToLink("User1:3", "S4:1", {"reliability": 3, "ownership": "A",
                                        "delay": 60, "bandwidth": 10}, links)
        TestKytosGraph3.addMetadataToLink("S2:2", "User2:1", {"reliability": 3, "ownership": "B",
                                        "delay": 30, "bandwidth": 20}, links)  
        TestKytosGraph3.addMetadataToLink("User2:2", "S4:2", {"reliability": 3, "ownership": "B",
                                        "delay": 30, "bandwidth": 10}, links)      
        TestKytosGraph3.addMetadataToLink("S5:2", "S4:3", {"reliability": 1, "ownership": "A",
                                        "delay": 10, "bandwidth": 50}, links)          
        TestKytosGraph3.addMetadataToLink("User2:3", "S4:3", {"reliability": 3, "ownership": "A",
                                        "delay": 29, "bandwidth": 10}, links)                                                                                                                                                
        return (switches, links)



