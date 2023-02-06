from subprocess import check_output

class PackagesCommand:
    def __init__(self, command: str, adjust_amt: int = 0):
        """
        Represents a command that retries a newline seperated list of all packages on the system.
        :param command: the command to run
        :param adjust_amt: the amount to add/remove to the number reported by the command
        """
        self.command = command
        self.adjust_amt = adjust_amt

packages_commands: list[PackagesCommand] = [
    PackagesCommand("pacman -Qq --color never"),  # Arch Linux
    PackagesCommand("dpkg-query -f '.\n' -W"),  # Debian, Ubuntu, Mint
    PackagesCommand("dnf list installed -q", -1),  # Fedora, RHEL
    PackagesCommand("yum list installed -q", -1),  # RHEL, Fedora Core, CentOS
    PackagesCommand("rpm -qa"),  # RHEL, Fedora Core, CentOS
    PackagesCommand("xbps-query -l"),  # Void Linux
    PackagesCommand("zypper search -i"),  # openSUSE
    PackagesCommand("kiss l"),  # KISS Linux
    PackagesCommand("equery list '*'"),  # Gentoo
    PackagesCommand("qlist -I"),  # Gentoo
    PackagesCommand("pkg info -a"),  # BSDs
    PackagesCommand("pkg_info"),  # BSDs
    PackagesCommand("apk info"),  # Alpine
    PackagesCommand("nix-store -qR /run/current-system/sw"),  # Nix
]

def get_num_packages() -> (int, bool):
    for packages_command in packages_commands:
        try:
            # Get the length of the output of the command - the number of packages
            return len(check_output(packages_command.command.split(" ")).decode("utf-8").split("\n")) - 1 + packages_command.adjust_amt

        except FileNotFoundError:
            # If the command doesn't exist, skip it
            pass

    # If we get here, we didn't find any of the commands
    return False
