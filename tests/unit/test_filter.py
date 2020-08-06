"""Test filter methods"""
from unittest import TestCase

from napps.kytos.pathfinder.graph import Filter
from tests.helpers import get_test_filter_function


class TestFilter(TestCase):
    """Tests for the Main class."""

    def setUp(self):
        """Execute steps before each test."""
        filter_type = (int, float)
        filter_function = get_test_filter_function()
        self.filter = Filter(filter_type, filter_function)

    def test_run_success_case(self):
        """Test filtering with valid minimum type."""
        items = [8, 9, 10, 11, 12]
        minimum = 10
        result = self.filter.run(minimum, items)
        expected_result = [10, 11, 12]
        self.assertEqual(list(result), expected_result)

    def test_run_failure_case(self):
        """Test filtering with invalid minimum type."""
        items = [8, 9, 10, 11, 12]
        minimum = "apple"
        with self.assertRaises(TypeError):
            self.filter.run(minimum, items)
