"""Module to test the KytosGraph in graph.py. Auxiliary"""

# module under test
from tests.integration.edges_settings import EdgesSettings


class TestResultsEdgesAux(EdgesSettings):
    """Tests for the graph class.

    Tests to see if reflexive searches and impossible searches
    show correct results.
    """

    def test_path6_1(self):
        """Tests paths between all users using constrained path algorithm,
        with the delay constraint set to 50.
        """
        self.assertTrue(self.paths_between_all_users("S1:1", {'delay': 50}))

    def test_path6_2(self):
        """Tests paths between all users using constrained path algorithm,
        with the delay constraint set to 50.
        """
        self.assertTrue(self.paths_between_all_users("S2:1", {'delay': 50}))

    def test_path6_3(self):
        """Tests paths between all users using constrained path algorithm,
        with the delay constraint set to 50.
        """
        self.assertTrue(self.paths_between_all_users("S3:1", {'delay': 50}))

    def test_path6_4(self):
        """Tests paths between all users using constrained path algorithm,
        with the delay constraint set to 50.
        """
        self.assertTrue(self.paths_between_all_users("S5:1", {'delay': 50}))

    def test_path6_5(self):
        """Tests paths between all users using constrained path algorithm,
        with the delay constraint set to 50.
        """
        self.assertTrue(self.paths_between_all_users("S4:2", {'delay': 50}))

    def test_path6_6(self):
        """Tests paths between all users using constrained path algorithm,
        with the delay constraint set to 50.
        """
        self.assertTrue(self.paths_between_all_users("User1:2", {'delay': 50}))

    def test_path6_7(self):
        """Tests paths between all users using constrained path algorithm,
        with the delay constraint set to 50.
        """
        self.assertTrue(self.paths_between_all_users("S5:5", {'delay': 50}))

    def test_path6_8(self):
        """Tests paths between all users using constrained path algorithm,
        with the delay constraint set to 50.
        """
        self.assertTrue(self.paths_between_all_users("S8:2", {'delay': 50}))

    def test_path6_9(self):
        """Tests paths between all users using constrained path algorithm,
        with the delay constraint set to 50.
        """
        self.assertTrue(self.paths_between_all_users("S5:6", {'delay': 50}))

    def test_path6_1_0(self):
        """Tests paths between all users using constrained path algorithm,
        with the delay constraint set to 50.
        """
        self.assertTrue(self.paths_between_all_users("User1:3", {'delay': 50}))

    def test_path6_1_1(self):
        """Tests paths between all users using constrained path algorithm,
        with the delay constraint set to 50.
        """
        self.assertTrue(self.paths_between_all_users("S6:3", {'delay': 50}))

    def test_path6_1_2(self):
        """Tests paths between all users using constrained path algorithm,
        with the delay constraint set to 50.
        """
        self.assertTrue(self.paths_between_all_users("S9:1", {'delay': 50}))

    def test_path6_1_3(self):
        """Tests paths between all users using constrained path algorithm,
        with the delay constraint set to 50.
        """
        self.assertTrue(self.paths_between_all_users("S6:4", {'delay': 50}))

    def test_path6_1_4(self):
        """Tests paths between all users using constrained path algorithm,
        with the delay constraint set to 50.
        """
        self.assertTrue(self.paths_between_all_users("S9:2", {'delay': 50}))

    def test_path6_1_5(self):
        """Tests paths between all users using constrained path algorithm,
        with the delay constraint set to 50.
        """
        self.assertTrue(self.paths_between_all_users("S6:5", {'delay': 50}))

    def test_path6_1_6(self):
        """Tests paths between all users using constrained path algorithm,
        with the delay constraint set to 50.
        """
        self.assertTrue(self.paths_between_all_users("S6:5", {'delay': 50}))

    def test_path6_1_7(self):
        """Tests paths between all users using constrained path algorithm,
        with the delay constraint set to 50.
        """
        self.assertTrue(self.paths_between_all_users("S10:1", {'delay': 50}))

    def test_path6_1_8(self):
        """Tests paths between all users using constrained path algorithm,
        with the delay constraint set to 50.
        """
        self.assertTrue(self.paths_between_all_users("S8:5", {'delay': 50}))

    def test_path6_1_9(self):
        """Tests paths between all users using constrained path algorithm,
        with the delay constraint set to 50.
        """
        self.assertTrue(self.paths_between_all_users("S9:4", {'delay': 50}))

    def test_path6_2_0(self):
        """Tests paths between all users using constrained path algorithm,
        with the delay constraint set to 50.
        """
        self.assertTrue(self.paths_between_all_users("User1:4", {'delay': 50}))

    def test_path6_2_1(self):
        """Tests paths between all users using constrained path algorithm,
        with the delay constraint set to 50.
        """
        self.assertTrue(self.paths_between_all_users("User4:3", {'delay': 50}))
