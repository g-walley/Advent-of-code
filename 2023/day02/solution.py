from __future__ import annotations
from pathlib import Path
from dataclasses import dataclass as dc

@dc
class Draw:
    red: int = 0
    green: int = 0
    blue: int = 0

    def __init__(self, raw_string: str):
        cube_types = raw_string.split(",")
        for cube_type in cube_types:
            num = int(cube_type.strip().split(" ")[0])
            if "red" in cube_type:
                self.red = num
            if "green" in cube_type:
                self.green = num
            if "blue" in cube_type:
                self.blue = num


    def __gt__(self, other: Draw):
        if self.red > other.red:
            return True
        if self.green > other.red:
            return True
        if self.blue > other.blue:
            return True

    def __eq__(self, other: Draw):
        return (
            self.red == other.red and
            self.blue == other.blue and
            self.green == other.green
        )

class Game:
    id: int
    drawn: list[Draw]

    def __init__(self, raw_string: str):
        split = raw_string.split(":")
        self.raw = split[1]
        self.id = int(split[0].strip("Game "))

        self.drawn = [Draw(s) for s in self.raw.split(";")]

    @property
    def max_blue(self):
        return max(drawn.blue for drawn in self.drawn)

    @property
    def max_red(self):
        return max(drawn.red for drawn in self.drawn)

    @property
    def max_green(self):
        return max(drawn.green for drawn in self.drawn)

def pt1(raw_input: Path) -> int:
    """part 1"""
    lines = raw_input.read_text().splitlines()
    games = [Game(line) for line in lines]
    max_draw = Draw("12 red, 13 green, 14 blue")
    valid = [
        game.id
        for game in games
        if game.max_blue <= max_draw.blue and
        game.max_green <= max_draw.green and
        game.max_red <= max_draw.red
    ]

    return sum(valid)

def pt2(raw_input: Path):
    """part 2"""
