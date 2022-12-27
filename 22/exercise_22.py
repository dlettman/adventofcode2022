import re
import numpy


DIRECTION_MAP = {"L": -1, "R": 1}
ORIENTATIONS = [(1, 0), (0, 1), (-1, 0), (0, -1)]

NEW_HEADING_MAP = {"<": 2,
                   ">": 0,
                   "^": 3,
                   "v": 1}

HEADING_ORIENTATION_MAP = {v: k for k, v in NEW_HEADING_MAP.items()}


def parse_map_and_instructions(input_text):
    split_input = input_text.split("\n")
    map = {}
    for y, line in enumerate(split_input):
        if line == "":
            break
        for x, char in enumerate(line):
            if char in [".", "#"]:
                map[(x, y)] = char
    instructions = input_text.split("\n\n")[1]
    regex_pattern = '(\d+)'
    split_instructions = re.split(regex_pattern, instructions)[1:-1]
    return map, split_instructions


def turn(current_facing: int, direction: str):
    return current_facing + DIRECTION_MAP[direction] % 4


def wrap_the_cube(x, y, heading):
    if 150 <= y <= 199 and 0 <= x <= 49:
        # side A
        if heading == "<":  # go onto E
            new_heading = "v"
            new_row = 0
            new_col = y - 100
        elif heading == "v":  # onto F
            new_heading = "v"
            new_row = 0
            new_col = x + 100
        elif heading == ">":  # onto C
            new_heading = "^"
            new_row = 149
            new_col = y - 100
        else:
            raise RuntimeError("direction should not occur")
    elif 100 <= y <= 149 and 0 <= x <= 49:
        # side B
        if heading == "<":  # onto E
            new_heading = ">"
            new_col = 50
            new_row = 149 - y
        elif heading == "^":  # onto D
            new_heading = ">"
            new_col = 50
            new_row = x + 50
        else:
            raise RuntimeError("direction should not occur")
    elif 100 <= y <= 149 and 50 <= x <= 149:
        # side C
        if heading == "v":  # onto A
            new_heading = "<"
            new_col = 49
            new_row = x + 100
        elif heading == ">":  # onto F
            new_heading = "<"
            new_col = 149
            new_row = 149 - y
        else:
            raise RuntimeError("direction should not occur")
    elif 50 <= y <= 99 and 50 <= x <= 99:
        # side D
        if heading == "<":  # onto B
            new_heading = "v"
            new_row = 100
            new_col = y - 50
        elif heading == ">":  # onto F
            new_heading = "^"
            new_row = 49
            new_col = y + 50
        else:
            raise RuntimeError("direction should not occur")
    elif 0 <= y <= 49 and 50 <= x <= 99:
        # side E
        if heading == "<":  # onto B
            new_heading = ">"
            new_col = 0
            new_row = 149 - y
        elif heading == "^":  # onto A
            new_heading = ">"
            new_col = 0
            new_row = x + 100
        else:
            raise RuntimeError("direction should not occur")
    elif 0 <= y <= 49 and 100 <= x <= 149:
        # side F
        if heading == "^":  # onto A
             new_heading = "^"
             new_row = 199
             new_col = x - 100
        elif heading == ">":  # onto C
            new_heading = "<"
            new_col = 99
            new_row = 149 - y
        elif heading == "v":  # onto D
            new_heading = "<"
            new_col = 99
            new_row = x - 50
        else:
            raise RuntimeError("direction should not occur")
    else:
        raise RuntimeError("Something went wrong with grid wrapping...")
    return (new_col, new_row), new_heading


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
    current_facing = 0
    current_coord = None
    for n in range(100000):
        if (n, 0) in map:
            current_coord = (n, 0)
            break

    for instruction in instructions:
        if instruction.isnumeric():
            for n in range(int(instruction)):
                print(current_coord)
                next_coord = tuple(numpy.add(current_coord, ORIENTATIONS[current_facing]))
                if not 0 <= next_coord[0] <= max_x or not 0 <= next_coord[1] <= max_y:
                    possible_coord = find_loop_dest(current_coord, ORIENTATIONS[current_facing], map, max_x, max_y)
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
        elif instruction.isalpha():
            current_facing = (current_facing + DIRECTION_MAP[instruction]) % 4
    return (current_coord[0] + 1) * 4 + (current_coord[1] + 1) * 1000 + current_facing


def part_two(input_filename, face_size):
    with open(input_filename) as file:
        input_text = file.read()
    map, instructions = parse_map_and_instructions(input_text)
    max_x, max_y = max([item[0] for item in map.keys()]), max([item[1] for item in map.keys()])
    current_facing = 0
    current_coord = None
    for n in range(100000):
        if (n, 0) in map:
            current_coord = (n, 0)
            break
    for instruction in instructions:
        if instruction.isnumeric():
            for n in range(int(instruction)):
                next_coord = tuple(numpy.add(current_coord, ORIENTATIONS[current_facing]))
                if not 0 <= next_coord[0] <= max_x or not 0 <= next_coord[1] <= max_y:
                    (pos_x, pos_y), pos_heading = wrap_the_cube(current_coord[0], current_coord[1], HEADING_ORIENTATION_MAP[current_facing])
                    if map[(pos_x, pos_y)] == "#":
                        break
                    else:
                        current_coord = (pos_x, pos_y)
                        current_facing = NEW_HEADING_MAP[pos_heading]
                elif next_coord in map:
                    if map[next_coord] == "#":
                        break
                    else:
                        current_coord = next_coord
                else:
                    (pos_x, pos_y), pos_heading = wrap_the_cube(current_coord[0], current_coord[1], HEADING_ORIENTATION_MAP[current_facing])
                    if map[(pos_x, pos_y)] == "#":
                        break
                    else:
                        current_coord = (pos_x, pos_y)
                        current_facing = NEW_HEADING_MAP[pos_heading]
        elif instruction.isalpha():
            current_facing = (current_facing + DIRECTION_MAP[instruction]) % 4
    return (current_coord[0] + 1) * 4 + (current_coord[1] + 1) * 1000 + current_facing


if __name__ == "__main__":
    print("*** PART ONE ***\n")
    print(f"Test result = {part_one('inputtest.txt')}\n")
    print(f"REAL RESULT = {part_one('input.txt')}\n\n")
    print("*** PART TWO ***\n")
    # Nope, not gonna hardcode for the example as well - we'll test in prod!
    # print(f"Test result = {part_two('inputtest.txt')}\n")
    print(f"REAL RESULT = {part_two('input.txt')}")
