from pathlib import Path

def main() -> None:
    """higher/lower"""
    in_file = Path("./input.txt")
    in_list = [int(num) for num in in_file.read_text(encoding="utf-8").splitlines()]

    count = 0
    other = 0
    for index, num in enumerate(in_list):
        if index > 0:
            if num > in_list[index-1]:
                count += 1
            else:
                other += 1

    if (count + other + 1) == len(in_list):
        print("all good")

    print(f"Count: {count}")

if __name__ == "__main__":
    main()