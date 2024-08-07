from collections import Counter
import functools, argparse
import Levenshtein as lev


class UniqueSymbolCount:
    """Class to count unique symbols in a string"""

    def validate_input(self, text: str):
        """
        Validate that the input data is a string
        :arg
            text (str)
        :raise
            Error: if the input is not string.
        """

        if not isinstance(text, str):

            raise TypeError(f"Input must be a string, received {type(text)}")

    # caching function results
    @functools.lru_cache(maxsize=100)
    def unique_symbol_count(self, text: str) -> int:
        """
        Calculates sum of symbols occurring in a string only once
        :arg
            text: input string
        :returns
            the sum of unique symbols(int)
        """

        symbol_count = Counter(text)
        return sum(map(lambda count: count == 1, symbol_count.values()))


def suggest_command(input_cmd, valid_cmds, threshold=3):
    """
    Suggests a valid command based on the Levenshtein distance if the input command is invalid.
    :param input_cmd: The invalid command input by the user.
    :param valid_cmds: A list of valid commands.
    :param threshold: The maximum Levenshtein distance for suggestions.
    :return: Suggested command if found, otherwise None.
    """
    suggestions = [
        cmd for cmd in valid_cmds if lev.distance(input_cmd, cmd) <= threshold
    ]
    if not suggestions:
        return None

    # Sort suggestions by Levenshtein distance
    suggestions.sort(key=lambda cmd: lev.distance(input_cmd, cmd))
    return suggestions[0]


def command_line_input():
    """
    Function to parse command line arguments and process
    it with UniqueSymbolCount.
    If the provided arguments are invalid,
    it suggests the closest valid commands based on Levenshtein distance.
    :param
        Variable string or file to process
    """

    # Parser object
    parser = argparse.ArgumentParser()

    # Argument for input string
    parser.add_argument("--string", type=str)

    # Argument for input file
    parser.add_argument("--file", type=argparse.FileType("r"))
    parser.add_argument("--data", type=str)

    # Number of UniqueSymbolClass
    usc = UniqueSymbolCount()

    # List of valid commands
    valid_cmds = ["--string", "--file", "--data", "--help"]

    # Parse the arguments
    try:
        arg = parser.parse_args()
    except argparse.ArgumentError as exception:

        # Suggest closest command if an argument error occurs
        suggestion = suggest_command(str(exception), valid_cmds)
        if suggestion:
            print(f"Error: {exception}\nMaybe you mean: {suggestion}")
        else:
            print(f"Error unknown command: {exception}")
        return

    # Parse the arguments
    arg = parser.parse_args()

    if arg.file:  # Process the file

        # With... as construction to ensure that file will be closed
        with arg.file as file:
            print("Processing file...")

            # Reading the file
            content = file.read()

            # Validation content
            usc.validate_input(content)
            result = usc.unique_symbol_count(content)
            print(f"Result of operation with file: {result}")

        # Manually close the file (typically not needed, but added for test purposes)
        file.close()

    elif arg.string:  # Process the string if input non-text file
        print("Processing string...")

        # Validation string
        usc.unique_symbol_count(arg.string)
        result = usc.unique_symbol_count(arg.string)
        print(f"Result of operation with string: {result}")

    else:  # Error for incorrect input type
        raise TypeError(
            "Error: No valid input provided. A string or a text file is expected."
        )


if __name__ == "__main__":
    command_line_input()
