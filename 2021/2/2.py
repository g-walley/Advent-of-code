from pathlib import Path


def main() -> None:

    in_file = Path("./2/input.txt")
    in_list = in_file.read_text(encoding="utf-8").splitlines()
    depth = 0
    aim = 0
    forward = 0
    for movement in in_list:
        split = movement.split(sep=" ")
        dist = int(split[-1])
        direction = split[0]
        if direction == "forward":
            forward += dist
            depth += dist*aim
        elif direction == "down":
            aim += dist
        elif direction == "up":
            aim -= dist
        else:
            raise ValueError(f"Input unexpected: {direction}")

    print(depth*forward)


if __name__ == "__main__":
    main()