
from pathlib import Path

DIGIT_MAP = {
    "one": "1",
    "two": "2",
    "three": "3",
    "four": "4",
    "five": "5",
    "six": "6",
    "seven": "7",
    "eight": "8",
    "nine": "9",
    "1": "1",
    "2": "2",
    "3": "3",
    "4": "4",
    "5": "5",
    "6": "6",
    "7": "7",
    "8": "8",
    "9": "9",
}

# DIGITS_LENGTHS = [len(digit) for digit in DIGITS]
# MIN_LEN = min(DIGITS_LENGTHS)
# MAX_LEN = max(DIGITS_LENGTHS)

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
    lines = raw_input.read_text().splitlines()

    total = 0
    for line in lines:
        first_digit = (len(line), "")
        last_digit = (-1, "")
        for d, a  in DIGIT_MAP.items():
            lpos = line.find(d)
            if lpos < first_digit[0] and lpos != -1:
                first_digit = (lpos, a)

            rpos = line.rfind(d)
            if rpos > last_digit[0] and rpos != -1:
                last_digit = (rpos, a)

        total += int(first_digit[1] + last_digit[1])

    return total


