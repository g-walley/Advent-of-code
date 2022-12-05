import string

letter_prio = {l: idx+1 for idx, l in  enumerate(string.ascii_letters)}

def pt1(raw_input: str):
    """comparing two halfs of each string"""
    shared_items = []
    for backpack in raw_input.splitlines():
        half = len(backpack)//2
        comp_1 = backpack[:half]
        comp_2 = backpack[half:]

        for item in comp_1:
            if item in comp_2:
                shared_items.append(item)
                break

    return sum([
        letter_prio[item]
        for item in shared_items
    ])


def pt2(raw_input: str):
    """comparing 3 strings. Find common char in all"""
    backpacks = raw_input.splitlines()
    groups = int(len(backpacks)/3)
    priorities = []
    for group_number in range(groups):
        group = [
            set(backpack)
            for backpack in backpacks[3*group_number: (3*group_number) + 3]
        ]

        badge = group[0].intersection(group[1]).intersection(group[2])
        assert len(badge) == 1

        priorities.append(letter_prio[badge.pop()])

    return sum(priorities)
