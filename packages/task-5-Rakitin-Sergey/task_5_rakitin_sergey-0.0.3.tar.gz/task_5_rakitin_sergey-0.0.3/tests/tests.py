import argparse
import os
import sys

import pytest


from task_5_Rakitin_Sergey.collection import (
    UniqueSymbolCount,
    command_line_input,
    suggest_command,
)
from unittest.mock import patch, mock_open


class Tests:
    """Tests for the UniqueSymbolCount class"""

    def setup_class(self):
        """Clear cache before tests"""

        UniqueSymbolCount().unique_symbol_count.cache_clear()
        print("Cache cleared before tests")

    @pytest.mark.parametrize(
        "text", [1234, 26.5, ["a", "b"], {"key": "value"}, (1, 2, 3), None]
    )
    def test_validate_input(self, text):
        """
        Test validate_input with invalid inputs
        ensures Type error is raised with the correct message
        :parameter
            text: The input data to test expected to be invalid.
        """

        with pytest.raises(TypeError) as error:
            UniqueSymbolCount().validate_input(text)
        assert str(error.value) == f"Input must be a string, received {type(text)}"

    @pytest.mark.parametrize(
        "text, expected",
        [
            ("abbbccdf", 3),
            ("aabbcc", 0),
            ("abcdef", 6),
            ("", 0),
            ("a", 1),
            ("aabbcde", 3),
            ("abcabcabc", 0),
            ("abcdeabcd", 1),
            ("abbbccdf", 3),
            ("abbbccdf", 3),
            ("aabbcc", 0),
            ("abcdef", 6),
            ("", 0),
            ("a", 1),
            ("aabbcde", 3),
            ("abcabcabc", 0),
            ("abcdeabcd", 1),
            ("abbbccdf", 3),
            ("abbbccdf", 3),
            ("aabbcc", 0),
        ],
    )
    def test_unique_symbol_cont(self, text: str, expected: int):
        """
        Test unique_symbol_cont with different input strings
        Ensuring that function returns correct number of unique symbols
        :param
            text: input string
            expected: output integer
        """

        # create number of class for test
        test_case = UniqueSymbolCount().unique_symbol_count(text)
        assert test_case == expected

    def test_cache_behavior(self):
        """
        Test the caching behavior of unique_symbol_count method.
        The function passes two different strings alternately and counts hits and misses.
        """

        # Creating an instance of a class
        usc = UniqueSymbolCount()

        # Clear the cache before testing
        usc.unique_symbol_count.cache_clear()

        # First call - cache miss
        usc.unique_symbol_count("abc")
        cache_info = usc.unique_symbol_count.cache_info()
        assert cache_info.hits == 0
        assert cache_info.misses == 1

        # Second call with same argument - cache hit
        usc.unique_symbol_count("abc")
        cache_info = usc.unique_symbol_count.cache_info()
        assert cache_info.hits == 1
        assert cache_info.misses == 1

        # Third call with different argument - cache miss
        usc.unique_symbol_count("def")
        cache_info = usc.unique_symbol_count.cache_info()
        assert cache_info.hits == 1
        assert cache_info.misses == 2

        # Fourth call with first argument again - cache hit
        usc.unique_symbol_count("abc")
        cache_info = usc.unique_symbol_count.cache_info()
        assert cache_info.hits == 2
        assert cache_info.misses == 2

    def test_cache_maxsize(self):
        """Test that the cache does not exceed its maximum size."""

        # Creating an instance of a class
        usc = UniqueSymbolCount()

        # Clear the cache before testing
        usc.unique_symbol_count.cache_clear()

        # Fill the cache with unique entries
        for iteration in range(101):
            usc.unique_symbol_count(f"string_{iteration}")

        cache_info = usc.unique_symbol_count.cache_info()
        assert cache_info.currsize <= 100, "Cache exceeded its maximum size"

        # Check if oldest item was removed and new item added correctly
        usc.unique_symbol_count("string_101")
        cache_info = usc.unique_symbol_count.cache_info()
        assert (
            cache_info.currsize <= 100
        ), "Cache exceeded its maximum size after adding a new item"
        assert cache_info.hits == 0, "Unexpected cache hits"
        assert cache_info.misses == 102, "Unexpected cache misses"

    @patch("argparse.ArgumentParser.parse_args")
    def test_command_line_input_string(self, mock_args):
        """
        Test the command_line_function with a string argument.
        Test ensures that function correct process string and
        returns expected output.
        :param mock_args: Mock object for argparse.ArgumentParser.parse_args
        """

        # Configure the mock object to simulate CLI arguments
        mock_args.return_value = argparse.Namespace(string="abc", file=None)

        # Patch the built-in print function to capture its output
        with patch("builtins.print") as mocked_print:

            # Call CLI function
            command_line_input()

            # Verify that correct messages printed
            mocked_print.assert_any_call("Processing string...")
            mocked_print.assert_any_call("Result of operation with string: 3")

    @patch("argparse.ArgumentParser.parse_args")
    @patch("builtins.open", new_callable=mock_open, read_data="abc")
    def test_command_line_input_file(self, mock_open, mock_args):
        """
        Test command_line_input with a file argument.
        Ensures that function correct process the file, return expected messages.
        Also verifies that file was read and closed.
        :param mock_open: Mock object for built-on open funktion
        :param mock_args: Mock object for argparse.ArgumentParser.parse_args
        :return:
        """

        # Create mock file object
        mock_file = mock_open.return_value
        mock_file.name = "test.txt"

        # Set up mock for argparse.Namespace
        mock_args.return_value = argparse.Namespace(string=None, file=mock_file)

        # Mock print for checking output
        with patch("builtins.print") as mocked_print:
            command_line_input()

            # Check that print was called with expected arguments
            mocked_print.assert_any_call("Processing file...")
            mocked_print.assert_any_call("Result of operation with file: 3")

            # Verify that the file was read and closed
            mock_file.read.assert_called_once()
            mock_file.close.assert_called_once()

    @patch("argparse.ArgumentParser.parse_args")
    def test_command_line_invalid_input(self, mock_args):
        """
        Test the command_line_input function with an invalid input(for example data "123")
        ensuring correct error handling.
        """

        mock_args.return_value = argparse.Namespace(
            string=None, file=None, data=123
        )  # Using an invalid data type

        with pytest.raises(TypeError) as exception_info:
            command_line_input()
        assert (
            str(exception_info.value)
            == "Error: No valid input provided. A string or a text file is expected."
        )

    def test_suggest_command(self):
        """
        Test the suggest_command function with various invalid inputs.
        """

        # List of valid commands
        valid_cmds = ["--string", "--file", "--help"]

        # Test cases with invalid CMD input
        assert suggest_command("--strin", valid_cmds) == "--string"
        assert suggest_command("--fil", valid_cmds) == "--file"
        assert suggest_command("--hel", valid_cmds) == "--help"


if __name__ == "__main__":

    pytest.main()
