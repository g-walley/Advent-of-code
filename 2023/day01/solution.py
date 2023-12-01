
from pathlib import Path


def pt1(raw_input: Path):
    """part 1"""
    lines = raw_input.read_text().splitlines()
    # get all digits
    total = 0
    for line in lines:
        numerical = "".join(char for char in line if char.isdigit())
        total += int(numerical[0] + numerical[-1])

    return total

def pt2(raw_input: Path):
    """part 2"""