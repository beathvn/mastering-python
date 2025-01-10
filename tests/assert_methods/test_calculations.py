# the make_suit and load_tests function is only necessary for the command line.
# vs code detects the suits

import unittest

from calculations import (
    add,
    divide,
    mean,
    median,
    mode,
    multiply,
    subtract,
)

class TestArithmeticOperations(unittest.TestCase):
    def test_add(self):
        self.assertEqual(add(10, 5), 15)
        self.assertEqual(add(-1, 1), 0)

    def test_subtract(self):
        self.assertEqual(subtract(10, 5), 5)
        self.assertEqual(subtract(-1, 1), -2)

    def test_multiply(self):
        self.assertEqual(multiply(10, 5), 50)
        self.assertEqual(multiply(-1, 1), -1)

    def test_divide(self):
        self.assertEqual(divide(10, 5), 2)
        self.assertEqual(divide(-1, 1), -1)
        with self.assertRaises(ZeroDivisionError):
            divide(10, 0)

class TestStatisticalOperations(unittest.TestCase):
    def test_mean(self):
        self.assertEqual(mean([1, 2, 3, 4, 5, 6]), 3.5)

    def test_median_odd(self):
        self.assertEqual(median([1, 3, 3, 6, 7, 8, 9]), 6)

    def test_median_even(self):
        self.assertEqual(median([1, 2, 3, 4, 5, 6, 8, 9]), 4.5)

    def test_median_unsorted(self):
        self.assertEqual(median([7, 1, 3, 3, 2, 6]), 3)

    def test_mode_single(self):
        self.assertEqual(mode([1, 2, 2, 3, 4, 4, 4, 5]), [4])

    def test_mode_multiple(self):
        self.assertEqual(set(mode([1, 1, 2, 3, 4, 4, 5, 5])), {1, 4, 5})


def make_suite():
    arithmetic_tests = [
        TestArithmeticOperations("test_add"),
        TestArithmeticOperations("test_subtract"),
        TestArithmeticOperations("test_multiply"),
        TestArithmeticOperations("test_divide"),
    ]
    return unittest.TestSuite(tests=arithmetic_tests)

def load_tests(loader, standard_tests, pattern):
    # make_suite can be cumbersome to maintain
    suite = unittest.TestSuite()
    suite.addTests(loader.loadTestsFromTestCase(TestArithmeticOperations))
    suite.addTests(loader.loadTestsFromTestCase(TestStatisticalOperations))
    return suite

if __name__ == "__main__":
    suite = make_suite()
    runner = unittest.TextTestRunner(verbosity=2)
    runner.run(suite)