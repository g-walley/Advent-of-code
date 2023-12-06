from dataclasses import dataclass
from pathlib import Path


@dataclass
class Mapping:
    src: int
    dst: int
    rng: int

    def convert(self, num: int) -> int:
        if ((self.src <= num) and (num < self.src + self.rng)):
            return self.dst + (num - self.src) 
        else:
            return num

def algo(line_dict, seeds):
    mapping_names = list(line_dict)
    mapping_names.remove("seeds")

    mappings: list[list[Mapping]] = []
    
    
    for key in mapping_names:
        set_of_mappings = []
        for number_range in line_dict[key]:
            to_min, from_min, span = tuple(map(int, number_range.split()))
            set_of_mappings.append(Mapping(from_min, to_min, span))
        
        mappings.append(set_of_mappings)

    converted_nums = []
    for seed in seeds:
        num = seed
        for set_of_mappings in mappings:
            converted = [ 
                conv 
                for mapping in set_of_mappings 
                if (conv := mapping.convert(num)) != num
            ]
            num = converted[0] if converted else num
        converted_nums.append(num)

    return min(converted_nums)    

def pt1(raw_input: Path):
    """part 1"""
    lines = raw_input.read_text().split("\n\n")

    line_dict = {
        line.split(":")[0].strip(): line.split(":")[1].strip().splitlines()
        for line in lines
    }
    seeds = [int(num) for num in line_dict["seeds"][0].split()]

    return algo(line_dict, seeds)


def pt2(raw_input: Path):
    """part 2"""
    lines = raw_input.read_text().split("\n\n")

    line_dict = {
        line.split(":")[0].strip(): line.split(":")[1].strip().splitlines()
        for line in lines
    }
    seeds = [int(num) for num in line_dict["seeds"][0].split()]
    full_seeds = []
    while seeds:
        x = seeds.pop(0)
        r = seeds.pop(0)
        full_seeds.extend(range(x, x+r))

    print(f"Number of Seeds: {len(full_seeds)}")
    return algo(line_dict, full_seeds)