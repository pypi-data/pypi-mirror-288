# tests/test_color_printer.py

import unittest
from io import StringIO
import sys
from image_to_psd.color_printer import *

class TestColorPrinter(unittest.TestCase):

    def setUp(self):
        # Redirect stdout to capture print statements
        self.held_output = StringIO()
        sys.stdout = self.held_output

    def tearDown(self):
        # Reset redirect.
        sys.stdout = sys.__stdout__

    def test_print_color(self):
        # Test the print_color function
        test_message = "Red"
        print_red(test_message)
        self.held_output.seek(0)  # Go to the start of the StringIO buffer
        output = self.held_output.getvalue().strip()
        expected_output = f"Color: {test_message}"
        self.assertEqual(output, expected_output)

if __name__ == '__main__':
    unittest.main()
