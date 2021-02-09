"""Module to test the KytosGraph in graph.py. Auxiliary Third"""

# module under test
from tests.integration.edges_settings import EdgesSettings


class TestResultsEdgesAux3(EdgesSettings):
    """Tests for the graph class.

    Tests to see if reflexive searches and impossible searches
    show correct results.
    """

    def test_path8_1(self):
        """Tests paths between all users using constrained path algorithm,
        with the delay constraint set to 50, the bandwidth constraint
        set to 100, the reliability constraint set to 3, and the ownership
        constraint set to 'B'

        Tests conducted with flexibility enabled
        """
        # delay = 50
        self.assertTrue(self.paths_between_all_users("S1:1", flexible={'delay': 50,
                                                                       'bandwidth': 100,
                                                                       'reliability': 3,
                                                                       'ownership': "B"},
                                                     metrics='delay'))

    def test_path8_2(self):
        """Tests paths between all users using constrained path algorithm,
        with the delay constraint set to 50, the bandwidth constraint
        set to 100, the reliability constraint set to 3, and the ownership
        constraint set to 'B'

        Tests conducted with flexibility enabled
        """
        # delay = 50
        self.assertTrue(self.paths_between_all_users("S2:1", flexible={'delay': 50,
                                                                       'bandwidth': 100,
                                                                       'reliability': 3,
                                                                       'ownership': "B"},
                                                     metrics='delay'))

    def test_path8_3(self):
        """Tests paths between all users using constrained path algorithm,
        with the delay constraint set to 50, the bandwidth constraint
        set to 100, the reliability constraint set to 3, and the ownership
        constraint set to 'B'

        Tests conducted with flexibility enabled
        """
        # delay = 50
        self.assertTrue(self.paths_between_all_users("S3:1", flexible={'delay': 50,
                                                                       'bandwidth': 100,
                                                                       'reliability': 3,
                                                                       'ownership': "B"},
                                                     metrics='delay'))

    def test_path8_4(self):
        """Tests paths between all users using constrained path algorithm,
        with the delay constraint set to 50, the bandwidth constraint
        set to 100, the reliability constraint set to 3, and the ownership
        constraint set to 'B'

        Tests conducted with flexibility enabled
        """
        # delay = 50
        self.assertTrue(self.paths_between_all_users("S5:1", flexible={'delay': 50,
                                                                       'bandwidth': 100,
                                                                       'reliability': 3,
                                                                       'ownership': "B"},
                                                     metrics='delay'))

    def test_path8_5(self):
        """Tests paths between all users using constrained path algorithm,
        with the delay constraint set to 50, the bandwidth constraint
        set to 100, the reliability constraint set to 3, and the ownership
        constraint set to 'B'

        Tests conducted with flexibility enabled
        """
        # delay = 50
        self.assertTrue(self.paths_between_all_users("S4:2", flexible={'delay': 50,
                                                                       'bandwidth': 100,
                                                                       'reliability': 3,
                                                                       'ownership': "B"},
                                                     metrics='delay'))

    def test_path8_6(self):
        """Tests paths between all users using constrained path algorithm,
        with the delay constraint set to 50, the bandwidth constraint
        set to 100, the reliability constraint set to 3, and the ownership
        constraint set to 'B'

        Tests conducted with flexibility enabled
        """
        # delay = 50
        self.assertTrue(self.paths_between_all_users("User1:2", flexible={'delay': 50,
                                                                          'bandwidth': 100,
                                                                          'reliability': 3,
                                                                          'ownership': "B"},
                                                     metrics='delay'))

    def test_path8_7(self):
        """Tests paths between all users using constrained path algorithm,
        with the delay constraint set to 50, the bandwidth constraint
        set to 100, the reliability constraint set to 3, and the ownership
        constraint set to 'B'

        Tests conducted with flexibility enabled
        """
        # delay = 50
        self.assertTrue(self.paths_between_all_users("S5:5", flexible={'delay': 50,
                                                                       'bandwidth': 100,
                                                                       'reliability': 3,
                                                                       'ownership': "B"},
                                                     metrics='delay'))

    def test_path8_8(self):
        """Tests paths between all users using constrained path algorithm,
        with the delay constraint set to 50, the bandwidth constraint
        set to 100, the reliability constraint set to 3, and the ownership
        constraint set to 'B'

        Tests conducted with flexibility enabled
        """
        # delay = 50
        self.assertTrue(self.paths_between_all_users("S8:2", flexible={'delay': 50,
                                                                       'bandwidth': 100,
                                                                       'reliability': 3,
                                                                       'ownership': "B"},
                                                     metrics='delay'))

    def test_path8_9(self):
        """Tests paths between all users using constrained path algorithm,
        with the delay constraint set to 50, the bandwidth constraint
        set to 100, the reliability constraint set to 3, and the ownership
        constraint set to 'B'

        Tests conducted with flexibility enabled
        """
        # delay = 50
        self.assertTrue(self.paths_between_all_users("S5:6", flexible={'delay': 50,
                                                                       'bandwidth': 100,
                                                                       'reliability': 3,
                                                                       'ownership': "B"},
                                                     metrics='delay'))

    def test_path8_1_0(self):
        """Tests paths between all users using constrained path algorithm,
        with the delay constraint set to 50, the bandwidth constraint
        set to 100, the reliability constraint set to 3, and the ownership
        constraint set to 'B'

        Tests conducted with flexibility enabled
        """
        # delay = 50
        self.assertTrue(self.paths_between_all_users("User1:3", flexible={'delay': 50,
                                                                          'bandwidth': 100,
                                                                          'reliability': 3,
                                                                          'ownership': "B"},
                                                     metrics='delay'))

    def test_path8_1_1(self):
        """Tests paths between all users using constrained path algorithm,
        with the delay constraint set to 50, the bandwidth constraint
        set to 100, the reliability constraint set to 3, and the ownership
        constraint set to 'B'

        Tests conducted with flexibility enabled
        """
        # delay = 50
        self.assertTrue(self.paths_between_all_users("S6:3", flexible={'delay': 50,
                                                                       'bandwidth': 100,
                                                                       'reliability': 3,
                                                                       'ownership': "B"},
                                                     metrics='delay'))

    def test_path8_1_2(self):
        """Tests paths between all users using constrained path algorithm,
        with the delay constraint set to 50, the bandwidth constraint
        set to 100, the reliability constraint set to 3, and the ownership
        constraint set to 'B'

        Tests conducted with flexibility enabled
        """
        # delay = 50
        self.assertTrue(self.paths_between_all_users("S9:1", flexible={'delay': 50,
                                                                       'bandwidth': 100,
                                                                       'reliability': 3,
                                                                       'ownership': "B"},
                                                     metrics='delay'))

    def test_path8_1_3(self):
        """Tests paths between all users using constrained path algorithm,
        with the delay constraint set to 50, the bandwidth constraint
        set to 100, the reliability constraint set to 3, and the ownership
        constraint set to 'B'

        Tests conducted with flexibility enabled
        """
        # delay = 50
        self.assertTrue(self.paths_between_all_users("S6:4", flexible={'delay': 50,
                                                                       'bandwidth': 100,
                                                                       'reliability': 3,
                                                                       'ownership': "B"},
                                                     metrics='delay'))

    def test_path8_1_4(self):
        """Tests paths between all users using constrained path algorithm,
        with the delay constraint set to 50, the bandwidth constraint
        set to 100, the reliability constraint set to 3, and the ownership
        constraint set to 'B'

        Tests conducted with flexibility enabled
        """
        # delay = 50
        self.assertTrue(self.paths_between_all_users("S9:2", flexible={'delay': 50,
                                                                       'bandwidth': 100,
                                                                       'reliability': 3,
                                                                       'ownership': "B"},
                                                     metrics='delay'))

    def test_path8_1_5(self):
        """Tests paths between all users using constrained path algorithm,
        with the delay constraint set to 50, the bandwidth constraint
        set to 100, the reliability constraint set to 3, and the ownership
        constraint set to 'B'

        Tests conducted with flexibility enabled
        """
        # delay = 50
        self.assertTrue(self.paths_between_all_users("S6:5", flexible={'delay': 50,
                                                                       'bandwidth': 100,
                                                                       'reliability': 3,
                                                                       'ownership': "B"},
                                                     metrics='delay'))

    def test_path8_1_6(self):
        """Tests paths between all users using constrained path algorithm,
        with the delay constraint set to 50, the bandwidth constraint
        set to 100, the reliability constraint set to 3, and the ownership
        constraint set to 'B'

        Tests conducted with flexibility enabled
        """
        # delay = 50
        self.assertTrue(self.paths_between_all_users("S10:1", flexible={'delay': 50,
                                                                        'bandwidth': 100,
                                                                        'reliability': 3,
                                                                        'ownership': "B"},
                                                     metrics='delay'))

    def test_path8_1_7(self):
        """Tests paths between all users using constrained path algorithm,
        with the delay constraint set to 50, the bandwidth constraint
        set to 100, the reliability constraint set to 3, and the ownership
        constraint set to 'B'

        Tests conducted with flexibility enabled
        """
        # delay = 50
        self.assertTrue(self.paths_between_all_users("S8:5", flexible={'delay': 50,
                                                                       'bandwidth': 100,
                                                                       'reliability': 3,
                                                                       'ownership': "B"},
                                                     metrics='delay'))

    def test_path8_1_8(self):
        """Tests paths between all users using constrained path algorithm,
        with the delay constraint set to 50, the bandwidth constraint
        set to 100, the reliability constraint set to 3, and the ownership
        constraint set to 'B'

        Tests conducted with flexibility enabled
        """
        # delay = 50
        self.assertTrue(self.paths_between_all_users("S9:4", flexible={'delay': 50,
                                                                       'bandwidth': 100,
                                                                       'reliability': 3,
                                                                       'ownership': "B"},
                                                     metrics='delay'))

    def test_path8_1_9(self):
        """Tests paths between all users using constrained path algorithm,
        with the delay constraint set to 50, the bandwidth constraint
        set to 100, the reliability constraint set to 3, and the ownership
        constraint set to 'B'

        Tests conducted with flexibility enabled
        """
        # delay = 50
        self.assertTrue(self.paths_between_all_users("User1:4", flexible={'delay': 50,
                                                                          'bandwidth': 100,
                                                                          'reliability': 3,
                                                                          'ownership': "B"},
                                                     metrics='delay'))

    def test_path8_2_0(self):
        """Tests paths between all users using constrained path algorithm,
        with the delay constraint set to 50, the bandwidth constraint
        set to 100, the reliability constraint set to 3, and the ownership
        constraint set to 'B'

        Tests conducted with flexibility enabled
        """
        # delay = 50
        self.assertTrue(self.paths_between_all_users("User4:3", flexible={'delay': 50,
                                                                          'bandwidth': 100,
                                                                          'reliability': 3,
                                                                          'ownership': "B"},
                                                     metrics='delay'))

    def test_path8_2_1(self):
        """Tests paths between all users using constrained path algorithm,
        with the delay constraint set to 50, the bandwidth constraint
        set to 100, the reliability constraint set to 3, and the ownership
        constraint set to 'B'

        Tests conducted with flexibility enabled
        """
        # bandwidth = 100
        self.assertTrue(self.paths_between_all_users("S3:1", flexible={'delay': 50,
                                                                       'bandwidth': 100,
                                                                       'reliability': 3,
                                                                       'ownership': "B"},
                                                     metrics='bandwidth'))

    def test_path8_2_2(self):
        """Tests paths between all users using constrained path algorithm,
        with the delay constraint set to 50, the bandwidth constraint
        set to 100, the reliability constraint set to 3, and the ownership
        constraint set to 'B'

        Tests conducted with flexibility enabled
        """
        # bandwidth = 100
        self.assertTrue(self.paths_between_all_users("S5:1", flexible={'delay': 50,
                                                                       'bandwidth': 100,
                                                                       'reliability': 3,
                                                                       'ownership': "B"},
                                                     metrics='bandwidth'))

    def test_path8_2_3(self):
        """Tests paths between all users using constrained path algorithm,
        with the delay constraint set to 50, the bandwidth constraint
        set to 100, the reliability constraint set to 3, and the ownership
        constraint set to 'B'

        Tests conducted with flexibility enabled
        """
        # bandwidth = 100
        self.assertTrue(self.paths_between_all_users("User1:4", flexible={'delay': 50,
                                                                          'bandwidth': 100,
                                                                          'reliability': 3,
                                                                          'ownership': "B"},
                                                     metrics='bandwidth'))

    def test_path8_2_4(self):
        """Tests paths between all users using constrained path algorithm,
        with the delay constraint set to 50, the bandwidth constraint
        set to 100, the reliability constraint set to 3, and the ownership
        constraint set to 'B'

        Tests conducted with flexibility enabled
        """
        # bandwidth = 100
        self.assertTrue(self.paths_between_all_users("User4:3", flexible={'delay': 50,
                                                                          'bandwidth': 100,
                                                                          'reliability': 3,
                                                                          'ownership': "B"},
                                                     metrics='bandwidth'))

    def test_path8_2_5(self):
        """Tests paths between all users using constrained path algorithm,
        with the delay constraint set to 50, the bandwidth constraint
        set to 100, the reliability constraint set to 3, and the ownership
        constraint set to 'B'

        Tests conducted with flexibility enabled
        """
        # reliability = 3
        self.assertTrue(self.paths_between_all_users("S4:1", flexible={'delay': 50,
                                                                       'bandwidth': 100,
                                                                       'reliability': 3,
                                                                       'ownership': "B"},
                                                     metrics='reliability'))

    def test_path8_2_6(self):
        """Tests paths between all users using constrained path algorithm,
        with the delay constraint set to 50, the bandwidth constraint
        set to 100, the reliability constraint set to 3, and the ownership
        constraint set to 'B'

        Tests conducted with flexibility enabled
        """
        # reliability = 3
        self.assertTrue(self.paths_between_all_users("S5:2", flexible={'delay': 50,
                                                                       'bandwidth': 100,
                                                                       'reliability': 3,
                                                                       'ownership': "B"},
                                                     metrics='reliability'))

    def test_path8_2_7(self):
        """Tests paths between all users using constrained path algorithm,
        with the delay constraint set to 50, the bandwidth constraint
        set to 100, the reliability constraint set to 3, and the ownership
        constraint set to 'B'

        Tests conducted with flexibility enabled
        """
        # reliability = 3
        self.assertTrue(self.paths_between_all_users("S5:3", flexible={'delay': 50,
                                                                       'bandwidth': 100,
                                                                       'reliability': 3,
                                                                       'ownership': "B"},
                                                     metrics='reliability'))

    def test_path8_2_8(self):
        """Tests paths between all users using constrained path algorithm,
        with the delay constraint set to 50, the bandwidth constraint
        set to 100, the reliability constraint set to 3, and the ownership
        constraint set to 'B'

        Tests conducted with flexibility enabled
        """
        # reliability = 3
        self.assertTrue(self.paths_between_all_users("S6:1", flexible={'delay': 50,
                                                                       'bandwidth': 100,
                                                                       'reliability': 3,
                                                                       'ownership': "B"},
                                                     metrics='reliability'))

    def test_path8_2_9(self):
        """Tests paths between all users using constrained path algorithm,
        with the delay constraint set to 50, the bandwidth constraint
        set to 100, the reliability constraint set to 3, and the ownership
        constraint set to 'B'

        Tests conducted with flexibility enabled
        """
        # ownership = "B"
        self.assertTrue(self.paths_between_all_users("S4:1", flexible={'delay': 50,
                                                                       'bandwidth': 100,
                                                                       'reliability': 3,
                                                                       'ownership': "B"}))

    def test_path8_3_0(self):
        """Tests paths between all users using constrained path algorithm,
        with the delay constraint set to 50, the bandwidth constraint
        set to 100, the reliability constraint set to 3, and the ownership
        constraint set to 'B'

        Tests conducted with flexibility enabled
        """
        # ownership = "B"
        self.assertTrue(self.paths_between_all_users("S5:2", flexible={'delay': 50,
                                                                       'bandwidth': 100,
                                                                       'reliability': 3,
                                                                       'ownership': "B"}))

    def test_path8_3_1(self):
        """Tests paths between all users using constrained path algorithm,
        with the delay constraint set to 50, the bandwidth constraint
        set to 100, the reliability constraint set to 3, and the ownership
        constraint set to 'B'

        Tests conducted with flexibility enabled
        """
        # ownership = "B"
        self.assertTrue(self.paths_between_all_users("S4:2", flexible={'delay': 50,
                                                                       'bandwidth': 100,
                                                                       'reliability': 3,
                                                                       'ownership': "B"}))

    def test_path8_3_2(self):
        """Tests paths between all users using constrained path algorithm,
        with the delay constraint set to 50, the bandwidth constraint
        set to 100, the reliability constraint set to 3, and the ownership
        constraint set to 'B'

        Tests conducted with flexibility enabled
        """
        # ownership = "B"
        self.assertTrue(self.paths_between_all_users("User1:2", flexible={'delay': 50,
                                                                          'bandwidth': 100,
                                                                          'reliability': 3,
                                                                          'ownership': "B"}))

    def test_path8_3_3(self):
        """Tests paths between all users using constrained path algorithm,
        with the delay constraint set to 50, the bandwidth constraint
        set to 100, the reliability constraint set to 3, and the ownership
        constraint set to 'B'

        Tests conducted with flexibility enabled
        """
        # ownership = "B"
        self.assertTrue(self.paths_between_all_users("S5:4", flexible={'delay': 50,
                                                                       'bandwidth': 100,
                                                                       'reliability': 3,
                                                                       'ownership': "B"}))

    def test_path8_3_4(self):
        """Tests paths between all users using constrained path algorithm,
        with the delay constraint set to 50, the bandwidth constraint
        set to 100, the reliability constraint set to 3, and the ownership
        constraint set to 'B'

        Tests conducted with flexibility enabled
        """
        # ownership = "B"
        self.assertTrue(self.paths_between_all_users("S6:2", flexible={'delay': 50,
                                                                       'bandwidth': 100,
                                                                       'reliability': 3,
                                                                       'ownership': "B"}))

    def test_path8_3_5(self):
        """Tests paths between all users using constrained path algorithm,
        with the delay constraint set to 50, the bandwidth constraint
        set to 100, the reliability constraint set to 3, and the ownership
        constraint set to 'B'

        Tests conducted with flexibility enabled
        """
        # ownership = "B"
        self.assertTrue(self.paths_between_all_users("S6:5", flexible={'delay': 50,
                                                                       'bandwidth': 100,
                                                                       'reliability': 3,
                                                                       'ownership': "B"}))

    def test_path8_3_6(self):
        """Tests paths between all users using constrained path algorithm,
        with the delay constraint set to 50, the bandwidth constraint
        set to 100, the reliability constraint set to 3, and the ownership
        constraint set to 'B'

        Tests conducted with flexibility enabled
        """
        # ownership = "B"
        self.assertTrue(self.paths_between_all_users("S10:1", flexible={'delay': 50,
                                                                        'bandwidth': 100,
                                                                        'reliability': 3,
                                                                        'ownership': "B"}))

    def test_path8_3_7(self):
        """Tests paths between all users using constrained path algorithm,
        with the delay constraint set to 50, the bandwidth constraint
        set to 100, the reliability constraint set to 3, and the ownership
        constraint set to 'B'

        Tests conducted with flexibility enabled
        """
        # ownership = "B"
        self.assertTrue(self.paths_between_all_users("S8:6", flexible={'delay': 50,
                                                                       'bandwidth': 100,
                                                                       'reliability': 3,
                                                                       'ownership': "B"}))

    def test_path8_3_8(self):
        """Tests paths between all users using constrained path algorithm,
        with the delay constraint set to 50, the bandwidth constraint
        set to 100, the reliability constraint set to 3, and the ownership
        constraint set to 'B'

        Tests conducted with flexibility enabled
        """
        # ownership = "B"
        self.assertTrue(self.paths_between_all_users("S10:2", flexible={'delay': 50,
                                                                        'bandwidth': 100,
                                                                        'reliability': 3,
                                                                        'ownership': "B"}))

    def test_path8_3_9(self):
        """Tests paths between all users using constrained path algorithm,
        with the delay constraint set to 50, the bandwidth constraint
        set to 100, the reliability constraint set to 3, and the ownership
        constraint set to 'B'

        Tests conducted with flexibility enabled
        """
        # ownership = "B"
        self.assertTrue(self.paths_between_all_users("S10:3", flexible={'delay': 50,
                                                                        'bandwidth': 100,
                                                                        'reliability': 3,
                                                                        'ownership': "B"}))

    def test_path8_4_0(self):
        """Tests paths between all users using constrained path algorithm,
        with the delay constraint set to 50, the bandwidth constraint
        set to 100, the reliability constraint set to 3, and the ownership
        constraint set to 'B'

        Tests conducted with flexibility enabled
        """
        # ownership = "B"
        self.assertTrue(self.paths_between_all_users("User2:1", flexible={'delay': 50,
                                                                          'bandwidth': 100,
                                                                          'reliability': 3,
                                                                          'ownership': "B"}))
