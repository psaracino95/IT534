#This tests the validation for the variable_sorter
#May have missed some
#Dunno, will try to use gemini to cover bases, but write the code myself,

import unittest
import variable_sorter 

class TestVariableSort(unittest.TestCase):
    def setUp(self):
        """Runs before every individual test case to provide a clean sorter instance."""
        self.sorter = variable_sorter.VariableSort()
    def test_valid_integer(self):
        """Verify positive, negative, and zero integers are sorted correctly."""
        self.sorter.validate_and_sort("42")
        self.sorter.validate_and_sort("-7")
        self.sorter.validate_and_sort("0")
        self.assertEqual(self.sorter.integers, [42, -7, 0])

    def test_valid_float(self):
        """Verify standard decimals and negative decimals are sorted correctly."""
        self.sorter.validate_and_sort("3.14")
        self.sorter.validate_and_sort("-0.005")
        self.assertEqual(self.sorter.floats, [3.14, -0.005])

    def test_valid_string(self):
        """Verify strings containing only alphabetic characters are accepted."""
        self.sorter.validate_and_sort("HelloWorld")
        self.sorter.validate_and_sort("python")
        self.assertEqual(self.sorter.strings, ["HelloWorld", "python"])

    def test_invalid_string_with_spaces(self):
        """Verify strings containing spaces are rejected with a ValueError."""
        with self.assertRaises(ValueError):
            self.sorter.validate_and_sort("Hello World")

    def test_invalid_string_with_special_characters(self):
        """Verify alphanumeric or punctuated strings are rejected."""
        with self.assertRaises(ValueError):
            self.sorter.validate_and_sort("Python3")
        with self.assertRaises(ValueError):
            self.sorter.validate_and_sort("user@domain.com")

    def test_empty_input(self):
        """Verify completely empty inputs throw an exception."""
        with self.assertRaises(ValueError):
            self.sorter.validate_and_sort("   ")

    def test_summary_output(self):
        """Verify the summary method maps lists correctly."""
        self.sorter.validate_and_sort("10")
        self.sorter.validate_and_sort("abc")
        summary = self.sorter.get_summary()
        self.assertIn(10, summary["Integers"])
        self.assertIn("abc", summary["Strings"])

if __name__ == "__main__":
    unittest.main()

#Usage: -m unittest test_variable_sorter.py