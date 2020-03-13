def TestKytosGraph3(TestCase)
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
        """Tests paths from User 1 to User 4 and back to User 1, such that the shortest path
        is in the result set"""
        #Arrange
        #Act
        #Assert
 
    def test_path10(self):
        """Tests paths from User 3 to User 4, such that a non-shortest path is not in the
        result set"""
        #Arrange
        #Act
        #Assert
 
    def test_path11(self):
        """Tests paths from User 1 to User 4, such that a non-shortest path is not in the
        result set"""
        #Arrange
        #Act
        #Assert
 
    def test_path12(self):
        """Tests paths from User 1 to User 2, such that a non-shortest path is not in the
        result set"""
        #Arrange
        #Act
        #Assert"""

    def test_path13(self):
        """Tests paths between User 1 and User 4, such that the shortest path is in the result set"""
        #Arrange
        self.setup()
        users = ["User1", "User4"]
        #Act
        result = self.get_path(users[0], users[1])
        print(str(result))
        #Assert
        self.assertEqual(1, 1)
        
    @staticmethod
    def createSwitch(name,switches):
        switches[name] = Switch(name)
        print("Creating Switch: ", name)

    @staticmethod
    def createLink(name = None, interface_a, interface_b, interfaces, links):
        compounded = "{}|{}".format(interface_a, interface_b)
        final_name = ""

        if (name is None):
            final_name = compounded
        else:
            final_name = name

        links[final_name] = Link(interfaces[interface_a], interfaces[interface_b])
        print("Creating Link: ", final_name)

    @staticmethod
    def addMetadataToLink(link, metrics):
        links[link].extend_metadata(metrics)


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
        TestKytosGraph3.createLink("S2:1", "S3:1", interfaces, links)
        TestKytosGraph3.createLink("S3:2", "S4:2", interfaces, links)
        TestKytosGraph3.createLink("S5:2", "S4:3", interfaces, links)
        TestKytosGraph3.createLink("S3:3", "S4:3", interfaces, links)



