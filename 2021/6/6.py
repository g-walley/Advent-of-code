import numpy as np

def get_fish_population(days, initial_pop) -> np.int64:
    """Fish population modelled with a shift register style approach.
    I group each fish based on when it will breed next
    The example:
        initial population = [3, 4, 3, 1 ,2]
        Which means there is one fish with 1,
                             one fish with 2,
                             two fish with 3,
                             one fish with 4.
        This is represented like this:
        fish_population = [0, 1, 1, 2, 1, 0, 0, 0, 0]
        Each day, I roll the whole array to the left by 1.

        This automatically moves the fish at 0 to 8, which deals with
        adding new fish to the pool, and then I manually add the quantity
        of fish at 8 to position 6, which is the same as resetting the
        breeding timer for the fish to 6.

        The population array would unfold as follows:
        Day 0: [0, 1, 1, 2, 1, 0, 0, 0, 0]
        Day 1: [1, 1, 2, 1, 0, 0, 0, 0, 0]
        Day 2: [1, 2, 1, 0, 0, 0, 1, 0, 1]
                                  ^ old fish go here
                                        ^ new fish go here
        Day 3: [2, 1, 0, 0, 0, 1, 1, 1, 1]
        Day 4: [1, 0, 0, 0, 1, 1, 3, 1, 2]
        Day 5: [0, 0, 0, 1, 1, 3, 2, 2, 1]
        etc..

        To get the total population, we sum the array.
        """

    fish_population = np.zeros(shape=9, dtype=np.int64)
    unique, counts = np.unique(initial_pop, return_counts=True)

    for uni, count in dict(zip(unique, counts)).items():
        fish_population[uni] = count

    for _ in range(days):
        fish_population = np.roll(fish_population, -1)
        fish_population[6] += fish_population[8]

    return np.sum(fish_population)

if __name__ == "__main__":
    # PART 1
    NUM_DAYS = 80
    ex1=get_fish_population(
        days=NUM_DAYS,
        initial_pop=np.array([3,4,3,1,2])
    )
    p1=get_fish_population(
        days=NUM_DAYS,
        initial_pop=np.loadtxt(
            "./6/input.txt",
            delimiter = ",",
            dtype=np.int64
        )
    )
    print(f"ex: {ex1}")
    print(f"part1: {p1}")

    # PART 2
    NUM_DAYS = 256
    ex2=get_fish_population(
        days=NUM_DAYS,
        initial_pop=np.array([3,4,3,1,2])
    )
    p2=get_fish_population(
        days=NUM_DAYS,
        initial_pop=np.loadtxt(
            "./6/input.txt",
            delimiter = ",",
            dtype=np.int64
        )
    )
    print(f"ex: {ex2}")
    print(f"part2: {p2}")
