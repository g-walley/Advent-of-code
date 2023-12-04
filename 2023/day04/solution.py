
from dataclasses import dataclass
from pathlib import Path

@dataclass
class Card:
    number: int
    winners: set[int]
    actual: set[int]
    total: int

    def __init__(self, card: str):
        card_number, numbers = card.split(":", 1)
        self.number = int(card_number.split()[1])
        
        winning_numbers, card_numbers = numbers.split("|", 1)
        self.winners = set(map(int, winning_numbers.split()))
        self.actual = set(map(int, card_numbers.split()))
        self.total = 1

    @property
    def matching_numbers(self):
        return len(self.winners.intersection(self.actual))
    
    @property
    def score(self):
        x = self.matching_numbers - 1
        return 2**x if x >= 0 else 0

def parse(raw_input: Path) -> list[Card]:
    cards = raw_input.read_text().strip().splitlines()
    return [Card(card) for card in cards]

def pt1(raw_input: Path):
    """part 1"""
    # Splitting the data into individual cards
    return sum(card.score for card in parse(raw_input))


def pt2(raw_input: Path):
    """part 2"""
    parsed_cards = parse(raw_input)
    for index, card in enumerate(parsed_cards):
        for i in range(index + 1, index + card.matching_numbers + 1):
            parsed_cards[i].total += card.total

    return sum(card.total for card in parsed_cards)