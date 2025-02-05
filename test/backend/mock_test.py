import unittest
from unittest.mock import patch
from io import StringIO
import sys
import os

# Add the backend directory to the Python path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "../..")))


class TestHelloWorld(unittest.TestCase):
    """Test cases for hello_world.py"""

    @patch("sys.stdout", new_callable=StringIO)
    def test_hello_world_output(self, mock_stdout):
        """Test if hello_world.py prints 'Hello, World!' correctly"""
        from backend.hello_world import print_hello_world  # noqa: F401

        expected_output = "Hello, World!\n"
        print_hello_world()
        self.assertEqual(mock_stdout.getvalue(), expected_output)


if __name__ == "__main__":
    unittest.main()
