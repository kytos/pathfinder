"""Module to test the KytosGraph in graph.py."""

from tests.integration.metadata_settings import MetadataSettings


class TestPathsMetadata(MetadataSettings):
    """Tests for the graph class.

    Tests if the metadata in search paths edges have passing values.
    """

    def test_path_constrained_user_user_k1(self):
        """Test if there is a constrained path between User - User."""
        self.initializer()

        source = "User1"
        destination = "User2"
        paths = self.graph.constrained_k_shortest_paths(
            source, destination, k=1
        )
        assert len(paths) == 1

        for path in paths:
            assert path["hops"][0] == source
            assert path["hops"][-1] == destination

    def test_path_constrained_user_user_k2(self):
        """Test if there are two constrained path between User - User."""
        self.initializer()

        source = "User1"
        destination = "User2"
        paths = self.graph.constrained_k_shortest_paths(
            source, destination, k=2
        )
        assert len(paths) == 2

        for path in paths:
            assert path["hops"][0] == source
            assert path["hops"][-1] == destination

    def test_path_constrained_user_user_k4(self):
        """Test if there are four constrained path between User - User."""
        self.initializer()

        source = "User1"
        destination = "User2"
        paths = self.graph.constrained_k_shortest_paths(
            source, destination, k=4
        )
        assert len(paths) == 4

        for path in paths:
            assert path["hops"][0] == source
            assert path["hops"][-1] == destination

    def test_path_constrained_user_switch(self):
        """Test if there is a constrained
        path between User - Switch."""
        self.initializer()

        source = "User1"
        destination = "S4"
        paths = self.graph.constrained_k_shortest_paths(source, destination)
        assert paths

        for path in paths:
            assert path["hops"][0] == source
            assert path["hops"][-1] == destination

    def test_path_constrained_switch_switch(self):
        """Test if there is a constrained
        path between Switch - Switch."""
        self.initializer()

        source = "S2"
        destination = "S4"
        paths = self.graph.constrained_k_shortest_paths(source, destination)
        assert paths

        for path in paths:
            assert path["hops"][0] == source
            assert path["hops"][-1] == destination

    def test_no_path_constrained_user_user(self):
        """Test if there is NOT a constrained
        path between User - User."""
        self.initializer()
        paths = self.graph.constrained_k_shortest_paths("User1", "User3")
        assert not paths

    def test_path_constrained_user_user_t1(self):
        """Test if there is a constrained path between
        User - User using the 2nd topology variant."""
        self.initializer(val=1)

        source = "User1"
        destination = "User3"
        paths = self.graph.constrained_k_shortest_paths(source, destination)
        assert paths

        for path in paths:
            assert path["hops"][0] == source
            assert path["hops"][-1] == destination

    def test_no_path_constrained_user_user_t1(self):
        """Test if there is NOT a constrained path between
        User - User using the 2nd topology variant."""
        self.initializer(val=1)
        paths = self.graph.constrained_k_shortest_paths("User1", "User2")
        assert not paths

    def test_no_path_constrained_switch_switch_t1(self):
        """Test if there is NOT a constrained path between
        Switch - Switch using the 2nd topology variant."""
        self.initializer(val=1)
        paths = self.graph.constrained_k_shortest_paths("S1", "S2")
        assert not paths

    def test_path_constrained_user_user_t2(self):
        """Test if there is a constrained path between
        User - User using the 3rd topology variant."""
        self.initializer(val=2)

        source = "User1"
        destination = "User2"
        paths = self.graph.constrained_k_shortest_paths(source, destination)
        assert paths

        for path in paths:
            assert path["hops"][0] == source
            assert path["hops"][-1] == destination

    def test_path_constrained_user_switch_t2(self):
        """Test if there is a constrained path between
        User - Switch using the 3rd topology variant."""
        self.initializer(val=2)

        source = "User1"
        destination = "S4"
        paths = self.graph.constrained_k_shortest_paths(source, destination)
        assert paths

        for path in paths:
            assert path["hops"][0] == source
            assert path["hops"][-1] == destination
        paths = self.graph.constrained_k_shortest_paths("User1", "S4")

    def test_path_constrained_switch_switch_t2(self):
        """Test if there is a constrained path between
        two switches using the 3rd topology variant."""
        self.initializer(val=2)

        source = "S2"
        destination = "S4"
        paths = self.graph.constrained_k_shortest_paths(source, destination)
        assert paths

        for path in paths:
            assert path["hops"][0] == source
            assert path["hops"][-1] == destination

    def test_path_constrained_reliability(self):
        """Tests if the edges used in the paths
        of the paths set do not have poor reliability
        """
        requirements = {"reliability": 3}

        self.initializer()

        source = "User1"
        destination = "User2"
        paths = self.graph.constrained_k_shortest_paths(
            source, destination, mandatory_metrics=requirements
        )
        assert paths

        for path in paths:
            assert path["hops"][0] == source
            assert path["hops"][-1] == destination

    def test_cspf_with_multiple_owners(self):
        """Tests if the edges with multiple owners"""

        owners = ("B", "C")
        owners_paths = []
        for owner in owners:
            requirements = {"ownership": owner}

            self.initializer()

            source = "User1"
            destination = "User2"
            paths = self.graph.constrained_k_shortest_paths(
                source, destination, mandatory_metrics=requirements, k=1
            )
            assert paths
            assert paths[0]["hops"][0] == source
            assert paths[0]["hops"][-1] == destination
            assert paths[0]["metrics"] == requirements
            owners_paths.append(paths[0]["hops"])
        assert owners_paths[0] == owners_paths[1]

    def test_no_path_constrained_reliability(self):
        """Tests if the edges used in the paths
        of the paths set do not have poor reliability
        """
        requirements = {"reliability": 1}

        self.initializer()

        paths = self.graph.constrained_k_shortest_paths(
            "User1", "User3", mandatory_metrics=requirements
        )
        assert not paths

    def test_path_constrained_reliability_detailed(self):
        """Tests if the edges used in the paths
        of the paths set do not have poor reliability
        """
        reliabilities = []
        requirements = {"reliability": 3}
        poor_reliability = 1

        self.initializer()

        paths = self.graph.constrained_k_shortest_paths(
            "User1", "User2", mandatory_metrics=requirements
        )

        if paths:
            for path in paths[0]["hops"]:
                for i in range(1, len(path)):
                    endpoint_a = path[i - 1]
                    endpoint_b = path[i]
                    meta_data = self.graph.get_link_metadata(
                        endpoint_a, endpoint_b
                    )
                    if meta_data and "reliability" in meta_data.keys():
                        reliabilities.append(meta_data["reliability"])

            self.assertNotIn(poor_reliability, reliabilities)

        else:
            self.assertNotEqual(paths, [])

    def test_path_constrained_delay(self):
        """Tests if the edges used in the paths
        from User 1 to User 2 have less than 30 delay.
        """
        delays = []
        requirements = {"delay": 29}

        self.initializer()

        paths = self.graph.constrained_k_shortest_paths(
            "User1", "User2", mandatory_metrics=requirements
        )
        assert paths

        for path in paths:
            for i, j in zip(
                range(0, len(path["hops"])), range(1, len(path["hops"]))
            ):
                endpoint_a = path["hops"][i]
                endpoint_b = path["hops"][j]
                meta_data = self.graph.get_link_metadata(
                    endpoint_a, endpoint_b
                )
                if meta_data and "delay" in meta_data.keys():
                    delays.append(meta_data["delay"])

        assert delays
        for delay in delays:
            assert delay <= requirements["delay"]

    def links_metadata_values(self, path, attr):
        """Method to build a list of metadata values of the links of a path"""
        values = []
        for i, j in zip(
            range(0, len(path["hops"])), range(1, len(path["hops"]))
        ):
            endpoint_a = path["hops"][i]
            endpoint_b = path["hops"][j]
            meta_data = self.graph.get_link_metadata(endpoint_a, endpoint_b)
            if meta_data and attr in meta_data.keys():
                values.append(meta_data[attr])
        return values

    def test_path_constrained_bandwidth_detailed(self):
        """Tests if the edges used in the paths
        from User 1 to User 2 have at least 20 bandwidth.
        """
        requirements = {"bandwidth": 20}

        self.initializer()

        paths = self.graph.constrained_k_shortest_paths(
            "User1", "User2", mandatory_metrics=requirements
        )
        assert paths

        for path in paths:
            bandwidths = self.links_metadata_values(path, "bandwidth")
            assert bandwidths

            for bandwidth in bandwidths:
                assert bandwidth >= requirements["bandwidth"]

    def test_path_constrained_bandwidth_detailed_t2(self):
        """Tests if the edges used in the paths
        from User 1 to User 2 have at least 20 bandwidth.
        """
        requirements = {"bandwidth": 20}

        self.initializer(val=2)

        paths = self.graph.constrained_k_shortest_paths(
            "User1", "User2", mandatory_metrics=requirements
        )
        assert paths

        for path in paths:
            bandwidths = self.links_metadata_values(path, "bandwidth")
            assert bandwidths
            for bandwidth in bandwidths:
                assert bandwidth >= requirements["bandwidth"]

    def test_path_constrained_bandwidth_delay(self):
        """Tests if the edges used in the paths from User 1
        to User 2 have at least 20 bandwidth and under 30 delay.
        """
        requirements = {"bandwidth": 20, "delay": 29}

        self.initializer()

        paths = self.graph.constrained_k_shortest_paths(
            "User1", "User2", mandatory_metrics=requirements
        )
        assert paths

        for path in paths:

            bandwidths = self.links_metadata_values(path, "bandwidth")
            assert bandwidths
            for bandwidth in bandwidths:
                assert bandwidth >= requirements["bandwidth"]

            delays = self.links_metadata_values(path, "delay")
            assert delays
            for delay in delays:
                assert delay <= requirements["delay"]

            assert len(bandwidths) == len(delays)
