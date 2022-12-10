from helpers import helpers

import os
import time
import numpy



def clear():
    os.system('clear')


rel_map = {(2, 0): (1, 0),
           (2, 1): (1, 1),
           (2, 2): (1, 1),
           (1, 2): (1, 1),
           (0, 2): (0, 1),
           (-1, 2): (-1, 1),
           (-2, 2): (-1, 1),
           (-2, 1): (-1, 1),
           (-2, 0): (-1, 0),
           (-2, -1): (-1, -1),
           (-2, -2): (-1, -1),
           (-1, -2): (-1, -1),
           (0, -2): (0, -1),
           (1, -2): (1, -1),
           (2, -2): (1, -1),
           (2, -1): (1, -1)}


dir_map = {"R": (1, 0),
           "L": (-1, 0),
           "U": (0, 1),
           "D": (0, -1)}


def plot_ropes(ropes, trail):
    places = list(trail)
    max_x = max([item[0] for item in ropes] + [item[0] for item in places])
    max_y = max([item[1] for item in ropes] + [item[1] for item in places])
    min_x = min(0, min([item[0] for item in ropes] + [item[0] for item in places]))
    min_y = min(0, min([item[1] for item in ropes] + [item[1] for item in places]))
    rope_map = [["🟫" for _ in range((max_x - min_x)+ 1)] for _ in range((max_y - min_y) + 1)]
    for spot in trail:
        rope_map[((max_y) - spot[1])][(spot[0] - min_x)] = "🔷"
    for idx, rope in enumerate(ropes[::-1]):
        if idx == 9:
            rope_map[((max_y) - rope[1])][(rope[0] - min_x)] = "🟡"
        elif idx == 0:
            rope_map[((max_y) - rope[1])][(rope[0] - min_x)] = "🔴"
        else:
            rope_map[((max_y) - rope[1])][(rope[0] - min_x)] = "⚪"
            # rope_map[((max_y) - rope[1])][(rope[0] - min_x)] = str(idx).zfill(2)
    for line in rope_map:
        print("".join(line))


def part_one(input_filename, put_on_a_show=False):
    input = helpers.parse_input(input_filename)
    head_pos = (0, 0)
    tail_pos = (0, 0)
    positions = set([tail_pos])
    for command in input:
        direction, magnitude = command.split(" ")
        for num in range(int(magnitude)):
            head_pos = numpy.add(head_pos, dir_map[direction])
            tail_rel = tuple(numpy.subtract(head_pos, tail_pos))
            if tail_rel in rel_map:
                tail_pos = numpy.add(tail_pos, rel_map[tail_rel])
                positions.add(tuple(tail_pos))
            if put_on_a_show:
                plot_ropes([head_pos, tail_pos], positions)
                time.sleep(0.05)
                clear()
    return len(positions)


def part_two(input_filename, put_on_a_show=False):
    input = helpers.parse_input(input_filename)
    knot_pos = [(0, 0) for _ in range(10)]
    positions = set([(0, 0)])
    for command in input:
        direction, magnitude = command.split(" ")
        for num in range(int(magnitude)):
            knot_pos[0] = numpy.add(knot_pos[0], dir_map[direction])
            for idx, rope in enumerate(knot_pos[1:]):
                idx_mod = idx + 1
                rel_pos = tuple(numpy.subtract(knot_pos[idx], knot_pos[idx_mod]))
                if rel_pos in rel_map:
                    knot_pos[idx_mod] = numpy.add(knot_pos[idx_mod], rel_map[rel_pos])
                if idx_mod == 9:
                    positions.add(tuple(knot_pos[idx_mod]))
            if put_on_a_show:
                plot_ropes(knot_pos, positions)
                time.sleep(0.05)
                clear()
    return len(positions)



if __name__ == "__main__":
    print("*** PART ONE ***\n")
    # print(f"Test result = {part_one('inputtest.txt')}\n")
    # print(f"REAL RESULT = {part_one('input.txt')}\n\n")
    print(f"REAL RESULT = {part_one('waginput.txt', put_on_a_show=True)}\n\n")
    print("*** PART TWO ***\n")
    # print(f"Test result = {part_two('inputtest.txt')}\n")
    # print(f"REAL RESULT = {part_two('input.txt', put_on_a_show=True)}")
    # print(f"REAL RESULT = {part_two('waginput.txt', put_on_a_show=True)}")
