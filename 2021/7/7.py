import numpy as np
from functools import wraps
from datetime import datetime

def timeit(func):
    '''a decorator function to calculate the time taken to run the code'''
    @wraps(func)
    def newfunc(*args, **kwargs):
        startTime = datetime.now()
        func(*args, **kwargs)
        elapsedTime = datetime.now() - startTime
        print('function [{}] finished in {} us'.format(
            func.__name__, int(elapsedTime.microseconds)))
        return elapsedTime
    return newfunc


# @timeit
def pt1(crab_position_data) -> np.int64:
    """Part 1"""
    unique, counts = np.unique(
        np.loadtxt(crab_position_data, delimiter = ",", dtype=np.int64),
        return_counts=True,
    )
    minimum_fuel = np.iinfo(np.int64).max
    pos = 0
    ones = np.ones(shape=len(unique), dtype=np.int64)
    targets = np.zeros(shape=len(unique), dtype=np.int64)

    for position in unique:
        cost = np.multiply(
            counts,
            np.abs(
                np.subtract(
                    targets,
                    unique
                )
            )
        )
        cost = np.sum(cost)
        if cost < minimum_fuel:
            minimum_fuel = cost
            pos = position
        targets = np.add(targets, ones)

    return pos, minimum_fuel

# @timeit
def pt2(crab_position_data) -> int:
    """Part 2"""
    unique, counts = np.unique(
        np.loadtxt(crab_position_data, delimiter = ",", dtype=np.int64),
        return_counts=True,
    )
    minimum_fuel = np.iinfo(np.int64).max
    pos = 0
    ones = np.ones(shape=len(unique), dtype=np.int64)
    twos = np.add(ones, ones)
    targets = np.zeros(shape=len(unique), dtype=np.int64)

    for position in unique:
        distance = np.add(
            np.abs(
                np.subtract(
                    targets,
                    unique
                )
            ),
            ones
        )
        journey_costs = np.divide(
            np.multiply(
                distance,
                np.subtract(
                    distance,
                    ones
                )
            ),
            twos
        )
        cost = np.sum(
            np.multiply(
                counts,
                journey_costs,
            )
        )
        if cost < minimum_fuel:
            minimum_fuel = cost
            pos = position
        targets = np.add(targets, ones)

    return pos, minimum_fuel


if __name__ == "__main__":

    ex1=pt1("./7/example.txt")
    p1=pt1("./7/input.txt")
    ex2=pt2("./7/example.txt")
    p2=pt2("./7/input.txt")

    print(f"ex: {ex1}")
    print(f"part1: {p1}")
    print(f"ex: {ex2}")
    print(f"part2: {p2}")
