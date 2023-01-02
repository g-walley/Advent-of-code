"""Tests for solution"""

from pathlib import Path
from shared_test import AOCTest
from day17.solution import pt1, pt2


class TestCase(AOCTest):
    """Test case for Day 1"""

    ex = "2022/day17/example.txt"
    in_path = "2022/day17/input.txt"

    def test_example_part_1(self):
        """Input example data to part 1"""
        self.assertEqual(pt1(Path(self.ex)), 3068)

    def test_example_part_2(self):
        """Input example data to part 2"""
        self.assertEqual(
            pt2(Path(self.ex)),
            1514285714288,
        )

    def test_input_part_1(self):
        """Test Created with answer to allow for refactoring."""
        self.assertEqual(
            pt1(Path(self.in_path)),
            3055,
        )

    def test_input_part_2(self):
        """Test Created with answer to allow refactoring"""
        self.assertEqual(
            pt2(Path(self.in_path)),
            0,
        )
