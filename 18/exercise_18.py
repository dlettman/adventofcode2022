from helpers import helpers
from collections import deque

import numpy

NEIGHBORS = [(1, 0, 0),
             (-1, 0, 0),
             (0, 1, 0),
             (0, -1, 0),
             (0, 0, 1),
             (0, 0, -1)]


def part_one(input_filename):
    input = helpers.parse_input(input_filename)
    count = 0
    coords = [tuple([int(item) for item in line.split(",")]) for line in input]
    for a_coord in coords:
        count += sum([1 for neighbor in NEIGHBORS if tuple(numpy.add(a_coord, neighbor)) not in coords])
    return count


def bfs_in_three_dee(coords, starting_coord):
    queue = deque(starting_coord)
    seen = set()
    sides_touched = 0
    while queue:
        current_coord = queue.popleft()
        if current_coord in seen:
            continue
        seen.add(current_coord)
        for neighbor in NEIGHBORS:
            neighbor_coord = tuple(numpy.add(current_coord, neighbor))
            if (not 0 <= neighbor_coord[0] <= 22) or (not 0 <= neighbor_coord[1] <= 22) or (not 0 <= neighbor_coord[2] <= 22):
                continue
            if neighbor_coord in coords:
                sides_touched += 1
                continue
            queue.append(neighbor_coord)
    return sides_touched


def part_two(input_filename):
    input = helpers.parse_input(input_filename)
    coords = set([tuple([int(item) for item in line.split(",")]) for line in input])
    for line in input:
        coord = tuple([int(item) for item in line.split(",")])
        coords.add(coord)
    return bfs_in_three_dee(coords, (0, 0, 0))  # manually verified that this is an appropriate starting spot


if __name__ == "__main__":
    print("*** PART ONE ***\n")
    print(f"Test result = {part_one('inputtest.txt')}\n")
    print(f"REAL RESULT = {part_one('input.txt')}\n\n")
    print("*** PART TWO ***\n")
    print(f"Test result = {part_two('inputtest.txt')}\n")
    print(f"REAL RESULT = {part_two('input.txt')}")
