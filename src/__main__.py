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
    "graysexual": [54, 242, 255, 242, 54],
}

# A dictionary of all the available stats
stats = {
    "os": distribution() or system() or 'N/A',
    "arch": architecture() or 'N/A',
    "pkgs": packages() or 'N/A',
    "kernel": kernel() or system() or 'N/A',
    "uptime": str(timedelta(seconds=clock_gettime(CLOCK_BOOTTIME))).split('.', 1)[0]
}

# When printed, reset will end the color of the row
reset = "\033[0m\033[39m"

# When printed, text will become bold
bold = "\033[1m"

def color256(col: int, bg_fg: str) -> str:
    # Alias to avoid manually typing out escape codes every time
    return f"\033[{48 if bg_fg == 'bg' else 38};5;{col}m"


def calc_fetch(flag_name: str, show_stats = None, width = None):
    # Load the chosen flag from the dictionary of flags
    flag = flags[flag_name]

    # Make sure that the row color is different to the color of the hostname
    row_color = color256(flag[1] if flag[0] != flag[1] else flag[2], "fg")

    # Set default stats to show
    show_stats = show_stats or ["os", "pkgs", "kernel", "uptime"]

    # Initalise the fetch data (system info) to be displayed with the user@hostname
    row_data = [
        f"{color256(flag[0], 'fg') if flag[0] != 0 else color256(242, 'fg')}"
        f"\033[1m{getuser()}@{gethostname()}{reset}",
    ]

    # Add the chosen stats to the list row_data
    for stat in show_stats:
        value = stats[stat]
        row = f"{row_color}{stat}: {reset}{value}"
        row_data.append(row)

    # Until the flag is a greater length than the data
    while len(flag) < len(row_data):
        # If the data is greater than the flag length then duplicate the length of the flag
        flag = [element for element in flag for _ in (0, 1)]

    # Set the width of the flag relative to its height (keep it in a ratio)
    width = width or round(len(flag) * 1.5 * 3)

    # Ensures nothing is printed for empty lines
    row_data.append("")

    # Return all the flag information ready for drawing
    return flag, width, row_data

def draw_fetch(flag: list, width: int, row_data: list):
    # Print a blank line to separate the flag from the terminal prompt
    print()

    for index, row in enumerate(flag):
        # Print out each row of the fetch
        print(f" {color256(row, 'bg')}{' ' * width}\033[49m{reset} {row_data[min(index, len(row_data) - 1)]}{reset}")

    # Print a blank line again to separate the flag from the terminal prompt
    print()


def main():
    # Argument configuration - options
    parser = ArgumentParser()
    parser.add_argument("-f", "--flag", help="displays the chosen flag")
    parser.add_argument("-r", "--random", help="randomly choose a flag from a comma-seperated list")
    parser.add_argument("-s", "--stats", help="choose the stats to appear from a comma-seperated list")
    parser.add_argument("-w", "--width", help="choose a custom width for the flag", type=int)
    parser.add_argument("-l", "--list", help="lists all the flags and stats that can be displayed", action="store_true")

    # Parse (collect) any arguments
    args = parser.parse_args()

    if args.stats:
        # Collect chosen stats if they exist
        show_stats = args.stats.split(",")

    else:
        # Otherwise, use the default stats
        show_stats = None

    if args.flag:
        # Check if the flag exists in the dictionary of flags
        assert args.flag in flags.keys(), f"flag '{args.flag}' is not a valid flag"

        # Draw the chosen flag and system information
        flag, width, row_data = calc_fetch(args.flag, show_stats, args.width)
        draw_fetch(flag, width, row_data)

    elif args.random:
        # Choose a flag at random from a list of comma-seperated flags
        flag_choices = args.random.split(",")
        flag, width, row_data = calc_fetch(random_choice(flag_choices), show_stats, args.width)
        draw_fetch(flag, width, row_data)

    elif args.list:
        # List out all the available flags
        print(f"{bold}Available flags:{reset}\n{', '.join(flags)}\n\n"
              f"{bold}Available stats:{reset}\n{', '.join(stats)}")

    else:
        # By default, draw the classic flag
        flag, width, row_data = calc_fetch("classic", show_stats, args.width)
        draw_fetch(flag, width, row_data)


if __name__ == "__main__":
    main()
