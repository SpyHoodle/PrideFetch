#!/usr/bin/env python3

# General imports
from argparse import ArgumentParser
from datetime import timedelta
from random import choice as random_choice
import color

# Title - user@hostname
from getpass import getuser
from socket import gethostname

# System info modules
from platform import platform as system
from platform import release as kernel
from time import clock_gettime, CLOCK_BOOTTIME
from platform import machine as architecture
from distro import name as distribution
from modules.packages import get_num_packages as packages

# A dictionary of all the flags and their colors
# Each color is the color for an individual row in the flag
flags = {
    "classic": [196, 208, 226, 28, 20, 90],
    "gay": [23, 43, 115, 255, 117, 57, 55],
    "bisexual": [198, 198, 97, 25, 25],
    "lesbian": [202, 209, 255, 255, 168, 161],
    "pansexual": [198, 220, 39],
    "trans": [81, 211, 255, 211, 81],
    "nonbinary": [226, 255, 98, 237],
    "demiboy": [244, 249, 117, 255, 117, 249, 244],
    "demigirl": [244, 249, 218, 255, 218, 249, 244],
    "genderfluid": [211, 255, 128, 0, 63],
    "genderqueer": [141, 255, 64],
    "aromantic": [71, 149, 255, 249, 0],
    "agender": [0, 251, 255, 149, 255, 251, 0],
    "asexual": [0, 242, 255, 54],
    "graysexual": [54, 242, 255, 242, 54]
}

# A dictionary of all the available stats
stats = {
    "os": lambda: distribution() or system() or 'N/A',
    "arch": lambda: architecture() or 'N/A',
    "pkgs": lambda: packages() or 'N/A',
    "kernel": lambda: kernel() or system() or 'N/A',
    "uptime": lambda: str(timedelta(seconds=clock_gettime(CLOCK_BOOTTIME))).split('.', 1)[0]
}


def generate_fetch(flag_name: str, show_stats: list = None, width: int = None) -> (list, int, list):
    """
    Generates variables needed for a fetch
    :param flag_name: The name of the flag to use
    :param show_stats: Stats to show in the fetch
    :param width: Custom width of the flag
    :return: Generated flag data
    """

    # Load the chosen flag from the dictionary of flags
    flag = flags[flag_name]

    # Make sure that the row color is different to the color of the hostname
    row_color = color.color256(flag[1] if flag[0] != flag[1] else flag[2], "fg")

    # Set default stats to show in the fetch
    show_stats = show_stats or ["os", "pkgs", "kernel", "uptime"]

    # Initialise the fetch data (system info) to be displayed with the user@hostname
    data = [
        f"{color.color256(flag[0], 'fg') if flag[0] != 0 else color.color256(242, 'fg')}"
        f"\033[1m{getuser()}@{gethostname()}{color.clear}",
    ]

    # Add the chosen stats to the list row_data
    for stat in show_stats:
        # Calculate the value for the stat by running its function
        value = stats[stat]()

        # Calculate the correct amount of spaces to keep the stat values in line with each other
        spaces = ((len(max(show_stats)) - len(stat)) + 1) * " "

        # Generate a row with color, stat name and its value
        row = f"{row_color}{stat}:{spaces}{color.clear}{value}"

        # Add the row to the data
        data.append(row)

    # Until the flag is a greater length than the data
    while len(flag) < len(data):
        # If the data is greater than the flag length then duplicate the length of the flag
        flag = [element for element in flag for _ in (0, 1)]

    # Set the width of the flag relative to its height (keep it in a ratio)
    width = width or round(len(flag) * 1.5 * 3)

    # Ensures nothing is printed for empty lines
    data.append("")

    # Return all the flag information ready for drawing
    return flag, width, data


def draw_fetch(flag: list, width: int, data: list) -> None:
    """
    Draws a fetch to the screen
    :param flag: The flag as a list of colors
    :param width: Width of the flag rows
    :param data: System stats data
    """

    # Print a blank line to separate the flag from the terminal prompt
    print()

    for index, row in enumerate(flag):
        # Print out each row of the fetch
        print(f" {color.color256(row, 'bg')}{' ' * width}\033[49m{color.clear} "  # Flag rows
              f"{data[min(index, len(data) - 1)]}{color.clear}")  # Stats rows

    # Print a blank line again to separate the flag from the terminal prompt
    print()


def create_fetch(flag_name: str, show_stats: list = None, width: int = None) -> None:
    """
    Creates a fetch, by generating and then drawing it
    :param flag_name: The name of the flag to use
    :param show_stats: Stats to show in the fetch
    :param width: Custom width of the flag
    """

    # Check if the flag exists in the dictionary of flags
    assert flag_name in flags.keys(), f"flag '{flag_name}' is not a valid flag"

    # Generate a fetch with the given info
    flag, width, data = generate_fetch(flag_name, show_stats, width)

    # Draw the fetch
    draw_fetch(flag, width, data)


