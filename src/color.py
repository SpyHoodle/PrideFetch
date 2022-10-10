# ASCII color codes for text
clear = "\033[0m\033[39m"
bold = "\033[1m"
red = "\033[31m"


def color256(col: int, bg_fg: str) -> str:
    # Alias to avoid manually typing out escape codes every time for flags
    return f"\033[{48 if bg_fg == 'bg' else 38};5;{col}m"

