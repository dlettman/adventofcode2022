from helpers import helpers
import re
import numpy
import time


DIRECTION_MAP = {"L": -1, "R": 1}
ORIENTATIONS = [(1, 0), (0, 1), (-1, 0), (0, -1)]


def parse_map_and_instructions(input_text):
    split_input = input_text.split("\n")
    print(split_input)
    map = {}
    for y, line in enumerate(split_input):
        if line == "":
            break
        for x, char in enumerate(line):
            if char in [".", "#"]:
                map[(x, y)] = char
    instructions = input_text.split("\n\n")[1]
    print(instructions)
    regex_pattern = '(\d+)'
    split_instructions = re.split(regex_pattern, instructions)[1:-1]
    return map, split_instructions


def turn(current_facing: int, direction: str):
    return current_facing + DIRECTION_MAP[direction] % 4


def find_loop_dest(starting_coord, direction, map, max_x, max_y):  # return a coord or -1 if the way is blocked
    print("looping")
    if direction == (1, 0):
        for n in range(max_x):
            if (n, starting_coord[1]) in map:
                if map[(n, starting_coord[1])] == "#":
                    return -1
                else:
                    return (n, starting_coord[1])
    elif direction == (-1, 0):
        for n in range(max_x, 0, -1):
            if (n, starting_coord[1]) in map:
                if map[(n, starting_coord[1])] == "#":
                    return -1
                else:
                    return (n, starting_coord[1])
    if direction == (0, 1):
        for n in range(max_y):
            if (starting_coord[0], n) in map:
                print(starting_coord[0], n, " in map" )
                if map[(starting_coord[0], n)] == "#":
                    return -1
                else:
                    return (starting_coord[0], n)
    elif direction == (0, -1):
        for n in range(max_y, 0, -1):
            if (starting_coord[0], n) in map:
                if map[(starting_coord[0], n)] == "#":
                    return -1
                else:
                    return (starting_coord[0], n)


def find_loop_dest(starting_coord, direction, map, max_x, max_y):  # return a coord or -1 if the way is blocked
    print("looping")
    if direction == (1, 0):
        for n in range(max_x):
            if (n, starting_coord[1]) in map:
                if map[(n, starting_coord[1])] == "#":
                    return -1
                else:
                    return (n, starting_coord[1])
    elif direction == (-1, 0):
        for n in range(max_x, 0, -1):
            if (n, starting_coord[1]) in map:
                if map[(n, starting_coord[1])] == "#":
                    return -1
                else:
                    return (n, starting_coord[1])
    if direction == (0, 1):
        for n in range(max_y):
            if (starting_coord[0], n) in map:
                print(starting_coord[0], n, " in map" )
                if map[(starting_coord[0], n)] == "#":
                    return -1
                else:
                    return (starting_coord[0], n)
    elif direction == (0, -1):
        for n in range(max_y, 0, -1):
            if (starting_coord[0], n) in map:
                if map[(starting_coord[0], n)] == "#":
                    return -1
                else:
                    return (starting_coord[0], n)

def part_one(input_filename):
    with open(input_filename) as file:
        input_text = file.read()
    map, instructions = parse_map_and_instructions(input_text)
    max_x, max_y = max([item[0] for item in map.keys()]), max([item[1] for item in map.keys()])
    print(max_x, max_y)
    current_facing = 0
    current_coord = None
    for n in range(100000):
        if (n, 0) in map:
            current_coord = (n, 0)
            break
    print(current_coord)
    print(ORIENTATIONS[current_facing])
    for instruction in instructions:
        if instruction.isnumeric():
            print(f"Going forward {instruction} paces")
            for n in range(int(instruction)):
                print(current_coord)
                next_coord = tuple(numpy.add(current_coord, ORIENTATIONS[current_facing]))
                if not 0 <= next_coord[0] <= max_x or not 0 <= next_coord[1] <= max_y:
                    possible_coord = find_loop_dest(current_coord, ORIENTATIONS[current_facing], map, max_x, max_y)
                    print(f"possible coord = {possible_coord}")
                    if possible_coord == -1:
                        break
                    else:
                        current_coord = possible_coord
                if next_coord in map:
                    if map[next_coord] == "#":
                        break
                    else:
                        current_coord = next_coord
                else:  # loop around
                    possible_coord = find_loop_dest(current_coord, ORIENTATIONS[current_facing], map, max_x, max_y)
                    if possible_coord == -1:
                        break
                    current_coord = possible_coord
            print(f"Resulting coord = {current_coord}")
        elif instruction.isalpha():
            current_facing = (current_facing + DIRECTION_MAP[instruction]) % 4
            print(f"Turning {instruction}. NEW FACING = {current_facing}")
    print(current_coord)
    # do stuff here
    return (current_coord[0] + 1) * 4 + (current_coord[1] + 1) * 1000 + current_facing


def part_two(input_filename, face_size):
    with open(input_filename) as file:
        input_text = file.read()
    map, instructions = parse_map_and_instructions(input_text)
    max_x, max_y = max([item[0] for item in map.keys()]), max([item[1] for item in map.keys()])
    print(max_x, max_y)
    current_facing = 0
    current_coord = None
    for n in range(100000):
        if (n, 0) in map:
            current_coord = (n, 0)
            break
    print(current_coord)
    print(ORIENTATIONS[current_facing])
    for instruction in instructions:
        if instruction.isnumeric():
            print(f"Going forward {instruction} paces")
            for n in range(int(instruction)):
                print(current_coord)
                next_coord = tuple(numpy.add(current_coord, ORIENTATIONS[current_facing]))
                if not 0 <= next_coord[0] <= max_x or not 0 <= next_coord[1] <= max_y:
                    possible_coord = find_loop_dest(current_coord, ORIENTATIONS[current_facing], map, max_x, max_y)
                    print(f"possible coord = {possible_coord}")
                    if possible_coord == -1:
                        break
                    else:
                        current_coord = possible_coord
                if next_coord in map:
                    if map[next_coord] == "#":
                        break
                    else:
                        current_coord = next_coord
                else:  # loop around
                    possible_coord = find_loop_dest(current_coord, ORIENTATIONS[current_facing], map, max_x, max_y)
                    if possible_coord == -1:
                        break
                    current_coord = possible_coord
            print(f"Resulting coord = {current_coord}")
        elif instruction.isalpha():
            current_facing = (current_facing + DIRECTION_MAP[instruction]) % 4
            print(f"Turning {instruction}. NEW FACING = {current_facing}")
    print(current_coord)
    # do stuff here
    return (current_coord[0] + 1) * 4 + (current_coord[1] + 1) * 1000 + current_facing


if __name__ == "__main__":
    print("*** PART ONE ***\n")
    # print(f"Test result = {part_one('inputtest.txt')}\n")
    # print(f"REAL RESULT = {part_one('input.txt')}\n\n")
    # print("*** PART TWO ***\n")
    print(f"Test result = {part_two('inputtest.txt', face_size=4)}\n")
    # print(f"REAL RESULT = {part_two('input.txt', face_size=40)}")
