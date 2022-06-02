#!/usr/bin/env python3

# General imports
from argparse import ArgumentParser
from datetime import timedelta
from random import choice as random_choice
from time import clock_gettime, CLOCK_BOOTTIME

# Title - user@hostname
from getpass import getuser
from socket import gethostname

# System info modules
from platform import platform as system
from platform import release as kernel
# from platform import machine as architecture
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
    "graysexual": [54, 242, 255, 242, 54],
}

# When printed, reset will end the color of the row
reset = "\033[0m\033[39m"


def color256(col: int, bg_fg: str) -> str:
    # Alias to avoid manually typing out escape codes every time
    return f"\033[{48 if bg_fg == 'bg' else 38};5;{col}m"


def draw_fetch(flag_name: str, width: int = None):
    # Load the chosen flag from the dictionary of flags
    flag = flags[flag_name]

    # Make sure that the row color is different to the color of the hostname
    row_color = color256(flag[1] if flag[0] != flag[1] else flag[2], "fg")

    # The fetch data (system info) to be displayed
    row_data = [
        f"{color256(flag[0], 'fg') if flag[0] != 0 else color256(242, 'fg')}"
        f"\033[1m{getuser()}@{gethostname()}{reset}",
        f"{row_color}os      {reset}{distribution() or system() or 'N/A'}",
        # f"{row_color}arch    {reset}{architecture() or 'N/A'}",
        f"{row_color}pkgs    {reset}{packages() or 'N/A'}",
        f"{row_color}kernel  {reset}{kernel() or system() or 'N/A'}",
        f"{row_color}uptime  {reset}{str(timedelta(seconds=clock_gettime(CLOCK_BOOTTIME))).split('.', 1)[0]}"
    ]

    # Until the flag is a greater length than the data
    while len(flag) < len(row_data):
        # If the data is greater than the flag length then duplicate the length of the flag
        flag = [element for element in flag for _ in (0, 1)]

    # Set the width of the flag relative to its height (keep it in a ratio)
    width = width or round(len(flag) * 1.5 * 3)

    # Ensures nothing is printed for empty lines
    row_data.append("")

    # Print a blank line to separate the flag from the terminal prompt
    print()

    for index, row in enumerate(flag):
        # Print out each row of the fetch
        print(f" {color256(row, 'bg')}{' ' * width}\033[49m{reset} {row_data[min(index, len(row_data) - 1)]}{reset}")

    # Print a blank line to separate the flag from the terminal prompt
    print()


def main():
    # Argument configuration - options
    parser = ArgumentParser()
    parser.add_argument("-f", "--flag", help="displays the chosen flag")
    parser.add_argument("-r", "--random", help="randomly choose a flag from a list seperated by commas")
    parser.add_argument("-w", "--width", help="choose a custom width for the flag", type=int)
    parser.add_argument("-l", "--list", help="lists all the flags that can be displayed", action="store_true")

    # Parse (collect) any arguments
    args = parser.parse_args()

    if args.flag:
        # Check if the flag exists in the dictionary of flags
        assert args.flag in flags.keys(), f"flag '{args.flag}' is not a valid flag"

        # Draw the chosen flag and system information
        draw_fetch(args.flag, args.width)

    elif args.random:
        # Choose a flag at random from a list of comma-seperated flags
        flag_choices = args.random.split(",")
        draw_fetch(random_choice(flag_choices), args.width)

    elif args.list:
        # List out all the available flags
        print(f"Available flags:\n{', '.join(flags)}")

    else:
        # By default, draw the classic flag
        draw_fetch("classic", args.width)


if __name__ == "__main__":
    main()
