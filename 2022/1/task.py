"""Day 1"""

def gen_list(raw_data):
    """Generate list of the elve's calorie inventory from raw text input"""
    elf_cal_counts = []
    for list_cals in raw_data.split("\n\n"):
        count = 0
        for item in list_cals.split("\n"):
            count += int(item)
        elf_cal_counts.append(count)
    return elf_cal_counts

def pt1(raw_data):
    """part 1"""
    return max(gen_list(raw_data))

def pt2(raw_data, num_top):
    """part 2"""
    list_cals = gen_list(raw_data)

    top_cals = []
    for _ in range(num_top):
        max_cal = max(list_cals)
        top_cals.append(max_cal)
        list_cals.remove(max_cal)

    return sum(top_cals)
