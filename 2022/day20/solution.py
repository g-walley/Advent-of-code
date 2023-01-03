from collections import deque
from pathlib import Path
from typing import Deque, List


def get_input(raw_input: Path, key) -> Deque:
    """Get each number from the file, and store it in a deque with it's index.
    The index is used to help key the item incase there are repeats in the file."""
    return deque(
        [
            (idx, int(num)*key)
            for idx, num in enumerate(
                raw_input.read_text(encoding="utf-8").splitlines()
            )
        ]
    )

def mix(d: Deque, ordering: List) -> Deque:
    """Execute mix algorithm.
    1. Find location of the item that is moving and rotate queue so that it is at the left.
    2. Remove it from the queue, and rotate by the amount.
    3. Stick it back on the front of the queue.
    4. Repeat for all numbers."""
    for idx, num in ordering:
        d.rotate(-d.index((idx, num)))
        d.rotate(-d.popleft()[1])
        d.appendleft((idx, num))
    return d

def calc_out(d: Deque) -> int:
    # Remove all idxes from the queue, they are no longer necessary.
    d = deque([num for (_, num) in d])
    # Find the zero, and rotate it to the front.
    d.rotate(-d.index(0))
    # Rotate the deque by 1000 3 times, and sum the numbers at the front.
    out = 0
    for _ in range(3):
        d.rotate(-1000)
        out += d[0]
    return out

def pt1(raw_input: Path):
    """part 1"""
    # Get input
    d = get_input(raw_input, key=1)
    # Mix it up once
    d = mix(d, list(d))
    # Calculate the output
    return calc_out(d)

def pt2(raw_input):
    """part 2"""
    # Get input
    d = get_input(raw_input, key=811589153)
    # Use this list for the ordering of the mixing
    l = list(d)
    # Mix 10 times.
    for _ in range(10):
        d = mix(d, l)
    # Calculate output
    return calc_out(d)
