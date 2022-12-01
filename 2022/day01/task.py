"""Day 1"""

def gen_list(raw_data):
    """Generate list of the elve's calorie inventory from raw text input"""
    return [
        sum(list(map(int, list_cals.split("\n"))))
        for list_cals in raw_data.split("\n\n")
    ]

def pt1(raw_data):
    """part 1"""
    return max(gen_list(raw_data))

def pt2(raw_data, num_top):
    """part 2"""
    return sum(sorted(gen_list(raw_data), reverse=True)[0:3])

