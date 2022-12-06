from pathlib import Path
import numpy as np
from scipy.ndimage.interpolation import shift


def main() -> None:
    """higher/lower"""
    window = 3
    in_file = Path("./input.txt")
    in_list = [int(num) for num in in_file.read_text(encoding="utf-8").splitlines()]
    shifted = np.array(in_list)
    sum = shifted
    for _ in range(window - 1):
        shifted = shift(shifted, -1, cval=0)
        sum = np.add(sum, shifted)

    shifted_sum = shift(sum, -1, cval=0)
    count = np.greater(shifted_sum, sum).sum()
    print(count)


if __name__ == "__main__":
    main()