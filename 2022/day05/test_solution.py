"""Tests for solution"""

from pathlib import Path
from shared_test import AOCTest
from day05.solution import pt1, pt2

class TestCase(AOCTest):
    """Test case for Day 1"""
    ex_crates = "2022/day05/example_crates.txt"
    ex_instr = "2022/day05/example_instructions.txt"
    in_crates = "2022/day05/input_crates.txt"
    in_instr = "2022/day05/input_instructions.txt"

    def test_example_part_1(self):
        """Input example data to part 1"""
        self.assertEqual(
            pt1(
                Path(self.ex_crates).read_text(encoding="utf8"),
                Path(self.ex_instr).read_text(encoding="utf8"),
            ),
            "CMZ"
        )

    def test_example_part_2(self):
        """Input example data to part 2"""
        self.assertEqual(
            pt2(
                Path(self.ex_crates).read_text(encoding="utf8"),
                Path(self.ex_instr).read_text(encoding="utf8"),
            ),
            "MCD"
        )

    def test_input_part_1(self):
        """Test Created with answer to allow for refactoring."""
        self.assertEqual(
            pt1(
                Path(self.in_crates).read_text(encoding="utf8"),
                Path(self.in_instr).read_text(encoding="utf8"),
            ),
            "FWNSHLDNZ",
        )


    def test_input_part_2(self):
        """Test Created with answer to allow refactoring"""
        self.assertEqual(
            pt2(
                Path(self.in_crates).read_text(encoding="utf8"),
                Path(self.in_instr).read_text(encoding="utf8"),
            ),
            "RNRGDNFQG"
        )
