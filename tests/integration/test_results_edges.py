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
