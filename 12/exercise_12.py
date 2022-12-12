from collections import deque

import numpy

from helpers import helpers

letters = "abcdefghijklmnopqrstuvwxyz"
letter_height_map = {val: idx for idx, val in enumerate(letters)}
letter_height_map["S"] = 0
letter_height_map["E"] = 25

def part_one(input_filename):
    the_map = helpers.parse_input(input_filename)
    starting_coord, ending_coord = None, None
    visited = set()
    for y, line in enumerate(the_map):
        for x, char in enumerate(line):
            if char == "S":
                starting_coord = (x, y)
            elif char == "E":
                ending_coord = (x, y)
        if starting_coord and ending_coord:
            break
    next_steps_queue = deque([(starting_coord[0], starting_coord[1], 0)])
    while next_steps_queue:
        this_step = next_steps_queue.popleft()
        for neighbor in helpers.NEIGHBORS_ORTH:
            possible_next_coord = tuple(numpy.add(this_step[0:2], neighbor))
            if possible_next_coord in visited:
                continue
            elif possible_next_coord[0] < 0 or possible_next_coord[1] < 0 or possible_next_coord[0] > len(the_map[0]) - 1 or possible_next_coord[1] > len(the_map) - 1:
                continue
            elif letter_height_map[the_map[possible_next_coord[1]][possible_next_coord[0]]] > 1 + letter_height_map[the_map[this_step[1]][this_step[0]]]:
                continue
            else:
                if tuple(possible_next_coord) == tuple(ending_coord):
                    return this_step[2] + 1
                next_steps_queue.append(tuple([possible_next_coord[0], possible_next_coord[1], this_step[2] + 1]))
                visited.add(possible_next_coord)


def part_two(input_filename):
    the_map = helpers.parse_input(input_filename)
    ending_coord = None
    possible_starts = []
    best_score = numpy.inf
    for y, line in enumerate(the_map):
        for x, char in enumerate(line):
            if char == "E":
                ending_coord = (x, y)
            elif char == "a":
                possible_starts.append(tuple([x, y]))
    for start in possible_starts:
        visited = set()
        next_steps_queue = deque([(start[0], start[1], 0)])
        while next_steps_queue:
            this_step = next_steps_queue.popleft()
            for neighbor in helpers.NEIGHBORS_ORTH:
                possible_next_coord = tuple(numpy.add(this_step[0:2], neighbor))
                if possible_next_coord in visited:
                    continue
                elif possible_next_coord[0] < 0 or possible_next_coord[1] < 0 or possible_next_coord[0] > len(the_map[0]) - 1 or possible_next_coord[1] > len(the_map) - 1:
                    continue
                elif letter_height_map[the_map[possible_next_coord[1]][possible_next_coord[0]]] > 1 + letter_height_map[the_map[this_step[1]][this_step[0]]]:
                    continue
                else:
                    if tuple(possible_next_coord) == tuple(ending_coord):
                        best_score = min(this_step[2] + 1, best_score)
                        next_steps_queue = None
                        break
                    next_steps_queue.append(tuple([possible_next_coord[0], possible_next_coord[1], this_step[2] + 1]))
                    visited.add(possible_next_coord)
    return best_score


if __name__ == "__main__":
    print("*** PART ONE ***\n")
    print(f"Test result = {part_one('inputtest.txt')}\n")
    print(f"REAL RESULT = {part_one('input.txt')}\n\n")
    print("*** PART TWO ***\n")
    print(f"Test result = {part_two('inputtest.txt')}\n")
    print(f"REAL RESULT = {part_two('input.txt')}")
