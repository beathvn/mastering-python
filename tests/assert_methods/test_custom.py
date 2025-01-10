# since we inherit from unittest.TestCase, we can use all the assert methods that unittest provides

import unittest

class CustomTestCase(unittest.TestCase):
    def assertAllIntegers(self, values):
        for value in values:
            self.assertIsInstance(
                value,
                int,
            )

class TestIntegerList(CustomTestCase):
    def test_values_are_integers(self):
        integers_list = [1, 2, 3, 4, 5]
        self.assertAllIntegers(integers_list)

if __name__ == "__main__":
    unittest.main()