def check_valid_argument(arg_flag: str, argument: str, valid_arguments: list) -> bool:
    """
    Checks if an argument is valid by checking if it's in a list of valid arguments
    :param arg_flag: The argument flag e.g. --random, --stats etc.
    :param argument: A user inputted argument
    :param valid_arguments: The valid list of arguments to check against
    :return: True if the argument is valid, False if not
    """

    # Check if argument is valid, by checking if it is not in valid_arguments
    if argument not in valid_arguments:
        _print_error(f"Invalid argument '{argument}' given for '{arg_flag}'",
                     f"must be one of '{', '.join(valid_arguments)}'")
        return False

    else:
        return True


def check_valid_arguments(arg_flag: str, arguments: list, valid_arguments: list) -> bool:
    """
    Checks if arguments are valid by checking if they are in a list of valid arguments
    :param arg_flag: The argument flag e.g. --random, --stats etc.
    :param arguments: A list of user inputted arguments
    :param valid_arguments: The valid list of arguments to check against
    :return: True if the arguments are valid, False if not
    """

    # If there are any arguments remaining
    if len(arguments) > 0:
        for argument in arguments:
            # If the argument isn't in valid_arguments, it isn't valid
            if not check_valid_argument(arg_flag, argument, valid_arguments):
                return False

    # Otherwise, the user must have typed comma(s) without any arguments
    else:
        _print_error(f"No arguments given for '{arg_flag}'",
                     f"must be one of '{', '.join(valid_arguments)}'")
        return False

    return True


def parse_comma_arguments(arg_flag: str, comma_arguments: str, valid_arguments: list) -> list:
    """
    Parses comma seperated arguments and checks if they are valid
    :param arg_flag: The argument command line flag e.g. --random, --stats etc.
    :param comma_arguments: Raw string of user inputted arguments including commas
    :param valid_arguments: The valid list of arguments to check against
    :return: Parsed arguments if valid, exits the program if invalid
    """

    # Separate arguments into a list
    arguments = comma_arguments.split(",")

    # Remove whitespaces from the list of arguments
    arguments = [argument.strip() for argument in arguments if argument.strip()]

    # Check if the passed arguments are valid, if not, exit with an error
    if not check_valid_arguments(arg_flag, arguments, valid_arguments):
        exit(1)

    # Otherwise return the arguments
    else:
        return arguments


def _print_error(error: str, help_message: str = None) -> None:
    """
    Prints an error message with optionally an extra help message
    :param error: Error message to print
    :param help_message: Optional help message
    :return:
    """

    # Print out the error message
    print(f"{color.bold}{color.red}Error: {error}{color.clear}")

    # If the help message was given, print it out
    if help_message:
        print(f"  {color.red}╰> {help_message}{color.clear}")


def main():
    """
    Main function that evaluates command line arguments
    """

    # Argument configuration - pridefetch command line options
    parser = ArgumentParser()
    parser.add_argument("-l", "--list", help="lists all flags and stats that can be displayed", action="store_true")
    parser.add_argument("-a", "--all-stats", help="use all available stats (overrides '--stats')", action="store_true")
    parser.add_argument("-f", "--flag", help="displays a flag of your choice")
    parser.add_argument("-r", "--random", help="randomly choose a flag from a comma-seperated list")
    parser.add_argument("-s", "--stats", help="choose the stats to appear from a comma-seperated list")
    parser.add_argument("-w", "--width", help="choose a custom width for the flag", type=int)

    # Parse (collect) any arguments
    args = parser.parse_args()

    if args.all_stats:
        # Add all the available stats to show_stats
        show_stats = list(stats)

    elif args.stats:
        # Parse chosen statistics arguments if they exist
        show_stats = parse_comma_arguments("--stats", args.stats, list(stats))

    else:
        # Otherwise, use the default stats
        show_stats = None

    if args.flag:
        # Check if the flag is a valid flag
        if not check_valid_argument("--flag", args.flag, list(flags)):
            exit(1)

        # Draw the chosen flag and system information
        create_fetch(args.flag, show_stats, args.width)

    elif args.random:
        # Parse chosen random flag arguments if they exist
        flag_choices = parse_comma_arguments("--random", args.random, list(flags))

        # Draw a randomly selected flag from the list
        create_fetch(random_choice(flag_choices), show_stats, args.width)

    elif args.list:
        # List out all the available flags and stats
        print(f"{color.bold}Available flags:{color.clear}\n{', '.join(flags)}\n\n"
              f"{color.bold}Available stats:{color.clear}\n{', '.join(stats)}")

    else:
        # By default, draw the classic flag
        create_fetch("classic", show_stats, args.width)


if __name__ == "__main__":
    main()
