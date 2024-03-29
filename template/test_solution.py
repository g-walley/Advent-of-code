"""Tests for solution"""

from pathlib import Path
from shared_test import AOCTest
from <dayXX>.solution import pt1, pt2

class TestCase(AOCTest):
    """Test case for Day 1"""
    ex = "2023/<dayXX>/example.txt"
    in_path = "2023/<dayXX>/input.txt"

    def test_example_part_1(self):
        """Input example data to part 1"""
        self.assertEqual(
            pt1(Path(self.ex)),
            0
        )

    # def test_example_part_2(self):
    #     """Input example data to part 2"""
    #     self.assertEqual(
    #         pt2(Path(self.ex)),
    #         ,
    #     )

    # def test_input_part_1(self):
    #     """Test Created with answer to allow for refactoring."""
    #     self.assertEqual(
    #         pt1(Path(self.in_path)),
    #         7811,
    #     )

    # def test_input_part_2(self):
    #     """Test Created with answer to allow refactoring"""
    #     self.assertEqual(
    #         pt2(Path(self.in_path)),
    #         2639,
    #     )
