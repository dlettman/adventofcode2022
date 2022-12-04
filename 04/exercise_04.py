import sys
sys.path.append("..")
import helpers

def get_mins_and_maxes(line):
    elf1, elf2 = line.split(",")
    elf1_min, elf1_max = [int(item) for item in elf1.split("-")]
    elf2_min, elf2_max = [int(item) for item in elf2.split("-")]
    return (elf1_min, elf1_max, elf2_min, elf2_max)

def part_one(input_filename):
    input = helpers.parse_input(input_filename)
    containers = 0
    for line in input:
        elf1_min, elf1_max, elf2_min, elf2_max = get_mins_and_maxes(line)
        if (elf1_min <= elf2_min and elf1_max >= elf2_max) or (elf1_min >= elf2_min and elf1_max <= elf2_max):
            containers += 1
    return containers

def part_two(input_filename):
    input = helpers.parse_input(input_filename)
    overlappers = 0
    for line in input:
        elf1_min, elf1_max, elf2_min, elf2_max = get_mins_and_maxes(line)
        e1 = set(range(elf1_min, elf1_max + 1))
        e2 = set(range(elf2_min, elf2_max + 1))
        if e1.intersection(e2):
            overlappers += 1
    return overlappers

if __name__ == "__main__":
    print("*** PART ONE ***\n")
    print(f"Test result = {part_one('inputtest.txt')}\n")
    print(f"REAL RESULT = {part_one('input.txt')}\n\n")
    print("*** PART TWO ***\n")
    print(f"Test result = {part_two('inputtest.txt')}\n")
    print(f"REAL RESULT = {part_two('input.txt')}")
