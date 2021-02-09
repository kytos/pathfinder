"""Module to test the KytosGraph in graph.py."""
from itertools import combinations

# module under test
from tests.integration.edges_settings import EdgesSettings


class TestResultsEdges(EdgesSettings):
    """Tests for the graph class.

    Tests to see if reflexive searches and impossible searches
    show correct results.
    """

    def test_path1(self):
        """Tests paths between all users using unconstrained path algorithm."""
        combos = combinations(["User1", "User2", "User3", "User4"], 2)
        self.initializer()

        valid = True
        for point_a, point_b in combos:
            results = self.get_path(point_a, point_b)
            if not results:
                valid = False
                break

        self.assertNotEqual(valid, False)

    def test_path12(self):
        """Tests paths between all users using unconstrained path algorithm."""
        combos = combinations(["User1", "User2", "User3", "User4", "User5"], 2)
        self.initializer()

        valid = True
        for point_a, point_b in combos:
            results = self.get_path(point_a, point_b)
            if not results:
                valid = False
                break

        self.assertEqual(valid, False)

    def test_path2(self):
        """Tests paths between all users using constrained path algorithm,
        with no constraints set.
        """
        combos = combinations(["User1", "User2", "User3", "User4"], 2)
        self.initializer()

        for point_a, point_b in combos:
            results = self.get_path_constrained(point_a, point_b)
            self.assertNotEqual(results, [])

    def paths_between_all_users(self, item, base=None, flexible=None, metrics=None):
        """Method to verify the existence of a path between
        a set of points given different constrains"""
        combos = combinations(["User1", "User2", "User3", "User4"], 2)
        self.initializer()

        valid = True
        for point_a, point_b in combos:
            results = []
            if base is not None and flexible is None:
                results = self.get_path_constrained(
                    point_a, point_b, base=base)

            elif base is None and flexible is not None:
                results = self.get_path_constrained(
                    point_a, point_b, flexible=flexible)

            for result in results:
                if metrics is not None:
                    if metrics in result["metrics"]:
                        for path in result["paths"]:
                            if item in path:
                                valid = False
                else:
                    for path in result["paths"]:
                        if item in path:
                            valid = False
        return valid

    def test_path3_1(self):
        """Tests paths between all users using constrained path algorithm,
        with the ownership constraint set to B.
        """
        self.assertTrue(self.paths_between_all_users("S4:1", {'ownership': "B"}))

    def test_path3_2(self):
        """Tests paths between all users using constrained path algorithm,
        with the ownership constraint set to B.
        """
        self.assertTrue(self.paths_between_all_users("S5:2", {'ownership': "B"}))

    def test_path3_3(self):
        """Tests paths between all users using constrained path algorithm,
        with the ownership constraint set to B.
        """
        self.assertTrue(self.paths_between_all_users("S4:2", {'ownership': "B"}))

    def test_path3_4(self):
        """Tests paths between all users using constrained path algorithm,
        with the ownership constraint set to B.
        """
        self.assertTrue(self.paths_between_all_users("User1:2", {'ownership': "B"}))

    def test_path3_5(self):
        """Tests paths between all users using constrained path algorithm,
        with the ownership constraint set to B.
        """
        self.assertTrue(self.paths_between_all_users("S5:4", {'ownership': "B"}))

    def test_path3_6(self):
        """Tests paths between all users using constrained path algorithm,
        with the ownership constraint set to B.
        """
        self.assertTrue(self.paths_between_all_users("S6:2", {'ownership': "B"}))

    def test_path3_7(self):
        """Tests paths between all users using constrained path algorithm,
        with the ownership constraint set to B.
        """
        self.assertTrue(self.paths_between_all_users("S6:5", {'ownership': "B"}))

    def test_path3_8(self):
        """Tests paths between all users using constrained path algorithm,
        with the ownership constraint set to B.
        """
        self.assertTrue(self.paths_between_all_users("S10:1", {'ownership': "B"}))

    def test_path3_9(self):
        """Tests paths between all users using constrained path algorithm,
        with the ownership constraint set to B.
        """
        self.assertTrue(self.paths_between_all_users("S8:6", {'ownership': "B"}))

    def test_path3_1_0(self):
        """Tests paths between all users using constrained path algorithm,
        with the ownership constraint set to B.
        """
        self.assertTrue(self.paths_between_all_users("S10:2", {'ownership': "B"}))

    def test_path3_1_1(self):
        """Tests paths between all users using constrained path algorithm,
        with the ownership constraint set to B.
        """
        self.assertTrue(self.paths_between_all_users("S10:3", {'ownership': "B"}))

    def test_path3_1_2(self):
        """Tests paths between all users using constrained path algorithm,
        with the ownership constraint set to B.
        """
        self.assertTrue(self.paths_between_all_users("User2:1", {'ownership': "B"}))

