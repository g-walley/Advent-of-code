"""Tests for day 1"""

from pathlib import Path
import unittest
from task import pt1, pt2

class TestCase(unittest.TestCase):
    """Test case for Day 1"""

    def test_example_part_1(self):
        """Input example data to part 1"""
        self.assertEqual(
            pt1(Path("2022/1/example.txt").read_text(encoding="utf8")),
            24000,
        )

    def test_example_part_2(self):
        """Input example data to part 2"""
        self.assertEqual(
            pt2(Path("2022/1/example.txt").read_text(encoding="utf8"), 3),
            45000,
        )

    def test_input_part_1(self):
        """Test Created with answer to allow for refactoring."""
        self.assertEqual(
            pt1(Path("2022/1/input.txt").read_text(encoding="utf8")),
            74394,
        )

    def test_input_part_2(self):
        """Test Created with answer to allow refactoring"""
        self.assertEqual(
            pt2(Path("2022/1/input.txt").read_text(encoding="utf8"), 3),
            212836,
        )
