from typing import List
import numpy as np
from copy import deepcopy
from scipy import stats
from pathlib import Path


class Bingo(object):
    BOARD_HEIGHT = 5

    def __init__(
        self,
        boards_path: Path,
        number_calls_path: Path,
        board_height=5,
        first=True,
    ) -> None:
        self.numbers = np.loadtxt(str(number_calls_path), delimiter = ",")
        self.first = first
        raw_board_input = np.loadtxt(boards_path)
        split_indexes = [index for index, _ in enumerate(
            raw_board_input) if index % board_height == 0]

        self.boards = np.split(raw_board_input, split_indexes[1:], axis = 0)

        self.board_hits = np.full_like(raw_board_input, fill_value = False, dtype = bool)
        self.board_hits = np.split(self.board_hits, split_indexes[1:], axis=0)
        self.board_winners = []
        self.numbers_at_win = []
        self.score = np.nan

    def execute_game(self) -> np.int64:
        """executes game"""

        for number in self.numbers:
            self._mark_number_matches(number)
            board_winners = self._check_for_board_wins(number)
            if board_winners != [np.nan]:
                self.board_winners.extend(board_winners)

        if self.first:
            board = self.board_winners[0]
            number = self.numbers_at_win[0]
            self.score = self._calculate_score(board, number)
        else:
            board = self.board_winners[-1]
            number = self.numbers_at_win[-1]
            self.score = self._calculate_score(self.board_winners[-1], number)

        return self.score

    def _calculate_score(self, board_index, number):
        """Calculates score"""
        score = 0
        board = self.boards[board_index]
        hit_board = self.board_hits[board_index]

        for row_index, row in enumerate(board):
            for col_index, col in enumerate(row):
                if not hit_board[row_index][col_index]:
                    score += col

        return score * number

    def _mark_number_matches(self, number):
        """Marks a square on the board if it matches a number"""
        for board_index, board in enumerate(self.boards):
            if board_index not in self.board_winners:
                for row_index, row, in enumerate(board):
                    for col_index, col in enumerate(row):
                        if col == number:
                            self.board_hits[board_index][row_index][col_index] = True

    def _check_for_board_wins(self, number) -> List[np.int64]:
        """checks if a board has won, returns board number of np.NA if no winner"""
        winners = []
        for board_index, board in enumerate(self.board_hits):
            if board_index not in self.board_winners:
                row_complete = True in np.all(board, axis=0)
                col_complete = True in np.all(board, axis=1)
                if row_complete or col_complete:
                    winners.append(np.int64(board_index))
                    self.numbers_at_win.append(number)

        if winners == []:
            return [np.nan]
        else:
            return winners


def pt1() -> np.int64:
    """Part 1"""
    boards = Path("./4/bingo_boards.txt")
    number_calls = Path("./4/bingo_calls.csv")
    bingo = Bingo(boards, number_calls, 5)
    return bingo.execute_game()

def pt2() -> int:
    """Part 2"""
    boards = Path("./4/bingo_boards.txt")
    number_calls = Path("./4/bingo_calls.csv")
    bingo = Bingo(boards, number_calls, 5, first=False)
    return bingo.execute_game()

def adi() -> int:
    boards = Path("./4/adi_bingo_boards.txt")
    number_calls = Path("./4/adi_bingo_calls.csv")
    bingo = Bingo(boards, number_calls, 5, first=False)
    return bingo.execute_game()

if __name__ == "__main__":
    p1=pt1()
    p2=pt2()
    ad=adi()

    print(f"part1: {p1}")
    print(f"part2: {p2}")
    print(f"adi: {ad}")
