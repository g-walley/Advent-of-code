from __future__ import annotations
from pathlib import Path

from dataclasses import dataclass
from typing import Dict


@dataclass(frozen=True)
class Coordinate:
    x: int
    y: int

    def __add__(self, other: Coordinate) -> Coordinate:
        return Coordinate(self.x + other.x, self.y + other.y)


@dataclass(frozen=True)
class Direction(Coordinate):
    @property
    def length(self):
        if self.x == 0:
            return self.y
        if self.y == 0:
            return self.x
        assert False, "Uni-dimensional directions only!"


directions = {
    Direction(0, -1),
    Direction(0, 1),
    Direction(1, 0),
    Direction(-1, 0),
}


@dataclass
class Rectangle:
    width: int
    length: int

    def __post_init__(self):
        assert self.width > 0
        assert self.length > 0


@dataclass
class Tree:
    height: int


@dataclass
class Forest:
    trees: Dict[Coordinate, Tree]  # 🎄
    size: Rectangle


def plant_forest(input_path: Path):
    file_content = input_path.read_text()

    trees = {}
    for y, row in enumerate(file_content.splitlines()):
        for x, height in enumerate(row.strip()):
            trees[Coordinate(x, y)] = Tree(int(height))

    return Forest(trees, size=Rectangle(x + 1, y + 1))


@dataclass
class Ray:
    """A point that moves in a direction at a height, and records distance travelled."""

    position: Coordinate
    height: int
    direction: Direction
    dist: int = 0
    hit: bool = False

    def __post_init__(self):
        assert self.height >= 0
        assert not self.direction.x or not self.direction.y


def trace_ray(forest: Forest, ray: Ray) -> Ray:
    # extend ray in a straight line
    ray.position = ray.position + ray.direction
    # record distance flown
    ray.dist = ray.dist + abs(ray.direction.length)

    # Did we hit a 🧱?
    out_of_bounds_x = (
        ray.position.x < 0 or forest.size.width <= ray.position.x
        if ray.direction.x != 0
        else False
    )
    out_of_bounds_y = (
        ray.position.y < 0 or forest.size.length <= ray.position.y
        if ray.direction.y != 0
        else False
    )
    if out_of_bounds_x or out_of_bounds_y:
        ray.dist -= 1
        return ray

    # Did it hit a 🎄?
    ray.hit = forest.trees[ray.position].height >= ray.height
    if ray.hit:
        return ray
    return trace_ray(forest=forest, ray=ray)


def pt1(input_path: Path):
    """part 1"""
    forest = plant_forest(input_path)
    visible_trees = 0

    for position, tree in forest.trees.items():
        for dir in directions:
            ray = trace_ray(forest=forest, ray=Ray(position, tree.height, dir))
            if not ray.hit:
                visible_trees += 1
                break

    return visible_trees


def pt2(input_path: Path):
    """part 2"""
    forest = plant_forest(input_path)

    max_score = 0
    for position, tree in forest.trees.items():
        score = 1
        for dir in directions:
            ray = trace_ray(forest=forest, ray=Ray(position, tree.height, dir))
            score *= ray.dist

        if score > max_score:
            max_score = score

    return max_score
