from collections import deque
from pathlib import Path

def pt1(raw_input: Path):
    """part 1"""
    nums = []
    for number in raw_input.read_text(encoding="utf-8").splitlines():
        nums.append(int(number))

    d = deque([(idx, num) for idx, num in enumerate(nums)])

    for idx, num in enumerate(nums):
        d.rotate(-d.index((idx, num)))
        _ = d.popleft()
        d.rotate(-num)
        d.appendleft((idx, num))

    _, c = d[0]
    while c != 0:
        d.rotate(-1)
        _, c = d[0]

    out = []
    for _ in range(3):
        d.rotate(-1000)
        out.append(d[0][1])

    return sum(out)

KEY = 811589153

def pt2(raw_input):
    """part 2"""
    nums = []
    for number in raw_input.read_text(encoding="utf-8").splitlines():
        nums.append(int(number) * KEY)

    d = deque([(idx, num) for idx, num in enumerate(nums)])

    for _ in range(10):
        for idx, num in enumerate(nums):
            d.rotate(-d.index((idx, num)))
            _ = d.popleft()
            d.rotate(-num)
            d.appendleft((idx, num))

    _, c = d[0]
    while c != 0:
        d.rotate(-1)
        _, c = d[0]

    out = []
    for _ in range(3):
        d.rotate(-1000)
        out.append(d[0][1])

    return sum(out)