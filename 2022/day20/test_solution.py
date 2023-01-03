"""Tests for solution"""

from pathlib import Path
from shared_test import AOCTest
from day20.solution import pt1, pt2

class TestCase(AOCTest):
    """Test case for Day 1"""
    ex = "2022/day20/example.txt"
    ex_2 = "2022/day20/example_2.txt"
    in_path = "2022/day20/input.txt"

    def test_example_part_1(self):
        """Input example data to part 1"""
        self.assertEqual(
            pt1(Path(self.ex)),
            3
        )

    def test_example_2_part_1(self):
        self.assertEqual(
            pt1(Path(self.ex_2)),
            15
        )

    def test_example_part_2(self):
        """Input example data to part 2"""
        self.assertEqual(
            pt2(Path(self.ex)),
            1623178306,
        )

    def test_input_part_1(self):
        """Test Created with answer to allow for refactoring."""
        self.assertEqual(
            pt1(Path(self.in_path)),
            13289,
        )

    def test_input_part_2(self):
        """Test Created with answer to allow refactoring"""
        self.assertEqual(
            pt2(Path(self.in_path)),
            2865721299243,
        )
