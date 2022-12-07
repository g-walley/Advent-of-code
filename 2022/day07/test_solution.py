"""Tests for solution"""

from pathlib import Path
from shared_test import AOCTest
from day07.solution import pt1, pt2

class TestCase(AOCTest):
    """Test case for Day 1"""
    ex = "2022/day07/example.txt"
    in_path = "2022/day07/input.txt"

    def test_example_part_1(self):
        """Input example data to part 1"""
        self.assertEqual(
            pt1(Path(self.ex).read_text(encoding="utf8")),
            95437,
        )

    def test_example_part_2(self):
        """Input example data to part 2"""
        self.assertEqual(
            pt2(Path(self.ex).read_text(encoding="utf8")),
            24933642,
        )

    def test_input_part_1(self):
        """Test Created with answer to allow for refactoring."""
        self.assertEqual(
            pt1(Path(self.in_path).read_text(encoding="utf8")),
            1501149,
        )

    def test_input_part_2(self):
        """Test Created with answer to allow refactoring"""
        self.assertEqual(
            pt2(Path(self.in_path).read_text(encoding="utf8")),
            10096985,
        )
