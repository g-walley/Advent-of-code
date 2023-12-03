from pathlib import Path
import re
from string import digits


def pt1(raw_input: Path):
    """part 1"""
    # Get length of lines:
    lines = raw_input.read_text().splitlines()
    shape = (len(lines[0]), len(lines))

    total = 0
    for line_idx, line in enumerate(lines):
        matches = re.finditer(r"\d+", line)
        for match in matches:
            span = match.span()
            h_min = 0 if (span[0] == 0) else span[0] - 1
            h_max = shape[0] if (span[1] == shape[0]) else span[1] + 1
            v_min = 0 if (line_idx == 0) else line_idx - 1
            v_max = shape[1] if (line_idx == shape[1]) else line_idx + 1

            relevant_lines = lines[v_min : v_max + 1]

            section = "".join([line[h_min:h_max] for line in relevant_lines])
            remove_digits = str.maketrans("", "", digits)
            remove_full_stops = str.maketrans("", "", ".")
            result = section.translate(remove_digits)
            result = result.translate(remove_full_stops)
            if result:
                total += int(match.group())
    return total


def pt2(raw_input: Path):
    """part 2"""