#####

    def test_path4_1(self):
        """Tests paths between all users using constrained path algorithm,
        with the reliability constraint set to 3.
        """
        self.assertTrue(self.paths_between_all_users("S4:1", {'reliability': 3}))

    def test_path4_2(self):
        """Tests paths between all users using constrained path algorithm,
        with the reliability constraint set to 3.
        """
        self.assertTrue(self.paths_between_all_users("S5:2", {'reliability': 3}))

    def test_path4_3(self):
        """Tests paths between all users using constrained path algorithm,
        with the reliability constraint set to 3.
        """
        self.assertTrue(self.paths_between_all_users("S5:3", {'reliability': 3}))

    def test_path4_4(self):
        """Tests paths between all users using constrained path algorithm,
        with the reliability constraint set to 3.
        """
        self.assertTrue(self.paths_between_all_users("S6:1", {'reliability': 3}))

    def test_path5_1(self):
        """Tests paths between all users using constrained path algorithm,
        with the reliability constraint set to 3.
        """
        self.assertTrue(self.paths_between_all_users("S3:1", {'bandwidth': 100}))

    def test_path5_2(self):
        """Tests paths between all users using constrained path algorithm,
        with the reliability constraint set to 3.
        """
        self.assertTrue(self.paths_between_all_users("S5:1", {'bandwidth': 100}))

    def test_path5_3(self):
        """Tests paths between all users using constrained path algorithm,
        with the reliability constraint set to 3.
        """
        self.assertTrue(self.paths_between_all_users("User1:4", {'bandwidth': 100}))

    def test_path5_4(self):
        """Tests paths between all users using constrained path algorithm,
        with the reliability constraint set to 3.
        """
        self.assertTrue(self.paths_between_all_users("User4:3", {'bandwidth': 100}))

####

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

####

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

#####

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

#####

    def test_path9(self):
        """Tests paths between all users using constrained path algorithm,
        with the delay constraint set to 50, the bandwidth constraint
        set to 100, the reliability constraint set to 3, and the ownership
        constraint set to 'B'

        Tests conducted with all but ownership flexible
        """
        combos = combinations(["User1", "User2", "User3", "User4"], 2)
        self.initializer()

        for point_a, point_b in combos:
            results = self.get_path_constrained(point_a, point_b,
                                                base={"ownership": "B"},
                                                flexible={"delay": 50,
                                                          "bandwidth": 100,
                                                          "reliability": 3})
            for result in results:
                # delay = 50 checks
                if "delay" in result["metrics"]:
                    for path in result["paths"]:
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

                # bandwidth = 100 checks
                if "bandwidth" in result["metrics"]:
                    for path in result["paths"]:
                        self.assertNotIn("S3:1", path)
                        self.assertNotIn("S5:1", path)
                        self.assertNotIn("User1:4", path)
                        self.assertNotIn("User4:3", path)

                # reliability = 3 checks
                if "reliability" in result["metrics"]:
                    for path in result["paths"]:
                        self.assertNotIn("S4:1", path)
                        self.assertNotIn("S5:2", path)
                        self.assertNotIn("S5:3", path)
                        self.assertNotIn("S6:1", path)

                # ownership = "B" checks
                self.assertIn("ownership", result["metrics"])
                for path in result["paths"]:
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

    def test_path10(self):
        """Tests that TypeError is generated by get_path_constrained

        Tests with ownership using an int type rather than string
        """
        self.initializer()

        with self.assertRaises(TypeError):
            self.get_path_constrained(
                "User1", "User2", base={"ownership": 1})
