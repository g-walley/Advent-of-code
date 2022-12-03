
letter_prio = {
    'a': 1, 'b': 2, 'c': 3, 'd': 4, 'e': 5, 'f': 6,
    'g': 7, 'h': 8, 'i': 9, 'j': 10,'k': 11,'l': 12,
    'm': 13,'n': 14,'o': 15,'p': 16,'q': 17,'r': 18,
    's': 19,'t': 20,'u': 21,'v': 22,'w': 23,'x': 24,
    'y': 25,'z': 26,'A': 27,'B': 28,'C': 29,'D': 30,
    'E': 31,'F': 32,'G': 33,'H': 34,'I': 35,'J': 36,
    'K': 37,'L': 38,'M': 39,'N': 40,'O': 41,'P': 42,
    'Q': 43,'R': 44,'S': 45,'T': 46,'U': 47,'V': 48,
    'W': 49,'X': 50,'Y': 51,'Z': 52,
}

def pt1(raw_input: str):
    """comparing two halfs of each string"""
    shared_items = []
    for backpack in raw_input.splitlines():
        half = int(len(backpack)/2)
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
