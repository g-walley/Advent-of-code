"""
Notes:

ROCK: A X 1
PAPER: B Y 2
SCISSORS: C Z 3

Win: 6, draw: 3, loss: 0

A < B < C < A
A A
A B
A C
B A
B B
B C
C A
C B
C C
"""

WIN_LOSS_SCORES = {
    "A X": 3,
    "A Y": 6,
    "A Z": 0,
    "B X": 0,
    "B Y": 3,
    "B Z": 6,
    "C X": 6,
    "C Y": 0,
    "C Z": 3,
}
RPS_SCORE = {"X": 1, "Y": 2, "Z": 3}

def pt1(raw_data: str):
    """Part 1"""
    return sum([
        WIN_LOSS_SCORES[game] + RPS_SCORE[game[-1]]
        for game in raw_data.splitlines()
    ])

ABC_SCORE = {"A": 1, "B": 2, "C": 3}
GAME_SCORES = {'X': 0, 'Y': 3, 'Z': 6}
OPTION = {
    'X': {'A': 'C','B': 'A', 'C': 'B'},
    'Y': {'A': 'A','B': 'B', 'C': 'C'},
    'Z': {'A': 'B','B': 'C', 'C': 'A'},
}
def pt2(raw_data: str):
    """Part 2"""
    return sum([
        GAME_SCORES[game[-1]] + ABC_SCORE[OPTION[game[-1]][game[0]]]
        for game in raw_data.splitlines()
    ])

