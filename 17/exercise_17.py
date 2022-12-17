from helpers import helpers
from itertools import cycle
import numpy
from copy import deepcopy

SHAPE_CYCLE = cycle([[(0, 0), (1, 0), (2, 0), (3, 0)],
                     [(1, 0), (0, 1), (1, 1), (2, 1), (1, 2),],
                     [(0, 0), (1, 0), (2, 0), (2, 1), (2, 2),],
                     [(0, 0), (0, 1), (0, 2), (0, 3)],
                     [(0, 0), (1, 0), (0, 1), (1, 1)]])

GAS_DIR_MAP = {">": (1, 0), "<": (-1, 0)}


def visualize(tetris_board, max_y):
    for y in range(max_y + 1):
        for x in range(7):
            if (x, max_y - y) in tetris_board:
                print("#", end="")
            else:
                print(".", end="")
        print("")


def take_snapshot_of_top_rows(tetris_board, max_y):  # took a lot of tuning to figure out how far down to look
    snapshot = []
    for y in range(50):
        for x in range(7):
            if (x, max_y - y) in tetris_board:
                snapshot.append(tuple([x, y]))
    return tuple(snapshot)


def part_one(input_filename):
    shape_cycle = deepcopy(SHAPE_CYCLE)
    height_map = {}
    input = helpers.parse_input(input_filename)
    gas_pattern = cycle([char for char in input][0])
    highest_y_point = 0
    tetris_board = set()
    for _ in range(2022):
        next_rock = next(shape_cycle)
        origin = (2, highest_y_point + 3)
        still_falling = True
        while still_falling:
            gas_symbol = next(gas_pattern)
            gas_dir = GAS_DIR_MAP[gas_symbol] # gas blows
            for coord in next_rock:
                can_move = True
                try:
                    delta_coord = tuple(numpy.add(coord, origin))
                    if (tuple(numpy.add(delta_coord, gas_dir)) in tetris_board) or (numpy.add(delta_coord, gas_dir)[0] < 0) or (tuple(numpy.add(delta_coord, gas_dir))[1] < 0):
                        can_move = False
                        break
                    elif (numpy.add(delta_coord, gas_dir)[0] > 6):
                        can_move = False
                        break
                except IndexError:
                    can_move = False
            if can_move:
                origin = tuple(numpy.add(origin, gas_dir))
            for coord in next_rock:
                delta_coord = numpy.add(coord, origin)
                if tuple(numpy.add(delta_coord, (0, -1))) in tetris_board or tuple(numpy.add(delta_coord, (0, -1)))[0] < 0 or tuple(numpy.add(delta_coord, (0, -1)))[1] < 0:
                    still_falling = False
                    break
            if not still_falling:
                for coord in next_rock:
                    tetris_board.add(tuple(numpy.add(coord, origin)))
                    highest_y_point = max((max([coord[1] for coord in tetris_board]) + 1), highest_y_point)
                    height_map[_] = highest_y_point
            else:
                origin = numpy.add(origin, (0, -1))
    return highest_y_point


def part_two(input_filename):
    shape_cycle = deepcopy(SHAPE_CYCLE)
    height_map = {}
    target_round = 1000000000000
    input = helpers.parse_input(input_filename)
    gas_pattern = cycle([char for char in input][0])
    highest_y_point = 0
    tetris_board = set()
    snapshots = {}
    print(len(input[0]))
    for round in range(1000000):
        next_rock = next(shape_cycle)
        origin = (2, highest_y_point + 3)
        still_falling = True
        while still_falling:
            gas_symbol = next(gas_pattern)
            gas_dir = GAS_DIR_MAP[gas_symbol] # gas blows
            for coord in next_rock:
                can_move = True
                try:
                    delta_coord = tuple(numpy.add(coord, origin))
                    if (tuple(numpy.add(delta_coord, gas_dir)) in tetris_board) or (numpy.add(delta_coord, gas_dir)[0] < 0) or (tuple(numpy.add(delta_coord, gas_dir))[1] < 0):
                        can_move = False
                        break
                    elif (numpy.add(delta_coord, gas_dir)[0] > 6):
                        can_move = False
                        break
                except IndexError:
                    can_move = False
            if can_move:
                origin = tuple(numpy.add(origin, gas_dir))
            for coord in next_rock:
                delta_coord = numpy.add(coord, origin)
                if tuple(numpy.add(delta_coord, (0, -1))) in tetris_board or tuple(numpy.add(delta_coord, (0, -1)))[0] < 0 or tuple(numpy.add(delta_coord, (0, -1)))[1] < 0:
                    still_falling = False
                    break
            if not still_falling:
                for coord in next_rock:
                    tetris_board.add(tuple(numpy.add(coord, origin)))
                highest_y_point = max((max([coord[1] for coord in tetris_board]) + 1), highest_y_point)
                snapshot = take_snapshot_of_top_rows(tetris_board, highest_y_point)
                height_map[round] = highest_y_point
                if snapshot in snapshots:
                    snapshots[snapshot].append(round)
                    round_entering_cycle = snapshots[snapshot][0]
                    round_exiting_cycle = round
                    height_entering_cycle = height_map[snapshots[snapshot][0]]
                    height_per_cycle = height_map[round] - height_entering_cycle
                    cycle_length = round_exiting_cycle - round_entering_cycle
                    number_of_reps, leftover = divmod(target_round - round_entering_cycle, cycle_length)
                    return height_entering_cycle + (number_of_reps * height_per_cycle) + height_map[round_entering_cycle + leftover] - (height_map[round_entering_cycle]) - 1
                else:
                    snapshots[snapshot] = [round]

            else:
                origin = numpy.add(origin, (0, -1))

    print(snapshots)
    for key, value in snapshots.items():
        if len(value) > 1:
            print(value, "\n")
    return highest_y_point


if __name__ == "__main__":
    print("*** PART ONE ***\n")
    print(f"Test result = {part_one('inputtest.txt')}\n")
    print(f"REAL RESULT = {part_one('input.txt')}\n\n")
    print("*** PART TWO ***\n")
    print(f"Test result = {part_two('inputtest.txt')}\n")
    print(f"REAL RESULT = {part_two('input.txt')}")
