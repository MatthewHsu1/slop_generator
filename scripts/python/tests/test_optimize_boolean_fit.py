import math
import unittest

from src.optimize_boolean_fit import _binary_search_min_feasible, _generate_euler_grid


class TestOptimizeBooleanFitHelpers(unittest.TestCase):
    def test_generate_euler_grid_90_degrees_has_expected_count(self):
        grid = _generate_euler_grid(90)
        self.assertEqual(len(grid), 64)

    def test_generate_euler_grid_rejects_invalid_step(self):
        with self.assertRaises(ValueError):
            _generate_euler_grid(0)

    def test_binary_search_min_feasible_finds_threshold(self):
        threshold = math.sqrt(2.0)

        def predicate(x: float) -> bool:
            return x >= threshold

        result = _binary_search_min_feasible(0.0, 2.0, predicate, iterations=40)

        self.assertLess(abs(result - threshold), 1e-6)


if __name__ == "__main__":
    unittest.main()
