import copy
import os
import time
from collections import deque
from copy import deepcopy
import curses

import numpy
from rich import print as rprint
from rich.console import Console

from helpers import helpers

letters = "abcdefghijklmnopqrstuvwxyz"
letter_height_map = {val: idx for idx, val in enumerate(letters)}
letter_height_map["S"] = 0
letter_height_map["E"] = 25

def clear():
    os.system('clear')

# def print_map(the_map, visited, current_coord):
    # clear()
    # console = Console(soft_wrap=True)
    # new_map = copy.deepcopy(the_map)
    # new_map = [list(item) for item in new_map]
    # new_map[current_coord[1]][current_coord[0]] = "[red]" + the_map[current_coord[1]][current_coord[0]] + "[/red]"
    # for coord in visited:
    #     new_map[coord[1]][coord[0]] = "[blue]" + new_map[coord[1]][coord[0]] + "[/blue]"
    # new_map = ["".join(item) for item in new_map]
    # console.print("\n".join(new_map))


    # for y, line in enumerate(the_map):
    #     for x, char in enumerate(line):
    #         style = None
    #         if tuple([x, y]) == tuple(current_coord):
    #             style = "red"
    #         elif tuple([x, y]) in visited:
    #             style = "green"
    #         console.print(char, style=style, end="")
    #     print("")




def part_one(input_filename, use_curses=True):
    the_map = helpers.parse_input(input_filename)
    starting_coord, ending_coord = None, None
    visited = set()
    if use_curses:
        scr = helpers.init_curses()
    max_y = len(the_map)
    for y, line in enumerate(the_map):
        for x, char in enumerate(line):
            if char == "S":
                starting_coord = (x, y)
            elif char == "E":
                ending_coord = (x, y)
            if use_curses:
                scr.addch(y, x, char, curses.color_pair(1))
    if use_curses:
        scr.refresh()
    next_steps_queue = deque([(starting_coord[0], starting_coord[1], 0)])
    while next_steps_queue:
        this_step = next_steps_queue.popleft()
        if use_curses:
            scr.addstr(max_y + 1, 0, f"STEP COUNT = {this_step[2]}")
            scr.refresh()
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
                    if use_curses:
                        scr.addch(possible_next_coord[1], possible_next_coord[0], the_map[possible_next_coord[1]][possible_next_coord[0]], curses.color_pair(4))
                        scr.refresh()
                        time.sleep(10)
                    return this_step[2] + 1
                next_steps_queue.append(tuple([possible_next_coord[0], possible_next_coord[1], this_step[2] + 1]))
                if use_curses:
                    scr.addch(possible_next_coord[1], possible_next_coord[0], the_map[possible_next_coord[1]][possible_next_coord[0]], curses.color_pair(3))
                    scr.refresh()
                    time.sleep(0.025)
                next_steps_queue.append(tuple([possible_next_coord[0], possible_next_coord[1], this_step[2] + 1]))
                if use_curses:
                    scr.addch(possible_next_coord[1], possible_next_coord[0], the_map[possible_next_coord[1]][possible_next_coord[0]], curses.color_pair(2))
                    scr.addch(this_step[1], this_step[0], the_map[this_step[1]][this_step[0]], curses.color_pair(2))
                    scr.refresh()
                visited.add(possible_next_coord)


def part_two(input_filename, use_curses=True):
    the_map = helpers.parse_input(input_filename)
    ending_coord = None
    possible_starts = []
    best_score = numpy.inf
    if use_curses:
        scr = curses.initscr()
        curses.curs_set(False)
        curses.start_color()
        curses.init_pair(1, curses.COLOR_WHITE, curses.COLOR_BLACK)
        curses.init_pair(2, curses.COLOR_CYAN, curses.COLOR_BLACK)
        curses.init_pair(3, curses.COLOR_RED, curses.COLOR_BLACK)
        scr.scrollok(False)
    for y, line in enumerate(the_map):
        for x, char in enumerate(line):
            if char == "E":
                ending_coord = (x, y)
            elif char == "a":
                possible_starts.append(tuple([x, y]))
            scr.addch(y, x, char, curses.color_pair(1))
    scr.refresh()
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
                    # print_map(the_map, visited, possible_next_coord)
                    scr.addch(possible_next_coord[1], possible_next_coord[0], the_map[possible_next_coord[1]][possible_next_coord[0]], curses.color_pair(3))
                    scr.refresh()
                    time.sleep(0.03)
                    next_steps_queue.append(tuple([possible_next_coord[0], possible_next_coord[1], this_step[2] + 1]))
                    scr.addch(possible_next_coord[1], possible_next_coord[0], the_map[possible_next_coord[1]][possible_next_coord[0]], curses.color_pair(2))
                    scr.addch(this_step[1], this_step[0], the_map[this_step[1]][this_step[0]], curses.color_pair(2))
                    scr.refresh()
                    visited.add(possible_next_coord)
        break
    return best_score


if __name__ == "__main__":
    # print("*** PART ONE ***\n")
    # print(f"Test result = {part_one('inputtest.txt')}\n")
    # print(f"REAL RESULT = {part_one('input.txt')}\n\n")
    part_one('input.txt')
    # print("*** PART TWO ***\n")
    # print(f"Test result = {part_two('inputtest.txt')}\n")
    # print(f"REAL RESULT = {part_two('input.txt')}")
    # part_two('input.txt')

