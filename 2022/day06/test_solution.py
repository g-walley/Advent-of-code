"""Tests for solution"""

from pathlib import Path
from shared_test import AOCTest
from day06.solution import pt1, pt2

class TestCase(AOCTest):
    """Test case for Day 1"""
    ex = {
        "mjqjpqmgbljsphdztnvjfqwrcgsmlb": 7,
        "bvwbjplbgvbhsrlpgdmjqwftvncz": 5,
        "nppdvjthqldpwncqszvftbrmjlhg": 6,
        "nznrnfrfntjfmvfwmzdfjlvtqnbhcprsg": 10,
        "zcfzfwzzqfrljwzlrfnpqdbhtmscgvjw": 11,
    }
    ex_2 = {
        "mjqjpqmgbljsphdztnvjfqwrcgsmlb": 19,
        "bvwbjplbgvbhsrlpgdmjqwftvncz": 23,
        "nppdvjthqldpwncqszvftbrmjlhg": 23,
        "nznrnfrfntjfmvfwmzdfjlvtqnbhcprsg": 29,
        "zcfzfwzzqfrljwzlrfnpqdbhtmscgvjw": 26,
    }
    in_path = "2022/day06/input.txt"

    def test_example_pt1(self):
        """Input example data to part 1"""
        for k, v in self.ex.items():
            with self.subTest(i = k):
                self.assertEqual(pt1(k), v)


    def test_example_part_2(self):
        """Input example data to part 2"""
        for k, v in self.ex_2.items():
            with self.subTest(i = k):
                self.assertEqual(pt2(k), v)

    def test_input_part_1(self):
        """Test Created with answer to allow for refactoring."""
        self.assertEqual(
            pt1(Path(self.in_path).read_text(encoding="utf8")),
            1361,
        )

    def test_input_part_2(self):
        """Test Created with answer to allow refactoring"""
        self.assertEqual(
            pt2(Path(self.in_path).read_text(encoding="utf8")),
            3263,
        )
