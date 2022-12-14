from helpers import helpers

import numpy


BUFFER = 500


class FallenIntoTheAbyss(Exception):
    pass


def when_god_gives_you_paths_make_rocks(paths):
    paths = [[tuple([int(subsubitem) for subsubitem in subitem.split(",")]) for subitem in item.split(' -> ')] for item in paths]
    min_x, min_y, max_x, max_y = numpy.inf, 0, 0, 0
    for path in paths:
        for coord in path:
            min_x, max_x = min(coord[0], min_x), max(coord[0], max_x)
            min_y, max_y = min(coord[1], min_y), max(coord[1], max_y)
    map = make_map(paths, min_x, max_x, min_y, max_y)
    rocks = []
    for path in paths:
        for idx in range(len(path) - 1):
            start, end = path[idx], path[idx + 1]
            if start[0] == end[0]:  # x coord stays the same, vertical path
                for y in range(min(start[1], end[1]), max(start[1], end[1]) + 1):
                  rocks.append(tuple([start[0] - min_x, y - min_y]))
            else:  # horizontal path
                for x in range(min(start[0], end[0]), max(start[0], end[0]) + 1):
                    rocks.append(tuple([x - min_x, start[1] - min_y]))
    for x, y in rocks:
        map[y][x + BUFFER] = "#"
    return map, min_x, max_x, min_y, max_y


def make_map(input_text, min_x, max_x, min_y, max_y):
    map = [["." for _ in range(min_x - 500, max_x + 502)] for _ in range(min_y, max_y + 2)]
    return map


def print_map(map):
    for line in map:
        print("".join(line))


def update_map(map, min_x, part=1):
    #  Returns the map and a boolean indicating whether the sand-spout is blocked
    sand_loc = (500 + BUFFER - min_x, 0)
    if map[sand_loc[1]][sand_loc[0]] == "o" and part == 2:
        return map, True
    updated = True
    while updated:
        updated = False
        try:
            for x_delta in [0, -1, 1]:
                if map[sand_loc[1] + 1][sand_loc[0] + x_delta] == ".":
                    sand_loc = (sand_loc[0] + x_delta, sand_loc[1] + 1)
                    updated = True
                    break
        except IndexError:
            if part == 1:
                raise FallenIntoTheAbyss
            else:
                break
    map[sand_loc[1]][sand_loc[0]] = "o"
    return map, False

def part_one(input_filename):
    paths = helpers.parse_input(input_filename)
    map, min_x, min_y, max_y, max_y = when_god_gives_you_paths_make_rocks(paths)
    grain_count = -1
    while True:
        try:
            map = update_map(map, min_x)[0]
            grain_count += 1
        except FallenIntoTheAbyss:
            break
    return grain_count


def part_two(input_filename):
    paths = helpers.parse_input(input_filename)
    map, min_x, min_y, max_y, max_y = when_god_gives_you_paths_make_rocks(paths)
    grain_count = -1
    blocked = False
    while not blocked:
        map, blocked = update_map(map, min_x, part=2)
        grain_count += 1
    return grain_count


if __name__ == "__main__":
    print("*** PART ONE ***\n")
    print(f"Test result = {part_one('inputtest.txt')}\n")
    print(f"REAL RESULT = {part_one('input.txt')}\n\n")
    print("*** PART TWO ***\n")
    print(f"Test result = {part_two('inputtest.txt')}\n")
    print(f"REAL RESULT = {part_two('input.txt')}")
