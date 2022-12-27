from helpers import helpers

import numpy

BLIZZARD_DESTINATIONS = {">": (1, 0),
                         "<": (-1, 0),
                         "^": (0, -1),
                         "v": (0, 1)}

NEIGHBORS = [(1, 0), (0, 1), (-1, 0), (0, -1)]


def make_map(input_text):
    walls = set()
    blizzards = {}
    max_x = len(input_text[0]) - 1
    max_y = len(input_text) - 1
    for y, line in enumerate(input_text):
        for x, char in enumerate(line):
            if char == "#":
                walls.add((x, y))
            elif char in [">", "<", "^", "v"]:
                blizzards[(x, y)] = [char]
    return walls, blizzards, max_x, max_y


def move_blizzards(walls, blizzards, max_x, max_y):
    new_blizzards = {}
    for blizzard_coords in blizzards:
        for blizzard in blizzards[blizzard_coords]:
            new_blizzard_coord = tuple(numpy.add(blizzard_coords, BLIZZARD_DESTINATIONS[blizzard]))
            if new_blizzard_coord in walls:
                if blizzard == ">":
                    new_blizzard_coord = (1, blizzard_coords[1])
                elif blizzard == "<":
                    new_blizzard_coord = (max_x - 1, blizzard_coords[1])
                elif blizzard == "v":
                    new_blizzard_coord = (blizzard_coords[0], 1)
                elif blizzard == "^":
                    new_blizzard_coord = (blizzard_coords[0], max_y - 1)
            if new_blizzard_coord in new_blizzards:
                new_blizzards[new_blizzard_coord].append(blizzard)
            else:
                new_blizzards[new_blizzard_coord] = [blizzard]
    return new_blizzards


def visualize_map(walls, blizzards, max_x, max_y, coords=None):
    for y in range(max_y+ 1):
        for x in range(max_x + 1):
            if coords:
                if (x, y) in coords:
                    print("@", end="")
                    continue
            if (x, y) in walls:
                print("#", end="")
            elif (x, y) in blizzards:
                print(blizzards[(x, y)][0], end="")
            else:
                print(".", end="")
        print("")
    print("")


def part_one(input_filename, start=None, end=None, start_minute=0, blizzard_snapshots=None, debug=False):
    input_text = helpers.parse_input(input_filename)
    walls, blizzards, max_x, max_y = make_map(input_text)
    current_position = start if start else (max_x - 1, max_y)
    goal_coord = end if end else (max_x - 1, max_y)
    blizzard_snapshots = blizzard_snapshots if blizzard_snapshots else {0: blizzards}
    frontier = {(current_position[0], current_position[1], start_minute)}  # tuple of (x, y, round)
    for n in range(20000000000):
        if debug:
            print(n)
        new_frontier = set()
        possible_coords = set()
        for possibility in frontier:
            x, y, minute = possibility
            if minute + 1 not in blizzard_snapshots:
                blizzard_snapshots[minute + 1] = move_blizzards(walls, blizzards, max_x, max_y)
                blizzards = blizzard_snapshots[minute + 1]
            for neighbor in NEIGHBORS:
                neighbor_coords = tuple(numpy.add(neighbor, (x, y)))
                if neighbor_coords == goal_coord:
                    return minute + 1
                elif (neighbor_coords not in walls) and (neighbor_coords not in blizzard_snapshots[minute + 1]) and (neighbor_coords[0] >= 0) and (neighbor_coords[1] >= 0):
                    new_frontier.add((neighbor_coords[0], neighbor_coords[1], minute + 1))
                    possible_coords.add((neighbor_coords[0], neighbor_coords[1]))
            if (x, y) not in blizzard_snapshots[minute + 1]:
                new_frontier.add((x, y, minute + 1))
                possible_coords.add((x, y))
        if debug:
            visualize_map(walls, blizzard_snapshots[minute + 1], max_x, max_y, possible_coords)
        frontier = new_frontier


def part_two(input_filename):
    input_text = helpers.parse_input(input_filename)
    walls, blizzards, max_x, max_y = make_map(input_text)
    blizzard_snapshots = {0: blizzards}
    for n in range(2000):
        blizzard_snapshots[n] = move_blizzards(walls, blizzards, max_x, max_y)
        blizzards = move_blizzards(walls, blizzards, max_x, max_y)
    step_1_end = part_one(input_filename, start=(1,0), end=None, start_minute=0, blizzard_snapshots=blizzard_snapshots)
    print(f"Step one end = {step_1_end}")
    step_2_end = part_one(input_filename, start=None, end=(1,0), start_minute=step_1_end, blizzard_snapshots=blizzard_snapshots)
    print(f"Step two end = {step_2_end}")
    step_3_end = part_one(input_filename, start=(1,0), end=None, blizzard_snapshots=blizzard_snapshots, start_minute=step_2_end)
    return step_3_end + 1


if __name__ == "__main__":
    print("*** PART ONE ***\n")
    print(f"Test result = {part_one('inputtest.txt')}\n")
    print(f"REAL RESULT = {part_one('input.txt')}\n\n")
    print("*** PART TWO ***\n")
    print(f"Test result = {part_two('inputtest.txt')}\n")
    print(f"REAL RESULT = {part_two('input.txt')}")
