import unittest
import pandas as pd
from main import find_ideal_functions, locateY

'''Unit testcases for the code'''


class TestFindIdealFunctions(unittest.TestCase):
    def setUp(self):
        # test cases training data and ideal functions
        self.train_data = pd.DataFrame(
            {'x': [1, 2, 3], 'y1': [2, 4, 6], 'y2': [3, 6, 9], 'y3': [1, 3, 5], 'y4': [2, 3, 5]})
        self.ideal_functions = pd.DataFrame(
            {'x': [1, 2, 3], 'f1': [2, 4, 6], 'f2': [4, 8, 12], 'f3': [1, 4, 9], 'f4': [2, 4, 8], 'f5': [3, 4, 9]})

    def test_find_ideal_functions(self):
        chosen_functions = find_ideal_functions(self.train_data, self.ideal_functions)
        self.assertEqual(chosen_functions, {'x': 0, 'y1': 1, 'y2': 5, 'y3': 1, 'y4': 1})

    def test_locateY_existing_x(self):
        self.assertEqual(locateY(2, self.ideal_functions[['x', 'f1']]), 4)

    def test_locateY_missing_x(self):
        # Test the function with a non-existent x value in ideal
        with self.assertRaises(IndexError):
            locateY(4, self.ideal_functions[['x', 'f1']])


if __name__ == '__main__':
    unittest.main()
