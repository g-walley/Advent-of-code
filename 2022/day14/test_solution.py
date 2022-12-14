"""Tests for solution"""

from pathlib import Path
from shared_test import AOCTest
from day14.solution import pt1, pt2


class TestCase(AOCTest):
    """Test case for Day 1"""

    ex = "2022/day14/example.txt"
    in_path = "2022/day14/input.txt"

    def test_example_part_1(self):
        """Input example data to part 1"""
        self.assertEqual(pt1(Path(self.ex)), 24)

    def test_example_part_2(self):
        """Input example data to part 2"""
        self.assertEqual(
            pt2(Path(self.ex)),
            93,
        )

    def test_input_part_1(self):
        """Test Created with answer to allow for refactoring."""
        self.assertEqual(
            pt1(Path(self.in_path)),
            805,
        )

    def test_input_part_2(self):
        """Test Created with answer to allow refactoring"""
        self.assertEqual(
            pt2(Path(self.in_path)),
            25161,
        )


""" Notes for refactoring:

fell left

0o
next can start the algorithm from diagonal up and right of that position.

start here:
 x
0o

fell right

oo0
start here:
 x
000

couldn't fall anywhere, start
 x
 0
ooo
"""
