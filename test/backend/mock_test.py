"""Test cases for hello_world module."""

from io import StringIO
from unittest.mock import patch

from backend.hello_world import print_hello_world


def test_hello_world_output() -> None:
    """Test if print_hello_world outputs 'Hello, World!' correctly."""
    with patch("sys.stdout", new_callable=StringIO) as mock_stdout:
        print_hello_world()
        assert mock_stdout.getvalue() == "Hello, World!\n"
