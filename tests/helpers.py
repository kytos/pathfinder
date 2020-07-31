"""Module to help to create tests."""
from unittest.mock import MagicMock

from kytos.lib.helpers import (get_interface_mock, get_link_mock,
                               get_switch_mock)


def get_topology_mock():
    """Create a default topology."""
    switch_a = get_switch_mock("00:00:00:00:00:00:00:01", 0x04)
    switch_b = get_switch_mock("00:00:00:00:00:00:00:02", 0x04)
    switch_c = get_switch_mock("00:00:00:00:00:00:00:03", 0x01)

    interface_a1 = get_interface_mock("s1-eth1", 1, switch_a)
    interface_a2 = get_interface_mock("s1-eth2", 2, switch_a)

    interface_b1 = get_interface_mock("s2-eth1", 1, switch_b)
    interface_b2 = get_interface_mock("s2-eth2", 2, switch_b)

    interface_c1 = get_interface_mock("s3-eth1", 1, switch_c)
    interface_c2 = get_interface_mock("s3-eth2", 2, switch_c)

    switch_a.interfaces = {interface_a1.id: interface_a1,
                           interface_a2.id: interface_a2}
    switch_b.interfaces = {interface_b1.id: interface_b1,
                           interface_b2.id: interface_b2}
    switch_c.interfaces = {interface_c1.id: interface_c1,
                           interface_c2.id: interface_c2}

    link_1 = get_link_mock(interface_a1, interface_b1)
    link_2 = get_link_mock(interface_a2, interface_c1)
    link_3 = get_link_mock(interface_b2, interface_c2)

    topology = MagicMock()
    topology.links = {"1": link_1, "2": link_2, "3": link_3}
    topology.switches = {switch_a.dpid: switch_a,
                         switch_b.dpid: switch_b,
                         switch_c.dpid: switch_c}
    return topology


def get_topology_with_metadata_mock():
    """Create a topology with metadata."""
    switches = {}
    interfaces = {}
    links = {}
    i = 0

    switches_to_interface_counts = {"S1": 2, "S2": 2, "S3": 6, "S4": 2,
                                    "S5": 6, "S6": 5, "S7": 2, "S8": 8,
                                    "S9": 4, "S10": 3, "S11": 3,
                                    "User1": 4, "User2": 2,
                                    "User3": 2, "User4": 3}

    links_to_interfaces = [["S1:1", "S2:1"], ["S1:2", "User1:1"],
                           ["S2:2", "User4:1"], ["S3:1", "S5:1"],
                           ["S3:2", "S7:1"], ["S3:3", "S8:1"],
                           ["S3:4", "S11:1"],
                           ["S3:5", "User3:1"], ["S3:6", "User4:2"],
                           ["S4:1", "S5:2"], ["S4:2", "User1:2"],
                           ["S5:3", "S6:1"],
                           ["S5:4", "S6:2"], ["S5:5", "S8:2"],
                           ["S5:6", "User1:3"], ["S6:3", "S9:1"],
                           ["S6:4", "S9:2"], ["S6:5", "S10:1"],
                           ["S7:2", "S8:3"],
                           ["S8:4", "S9:3"], ["S8:5", "S9:4"],
                           ["S8:6", "S10:2"],
                           ["S8:7", "S11:2"], ["S8:8", "User3:2"],
                           ["S10:3", "User2:1"], ["S11:3", "User2:2"],
                           ["User1:4", "User4:3"]]

    links_to_metadata = [
        {"reliability": 5, "bandwidth": 100, "delay": 105},
        {"reliability": 5, "bandwidth": 100, "delay": 1},
        {"reliability": 5, "bandwidth": 100, "delay": 10},
        {"reliability": 5, "bandwidth": 10, "delay": 112},
        {"reliability": 5, "bandwidth": 100, "delay": 1},
        {"reliability": 5, "bandwidth": 100, "delay": 1},
        {"reliability": 3, "bandwidth": 100, "delay": 6},
        {"reliability": 5, "bandwidth": 100, "delay": 1},
        {"reliability": 5, "bandwidth": 100, "delay": 10},
        {"reliability": 1, "bandwidth": 100, "delay": 30, "ownership": "A"},
        {"reliability": 3, "bandwidth": 100, "delay": 110, "ownership": "A"},
        {"reliability": 1, "bandwidth": 100, "delay": 40},
        {"reliability": 3, "bandwidth": 100, "delay": 40, "ownership": "A"},
        {"reliability": 5, "bandwidth": 100, "delay": 112},
        {"reliability": 3, "bandwidth": 100, "delay": 60},
        {"reliability": 3, "bandwidth": 100, "delay": 60},
        {"reliability": 5, "bandwidth": 100, "delay": 62},
        {"bandwidth": 100, "delay": 108, "ownership": "A"},
        {"reliability": 5, "bandwidth": 100, "delay": 1},
        {"reliability": 3, "bandwidth": 100, "delay": 32},
        {"reliability": 3, "bandwidth": 100, "delay": 110},
        {"reliability": 5, "bandwidth": 100, "ownership": "A"},
        {"reliability": 3, "bandwidth": 100, "delay": 7},
        {"reliability": 5, "bandwidth": 100, "delay": 1},
        {"reliability": 3, "bandwidth": 100, "delay": 10, "ownership": "A"},
        {"reliability": 3, "bandwidth": 100, "delay": 6},
        {"reliability": 5, "bandwidth": 10, "delay": 105}]

    for switch in switches_to_interface_counts.keys():
        switches[switch] = get_switch_mock(switch)

    for key, value in switches_to_interface_counts.items():
        switches[key].interfaces = {}
        for interface in _get_interfaces(value, switches[key]):
            switches[key].interfaces[interface.id] = interface
            interfaces[interface.id] = interface

    for interfaces in links_to_interfaces:
        links[str(i)] = get_link_mock(interfaces[0], interfaces[1])
        links[str(i)].metadata = links_to_metadata[i]
        i += 1

    topology = MagicMock()
    topology.links = links
    topology.switches = switches
    return topology


def _get_interfaces(count, switch):
    '''Add a new interface to the list of interfaces'''
    for i in range(1, count + 1):
        yield get_interface_mock("", i, switch)


test = get_topology_with_metadata_mock()

print(list((i.endpoint_a, i.endpoint_b, i.metadata)
           for i in test.links.values()))

print("---------------------------------")

print(list((j.dpid, list(k.id for k in j.interfaces.values()))
           for j in test.switches.values()))
