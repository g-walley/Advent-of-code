from __future__ import annotations
from collections import deque
from dataclasses import dataclass
from pathlib import Path
from typing import Deque, List, Tuple
from parse import parse


@dataclass(frozen=True)
class Point2D:
    x: int
    y: int

    def taxicab(self, other: Point2D):
        return abs(other.x - self.x) + abs(other.y - self.y)


@dataclass(frozen=True)
class Slice:
    min: int
    max: int


@dataclass(frozen=True)
class Sensor:
    id: int
    at: Point2D
    beacon: Point2D

    def __hash__(self):
        return self.id

    @property
    def distance_to_beacon(self) -> int:
        return self.at.taxicab(self.beacon)

    def horizontal_slice(self, row) -> Slice | None:
        if (abs_dist := self.distance_to_beacon - abs(row - self.at.y)) < 0:
            return None
        return Slice(
            min=self.at.x - abs_dist,
            max=self.at.x + abs_dist,
        )

    def vertical_slice(self, col) -> Slice:
        vertical_dist = self.distance_to_beacon - abs(col - self.at.x)
        return Slice(
            min=self.at.y - vertical_dist,
            max=self.at.y + vertical_dist,
        )


def parse_sensor_data(raw_input: Path) -> List[Sensor]:
    sensors: List[Sensor] = []
    for idx, line in enumerate(raw_input.read_text(encoding="utf-8").splitlines()):
        parsed_line = parse(
            "Sensor at x={s_x}, y={s_y}: closest beacon is at x={b_x}, y={b_y}", line
        )
        sensor = Sensor(
            id=idx,
            at=Point2D(
                x=int(parsed_line["s_x"]),
                y=int(parsed_line["s_y"]),
            ),
            beacon=Point2D(
                x=int(parsed_line["b_x"]),
                y=int(parsed_line["b_y"]),
            ),
        )
        sensors.append(sensor)

    return sensors


def compress_slices(slices: Deque[Slice]) -> Deque[Slice]:
    s1 = slices.popleft()
    s2 = slices.popleft()

    if s2.min <= (s1.max + 1):
        slices.appendleft(Slice(s1.min, max(s1.max, s2.max)))
        if len(slices) > 1:
            return compress_slices(slices)
        else:
            return slices
    elif not slices:
        slices.extend([s1, s2])
        return slices
    else:
        # hold on to that left most one, it needs to be added again later
        slices.appendleft(s2)
        slices = compress_slices(slices)
        slices.appendleft(s1)
        return slices

    assert False, "Something went really wrong in compress_slices"


def pt1(raw_input: Path, y_row: int):
    """part 1"""
    sensors = parse_sensor_data(raw_input)
    beacons = set([sensor.beacon for sensor in sensors if sensor.beacon.y == y_row])

    slices = []
    for sensor in sensors:
        if (slice := sensor.horizontal_slice(y_row)) is not None:
            slices.append(slice)

    sorted_slices: List[Slice] = sorted(slices, key=lambda x: x.min)
    non_overlapping_slices = list(compress_slices(deque(sorted_slices)))

    total = 0
    for slice in non_overlapping_slices:
        total += (slice.max + 1) - slice.min

    total -= len(beacons)
    return total


def pt2(raw_input):
    """part 2"""
    sensors = parse_sensor_data(raw_input)
    m = 4000000
    for y in range(m + 1):
        slices = []
        for sensor in sensors:
            if (slice := sensor.horizontal_slice(y)) is not None:
                slices.append(slice)
        sorted_slices: List[Slice] = sorted(slices, key=lambda x: x.min)
        non_overlapping_slices = list(compress_slices(deque(sorted_slices)))
        if (l := len(non_overlapping_slices)) == 1:
            x = 0
            continue
        elif l == 2:
            x = non_overlapping_slices[0].max + 1
            break

        assert 0 < l and l <= 2, f"l has value {l}, {non_overlapping_slices}, {y}"
        assert False, "Shouldn't have made it to the end"

    return (x * m) + y
