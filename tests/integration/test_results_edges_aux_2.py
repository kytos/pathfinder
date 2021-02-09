"""Module to test the KytosGraph in graph.py. Auxiliary Second"""

# module under test
from tests.integration.edges_settings import EdgesSettings


class TestResultsEdgesAux2(EdgesSettings):
    """Tests for the graph class.

    Tests to see if reflexive searches and impossible searches
    show correct results.
    """

    def test_path7_1(self):
        """Tests paths between all users using constrained path algorithm,
        with the delay constraint set to 50, the bandwidth constraint set
        to 100, the reliability constraint set to 3, and the ownership
        constraint set to 'B'
        """
        # delay = 50
        self.assertTrue(self.paths_between_all_users("S1:1", {'delay': 50,
                                                              'bandwidth': 100,
                                                              'ownership': "B"}))

    def test_path7_2(self):
        """Tests paths between all users using constrained path algorithm,
        with the delay constraint set to 50, the bandwidth constraint set
        to 100, the reliability constraint set to 3, and the ownership
        constraint set to 'B'
        """
        # delay = 50
        self.assertTrue(self.paths_between_all_users("S2:1", {'delay': 50,
                                                              'bandwidth': 100,
                                                              'ownership': "B"}))

    def test_path7_3(self):
        """Tests paths between all users using constrained path algorithm,
        with the delay constraint set to 50, the bandwidth constraint set
        to 100, the reliability constraint set to 3, and the ownership
        constraint set to 'B'
        """
        # delay = 50
        self.assertTrue(self.paths_between_all_users("S3:1", {'delay': 50,
                                                              'bandwidth': 100,
                                                              'ownership': "B"}))

    def test_path7_4(self):
        """Tests paths between all users using constrained path algorithm,
        with the delay constraint set to 50, the bandwidth constraint set
        to 100, the reliability constraint set to 3, and the ownership
        constraint set to 'B'
        """
        # delay = 50
        self.assertTrue(self.paths_between_all_users("S5:1", {'delay': 50,
                                                              'bandwidth': 100,
                                                              'ownership': "B"}))

    def test_path7_5(self):
        """Tests paths between all users using constrained path algorithm,
        with the delay constraint set to 50, the bandwidth constraint set
        to 100, the reliability constraint set to 3, and the ownership
        constraint set to 'B'
        """
        # delay = 50
        self.assertTrue(self.paths_between_all_users("S4:2", {'delay': 50,
                                                              'bandwidth': 100,
                                                              'ownership': "B"}))

    def test_path7_6(self):
        """Tests paths between all users using constrained path algorithm,
        with the delay constraint set to 50, the bandwidth constraint set
        to 100, the reliability constraint set to 3, and the ownership
        constraint set to 'B'
        """
        # delay = 50
        self.assertTrue(self.paths_between_all_users("User1:2", {'delay': 50,
                                                                 'bandwidth': 100,
                                                                 'ownership': "B"}))

    def test_path7_7(self):
        """Tests paths between all users using constrained path algorithm,
        with the delay constraint set to 50, the bandwidth constraint set
        to 100, the reliability constraint set to 3, and the ownership
        constraint set to 'B'
        """
        # delay = 50
        self.assertTrue(self.paths_between_all_users("S5:5", {'delay': 50,
                                                              'bandwidth': 100,
                                                              'ownership': "B"}))

    def test_path7_8(self):
        """Tests paths between all users using constrained path algorithm,
        with the delay constraint set to 50, the bandwidth constraint set
        to 100, the reliability constraint set to 3, and the ownership
        constraint set to 'B'
        """
        # delay = 50
        self.assertTrue(self.paths_between_all_users("S8:2", {'delay': 50,
                                                              'bandwidth': 100,
                                                              'ownership': "B"}))

    def test_path7_9(self):
        """Tests paths between all users using constrained path algorithm,
        with the delay constraint set to 50, the bandwidth constraint set
        to 100, the reliability constraint set to 3, and the ownership
        constraint set to 'B'
        """
        # delay = 50
        self.assertTrue(self.paths_between_all_users("S5:6", {'delay': 50,
                                                              'bandwidth': 100,
                                                              'ownership': "B"}))

    def test_path7_1_0(self):
        """Tests paths between all users using constrained path algorithm,
        with the delay constraint set to 50, the bandwidth constraint set
        to 100, the reliability constraint set to 3, and the ownership
        constraint set to 'B'
        """
        # delay = 50
        self.assertTrue(self.paths_between_all_users("User1:3", {'delay': 50,
                                                                 'bandwidth': 100,
                                                                 'ownership': "B"}))

    def test_path7_1_1(self):
        """Tests paths between all users using constrained path algorithm,
        with the delay constraint set to 50, the bandwidth constraint set
        to 100, the reliability constraint set to 3, and the ownership
        constraint set to 'B'
        """
        # delay = 50
        self.assertTrue(self.paths_between_all_users("S6:3", {'delay': 50,
                                                              'bandwidth': 100,
                                                              'ownership': "B"}))

    def test_path7_1_2(self):
        """Tests paths between all users using constrained path algorithm,
        with the delay constraint set to 50, the bandwidth constraint set
        to 100, the reliability constraint set to 3, and the ownership
        constraint set to 'B'
        """
        # delay = 50
        self.assertTrue(self.paths_between_all_users("S9:1", {'delay': 50,
                                                              'bandwidth': 100,
                                                              'ownership': "B"}))

    def test_path7_1_3(self):
        """Tests paths between all users using constrained path algorithm,
        with the delay constraint set to 50, the bandwidth constraint set
        to 100, the reliability constraint set to 3, and the ownership
        constraint set to 'B'
        """
        # delay = 50
        self.assertTrue(self.paths_between_all_users("S6:4", {'delay': 50,
                                                              'bandwidth': 100,
                                                              'ownership': "B"}))

    def test_path7_1_4(self):
        """Tests paths between all users using constrained path algorithm,
        with the delay constraint set to 50, the bandwidth constraint set
        to 100, the reliability constraint set to 3, and the ownership
        constraint set to 'B'
        """
        # delay = 50
        self.assertTrue(self.paths_between_all_users("S9:2", {'delay': 50,
                                                              'bandwidth': 100,
                                                              'ownership': "B"}))

    def test_path7_1_5(self):
        """Tests paths between all users using constrained path algorithm,
        with the delay constraint set to 50, the bandwidth constraint set
        to 100, the reliability constraint set to 3, and the ownership
        constraint set to 'B'
        """
        # delay = 50
        self.assertTrue(self.paths_between_all_users("S6:5", {'delay': 50,
                                                              'bandwidth': 100,
                                                              'ownership': "B"}))

    def test_path7_1_6(self):
        """Tests paths between all users using constrained path algorithm,
        with the delay constraint set to 50, the bandwidth constraint set
        to 100, the reliability constraint set to 3, and the ownership
        constraint set to 'B'
        """
        # delay = 50
        self.assertTrue(self.paths_between_all_users("S10:1", {'delay': 50,
                                                               'bandwidth': 100,
                                                               'ownership': "B"}))

    def test_path7_1_7(self):
        """Tests paths between all users using constrained path algorithm,
        with the delay constraint set to 50, the bandwidth constraint set
        to 100, the reliability constraint set to 3, and the ownership
        constraint set to 'B'
        """
        # delay = 50
        self.assertTrue(self.paths_between_all_users("S8:5", {'delay': 50,
                                                              'bandwidth': 100,
                                                              'ownership': "B"}))

    def test_path7_1_8(self):
        """Tests paths between all users using constrained path algorithm,
        with the delay constraint set to 50, the bandwidth constraint set
        to 100, the reliability constraint set to 3, and the ownership
        constraint set to 'B'
        """
        # delay = 50
        self.assertTrue(self.paths_between_all_users("S9:4", {'delay': 50,
                                                              'bandwidth': 100,
                                                              'ownership': "B"}))

    def test_path7_1_9(self):
        """Tests paths between all users using constrained path algorithm,
        with the delay constraint set to 50, the bandwidth constraint set
        to 100, the reliability constraint set to 3, and the ownership
        constraint set to 'B'
        """
        # delay = 50
        self.assertTrue(self.paths_between_all_users("User1:4", {'delay': 50,
                                                                 'bandwidth': 100,
                                                                 'ownership': "B"}))

    def test_path7_2_0(self):
        """Tests paths between all users using constrained path algorithm,
        with the delay constraint set to 50, the bandwidth constraint set
        to 100, the reliability constraint set to 3, and the ownership
        constraint set to 'B'
        """
        # delay = 50
        self.assertTrue(self.paths_between_all_users("User4:3", {'delay': 50,
                                                                 'bandwidth': 100,
                                                                 'ownership': "B"}))

    def test_path7_2_1(self):
        """Tests paths between all users using constrained path algorithm,
        with the delay constraint set to 50, the bandwidth constraint set
        to 100, the reliability constraint set to 3, and the ownership
        constraint set to 'B'
        """
        # bandwidth = 100
        self.assertTrue(self.paths_between_all_users("S3:1", {'delay': 50,
                                                              'bandwidth': 100,
                                                              'ownership': "B"}))

    def test_path7_2_2(self):
        """Tests paths between all users using constrained path algorithm,
        with the delay constraint set to 50, the bandwidth constraint set
        to 100, the reliability constraint set to 3, and the ownership
        constraint set to 'B'
        """
        # bandwidth = 100
        self.assertTrue(self.paths_between_all_users("S5:1", {'delay': 50,
                                                              'bandwidth': 100,
                                                              'ownership': "B"}))

    def test_path7_2_3(self):
        """Tests paths between all users using constrained path algorithm,
        with the delay constraint set to 50, the bandwidth constraint set
        to 100, the reliability constraint set to 3, and the ownership
        constraint set to 'B'
        """
        # bandwidth = 100
        self.assertTrue(self.paths_between_all_users("User1:4", {'delay': 50,
                                                                 'bandwidth': 100,
                                                                 'ownership': "B"}))

    def test_path7_2_4(self):
        """Tests paths between all users using constrained path algorithm,
        with the delay constraint set to 50, the bandwidth constraint set
        to 100, the reliability constraint set to 3, and the ownership
        constraint set to 'B'
        """
        # bandwidth = 100
        self.assertTrue(self.paths_between_all_users("User4:3", {'delay': 50,
                                                                 'bandwidth': 100,
                                                                 'ownership': "B"}))

    def test_path7_2_5(self):
        """Tests paths between all users using constrained path algorithm,
        with the delay constraint set to 50, the bandwidth constraint set
        to 100, the reliability constraint set to 3, and the ownership
        constraint set to 'B'
        """
        # reliability = 3
        self.assertTrue(self.paths_between_all_users("S4:1", {'delay': 50,
                                                              'bandwidth': 100,
                                                              'ownership': "B"}))

    def test_path7_2_6(self):
        """Tests paths between all users using constrained path algorithm,
        with the delay constraint set to 50, the bandwidth constraint set
        to 100, the reliability constraint set to 3, and the ownership
        constraint set to 'B'
        """
        # reliability = 3
        self.assertTrue(self.paths_between_all_users("S5:2", {'delay': 50,
                                                              'bandwidth': 100,
                                                              'ownership': "B"}))

    def test_path7_2_7(self):
        """Tests paths between all users using constrained path algorithm,
        with the delay constraint set to 50, the bandwidth constraint set
        to 100, the reliability constraint set to 3, and the ownership
        constraint set to 'B'
        """
        # reliability = 3
        self.assertTrue(self.paths_between_all_users("S5:3", {'delay': 50,
                                                              'bandwidth': 100,
                                                              'ownership': "B"}))

    def test_path7_2_8(self):
        """Tests paths between all users using constrained path algorithm,
        with the delay constraint set to 50, the bandwidth constraint set
        to 100, the reliability constraint set to 3, and the ownership
        constraint set to 'B'
        """
        # reliability = 3
        self.assertTrue(self.paths_between_all_users("S6:1", {'delay': 50,
                                                              'bandwidth': 100,
                                                              'ownership': "B"}))

    def test_path7_2_9(self):
        """Tests paths between all users using constrained path algorithm,
        with the delay constraint set to 50, the bandwidth constraint set
        to 100, the reliability constraint set to 3, and the ownership
        constraint set to 'B'
        """
        # ownership = "B"
        self.assertTrue(self.paths_between_all_users("S4:1", {'delay': 50,
                                                              'bandwidth': 100,
                                                              'ownership': "B"}))

    def test_path7_3_0(self):
        """Tests paths between all users using constrained path algorithm,
        with the delay constraint set to 50, the bandwidth constraint set
        to 100, the reliability constraint set to 3, and the ownership
        constraint set to 'B'
        """
        # ownership = "B"
        self.assertTrue(self.paths_between_all_users("S5:2", {'delay': 50,
                                                              'bandwidth': 100,
                                                              'ownership': "B"}))

    def test_path7_3_1(self):
        """Tests paths between all users using constrained path algorithm,
        with the delay constraint set to 50, the bandwidth constraint set
        to 100, the reliability constraint set to 3, and the ownership
        constraint set to 'B'
        """
        # ownership = "B"
        self.assertTrue(self.paths_between_all_users("S4:2", {'delay': 50,
                                                              'bandwidth': 100,
                                                              'ownership': "B"}))

    def test_path7_3_2(self):
        """Tests paths between all users using constrained path algorithm,
        with the delay constraint set to 50, the bandwidth constraint set
        to 100, the reliability constraint set to 3, and the ownership
        constraint set to 'B'
        """
        # ownership = "B"
        self.assertTrue(self.paths_between_all_users("User1:2", {'delay': 50,
                                                                 'bandwidth': 100,
                                                                 'ownership': "B"}))

    def test_path7_3_3(self):
        """Tests paths between all users using constrained path algorithm,
        with the delay constraint set to 50, the bandwidth constraint set
        to 100, the reliability constraint set to 3, and the ownership
        constraint set to 'B'
        """
        # ownership = "B"
        self.assertTrue(self.paths_between_all_users("S5:4", {'delay': 50,
                                                              'bandwidth': 100,
                                                              'ownership': "B"}))

    def test_path7_3_4(self):
        """Tests paths between all users using constrained path algorithm,
        with the delay constraint set to 50, the bandwidth constraint set
        to 100, the reliability constraint set to 3, and the ownership
        constraint set to 'B'
        """
        # ownership = "B"
        self.assertTrue(self.paths_between_all_users("S6:2", {'delay': 50,
                                                              'bandwidth': 100,
                                                              'ownership': "B"}))

    def test_path7_3_5(self):
        """Tests paths between all users using constrained path algorithm,
        with the delay constraint set to 50, the bandwidth constraint set
        to 100, the reliability constraint set to 3, and the ownership
        constraint set to 'B'
        """
        # ownership = "B"
        self.assertTrue(self.paths_between_all_users("S6:5", {'delay': 50,
                                                              'bandwidth': 100,
                                                              'ownership': "B"}))

    def test_path7_3_6(self):
        """Tests paths between all users using constrained path algorithm,
        with the delay constraint set to 50, the bandwidth constraint set
        to 100, the reliability constraint set to 3, and the ownership
        constraint set to 'B'
        """
        # ownership = "B"
        self.assertTrue(self.paths_between_all_users("S10:1", {'delay': 50,
                                                               'bandwidth': 100,
                                                               'ownership': "B"}))

    def test_path7_3_7(self):
        """Tests paths between all users using constrained path algorithm,
        with the delay constraint set to 50, the bandwidth constraint set
        to 100, the reliability constraint set to 3, and the ownership
        constraint set to 'B'
        """
        # ownership = "B"
        self.assertTrue(self.paths_between_all_users("S8:6", {'delay': 50,
                                                              'bandwidth': 100,
                                                              'ownership': "B"}))

    def test_path7_3_8(self):
        """Tests paths between all users using constrained path algorithm,
        with the delay constraint set to 50, the bandwidth constraint set
        to 100, the reliability constraint set to 3, and the ownership
        constraint set to 'B'
        """
        # ownership = "B"
        self.assertTrue(self.paths_between_all_users("S10:2", {'delay': 50,
                                                               'bandwidth': 100,
                                                               'ownership': "B"}))

    def test_path7_3_9(self):
        """Tests paths between all users using constrained path algorithm,
        with the delay constraint set to 50, the bandwidth constraint set
        to 100, the reliability constraint set to 3, and the ownership
        constraint set to 'B'
        """
        # ownership = "B"
        self.assertTrue(self.paths_between_all_users("S10:3", {'delay': 50,
                                                               'bandwidth': 100,
                                                               'ownership': "B"}))

    def test_path7_4_0(self):
        """Tests paths between all users using constrained path algorithm,
        with the delay constraint set to 50, the bandwidth constraint set
        to 100, the reliability constraint set to 3, and the ownership
        constraint set to 'B'
        """
        # ownership = "B"
        self.assertTrue(self.paths_between_all_users("User2:1", {'delay': 50,
                                                                 'bandwidth': 100,
                                                                 'ownership': "B"}))
