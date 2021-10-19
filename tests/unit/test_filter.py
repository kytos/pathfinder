"""Test filter methods"""
from unittest import TestCase

from napps.kytos.pathfinder.utils import lazy_filter
from napps.kytos.pathfinder.graph import KytosGraph


class TestLazyFilter(TestCase):
    """Tests for the Main class."""

    def setUp(self):
        """Execute steps before each test."""
        self.graph = KytosGraph()

    def test_type_error(self):
        """Test filtering with invalid minimum type."""
        items = [8, 9, 10, 11, 12]
        minimum = "wrong_type"
        with self.assertRaises(TypeError):
            filtered = lazy_filter(int, lambda x: (lambda y: y >= x))
            list(filtered(minimum, items))

    def test_filter_functions_in(self):
        """Test _filter_function that are expected to use the filter_in""" ""

        attr = "ownership"
        nx_edge_values = [
            (None, None, {attr: {"blue": {}, "red": {}}}),
            (None, None, {attr: {"green": {}}}),
        ]

        target = "blue"
        ownership_filter = self.graph._filter_functions[attr]
        filtered = list(ownership_filter(target, nx_edge_values))
        assert filtered

        for item in filtered:
            assert target in item[2][attr]

    def test_filter_functions_ge(self):
        """Test _filter_function that are expected to use the filter_ge."""

        for attr in ("bandwidth", "reliability"):
            nx_edge_values = [
                (None, None, {attr: 20}),
                (None, None, {attr: 10}),
            ]

            target = 15
            func = self.graph._filter_functions[attr]
            filtered = list(func(target, nx_edge_values))
            assert filtered

            for item in filtered:
                assert item[2][attr] >= target

            target = 21
            filter_func = self.graph._filter_functions[attr]
            filtered = list(filter_func(target, nx_edge_values))
            assert not filtered

    def test_filter_functions_le(self):
        """Test _filter_function that are expected to use the filter_le."""

        for attr in ("priority", "delay", "utilization"):
            nx_edge_values = [
                (None, None, {attr: 20}),
                (None, None, {attr: 10}),
            ]

            target = 15
            func = self.graph._filter_functions[attr]
            filtered = list(func(target, nx_edge_values))
            assert filtered

            for item in filtered:
                assert item[2][attr] <= target

            target = 9
            filter_func = self.graph._filter_functions[attr]
            filtered = list(filter_func(target, nx_edge_values))
            assert not filtered
