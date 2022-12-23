from helpers import helpers
from collections import deque
import numpy

NEIGHBORS = [(1, 0), (1, 1), (0, 1), (-1, 1), (-1, 0), (-1, -1), (0, -1), (1, -1)]

DIRECTIONS = {"N": [(-1, -1), (0, -1), (1, -1)],
              "S": [(1, 1), (0, 1), (-1, 1)],
              "W": [(-1, -1), (-1, 0), (-1, 1)],
              "E": [(1, -1), (1, 0), (1, 1)]}

MOVING_DIRECTIONS = {"N": (0, -1),
                     "S": (0, 1),
                     "W": (-1, 0),
                     "E": (1, 0)}


def parse_input_map(input_text):
    elf_map = set()
    elf_count = 0
    for y, line in enumerate(input_text):
        for x, char in enumerate(line):
            if char == "#":
                elf_map.add((x + 100, y + 100))
                elf_count += 1
    return elf_map, elf_count


def visualize_map(elf_map):
    min_x, max_x = min([item[0] for item in elf_map]), max([item[0] for item in elf_map])
    min_y, max_y = min([item[1] for item in elf_map]), max([item[1] for item in elf_map])
    for y in range(min_y, max_y + 1):
        print(str(y).zfill(4)+ " ", end="")
        for x in range(min_x, max_x + 1):
            if (x, y) in elf_map:
                print("#", end="")
            else:
                print(".", end="")
        print("")
    print("")


def calculate_score(elf_map):
    min_x, max_x = min([item[0] for item in elf_map]), max([item[0] for item in elf_map])
    min_y, max_y = min([item[1] for item in elf_map]), max([item[1] for item in elf_map])
    score = 0
    for y in range(min_y, max_y + 1):
        for x in range(min_x, max_x + 1):
            if (x, y) not in elf_map:
                score += 1
    return score


def do_the_elfman(elf_map, directions):
    new_elf_map = set()
    proposed = {}
    for elf in elf_map:
        has_neighbor = False
        for neighbor in NEIGHBORS:
            considered_coord = tuple(numpy.add(elf, neighbor))
            if considered_coord in elf_map:
                has_neighbor = True
                break
        if not has_neighbor:
            new_elf_map.add(elf)
            continue
        staying_put = True
        for direction in directions:
            crowded = False
            for neighbor in DIRECTIONS[direction]:  # check to see if there's someone there
                considered_coord = tuple(numpy.add(neighbor, elf))
                if considered_coord in elf_map:
                    crowded = True
                    break
            if not crowded:
                proposed_coord = tuple(numpy.add(elf, MOVING_DIRECTIONS[direction]))
                if proposed_coord in proposed:
                    proposed[proposed_coord].append(elf)
                else:
                    proposed[proposed_coord] = [elf]
                    staying_put = False
                break
        if staying_put:
            new_elf_map.add(elf)
    for proposed_coord in proposed:
        if len(proposed[proposed_coord]) == 1:
            new_elf_map.add(proposed_coord)
        else:
            for elf in proposed[proposed_coord]:
                new_elf_map.add(elf)
    return new_elf_map


def part_one(input_filename):
    input = helpers.parse_input(input_filename)
    elf_map, elf_count = parse_input_map(input)
    directions = deque(["N", "S", "W", "E"])
    for round in range(10):
        new_elf_map = do_the_elfman(elf_map, directions)
        elf_map = new_elf_map
        directions.rotate(-1)
    return calculate_score(elf_map)


def part_two(input_filename):
    input = helpers.parse_input(input_filename)
    elf_map, elf_count = parse_input_map(input)
    directions = deque(["N", "S", "W", "E"])
    for round in range(10000000000):
        new_elf_map = do_the_elfman(elf_map, directions)
        if elf_map == new_elf_map:
            return round + 1
        elf_map = new_elf_map
        directions.rotate(-1)
    return calculate_score(elf_map)


if __name__ == "__main__":
    print("*** PART ONE ***\n")
    print(f"Test result = {part_one('inputtest2.txt')}\n")
    print(f"Test result = {part_one('inputtest.txt')}\n")
    print(f"REAL RESULT = {part_one('input.txt')}\n\n")
    print("*** PART TWO ***\n")
    print(f"Test result = {part_two('inputtest.txt')}\n")
    print(f"REAL RESULT = {part_two('input.txt')}")
