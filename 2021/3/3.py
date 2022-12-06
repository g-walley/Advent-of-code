from typing import Dict
import numpy as np
from copy import deepcopy
from scipy import stats

def pt1() -> int:
    """Part 1"""
    bin_data = np.genfromtxt('./3/input.csv')
    modes = stats.mode(bin_data)
    gamma = ""
    epsilon = ""
    for elem in modes.mode[0]:
        digit = str(int(elem))
        gamma += digit
        if digit == "1":
            epsilon += "0"
        else:
            epsilon += "1"
    return int(gamma, 2) * int(epsilon, 2)


def pt2() -> int:
    """Part 2"""
    def remove_rows(dataset: Dict) -> None:
        """given a dataset, removes rows"""
        dataset["data"] = np.delete(dataset["data"], dataset["to_remove"], axis=0)
        dataset["to_remove"] = []
        dataset["rows"] = np.shape(dataset["data"])[0]
        dataset["columns"] = np.shape(dataset["data"])[1]
        dataset["mode"] = stats.mode(dataset["data"])

    def compress_arr(arr) -> int:
        """given a single array, calculates value"""
        array_str = ""
        for elem in arr:
            array_str += str(int(elem))

        return int(array_str, 2)

    bin_data = np.genfromtxt('./3/input.csv')

    oxygen = {
        "data": deepcopy(bin_data),
        "rows": np.shape(bin_data)[0],
        "to_remove": [],
        "columns": np.shape(bin_data)[1],
        "mode": stats.mode(bin_data),
    }
    carbon = {
        "data": deepcopy(bin_data),
        "rows": np.shape(bin_data)[0],
        "to_remove": [],
        "columns": np.shape(bin_data)[1],
        "mode": stats.mode(bin_data),
    }

    for col in range(oxygen["columns"]):
        counts = oxygen["mode"].count[0][col]
        rows = oxygen["rows"]
        mode = oxygen["mode"].mode[0][col]

        if counts > float(rows)/2:
            to_keep = mode
        else:
            to_keep = 1.0

        for index, row in enumerate(oxygen["data"]):
            if row[col] != to_keep:
                oxygen["to_remove"].append(index)

        remove_rows(oxygen)

    oxygen_val = compress_arr(oxygen["data"][0])

    for col in range(carbon["columns"]):
        counts = carbon["mode"].count[0][col]
        rows = carbon["rows"]
        mode = carbon["mode"].mode[0][col]

        if counts == rows:
            to_keep = mode
        elif counts > float(rows)/2:
            to_keep = 1 - mode
        else:
            to_keep = 0.0

        for index, row in enumerate(carbon["data"]):
            if row[col] != to_keep:
                carbon["to_remove"].append(index)

        remove_rows(carbon)

    carbon_val = compress_arr(carbon["data"][0])
    return carbon_val * oxygen_val


if __name__ == "__main__":
    p1 = pt1()
    p2 = pt2()

    print(f"part1: {p1}")
    print(f"part2: {p2}")