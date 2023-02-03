from subprocess import check_output

commands = [
    "pacman -Qq --color never",  # Arch Linux
    "dpkg-query -f '.\n' -W",  # Debian, Ubuntu, Mint
    "dnf list installed | tail -n +2",  # Fedora, RHEL
    "rpm -qa",  # RHEL, Fedora Core, CentOS
    "yum list installed | tail -n +2",  # RHEL, Fedora Core, CentOS
    "xbps-query -l",  # Void Linux
    "zypper search -i",  # openSUSE
    "kiss l",  # KISS Linux
    "equery list '*'",  # Gentoo
    "qlist -I",  # Gentoo
    "pkg info -a",  # BSDs
    "pkg_info",  # BSDs
    "apk info",  # Alpine
    "nix-store -qR /run/current-system/sw",  # Nix
]


def get_num_packages() -> (int, bool):
    for command in commands:
        try:
            # Get the length of the output of the command - the number of packages
            return len(check_output(command.split(" ")).decode("utf-8").split("\n")) - 1

        except FileNotFoundError:
            # If the command doesn't exist, skip it
            pass

    # If we get here, we didn't find any of the commands
    return False
