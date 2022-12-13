from helpers import helpers

import ast
import itertools
import math


class FunkyList(object):
    def __init__(self, data):
        self.data = data

    def __repr__(self):
        return str(self.data)

    def __eq__(self, other):
        return self.data == other.data

    def __lt__(self, other):
        return self.is_in_right_order(self.data, other.data) if self.is_in_right_order(self.data, other.data) in [True, False] else True

    def is_in_right_order(self, a, b):
        for a_elem, b_elem in itertools.zip_longest(a, b, fillvalue="I'M OUT!"):
            if isinstance(a_elem, int) and isinstance(b_elem, int):
                if a_elem == b_elem:
                    continue
                else:
                    return a_elem < b_elem
            elif isinstance(a_elem, list) and isinstance(b_elem, list):
                if not self.is_in_right_order(a_elem, b_elem) is None:
                    return self.is_in_right_order(a_elem, b_elem)
            elif isinstance(a_elem, list) and isinstance(b_elem, int):
                return self.is_in_right_order(a_elem, [b_elem])
            elif isinstance(a_elem, int) and isinstance(b_elem, list):
                return self.is_in_right_order([a_elem], b_elem)
            elif not isinstance(a_elem, str) and isinstance(b_elem, str):
                return False
            elif isinstance(a_elem, str) and not isinstance(b_elem, str):
                return True


def part_one(input_filename):
    correct_order_count, pair_number = 0, 0
    with open(input_filename) as file:
        input_list = file.read().split("\n\n")
    for idx, pair in enumerate(input_list):
        first, second = pair.split("\n")
        first, second = FunkyList(ast.literal_eval(first)), FunkyList(ast.literal_eval(second))
        if first < second:
            correct_order_count += idx + 1
    return correct_order_count


def part_two(input_filename):
    input_text = helpers.parse_input(input_filename)
    list_of_funky_lists = [FunkyList(ast.literal_eval(line)) for line in input_text if line]
    list_of_funky_lists += [FunkyList([[6]]), FunkyList([[2]])]
    list_of_funky_lists = sorted(list_of_funky_lists)
    return math.prod([idx + 1 for idx, funky_list in enumerate(list_of_funky_lists) if (funky_list.data == [[6]] or funky_list.data == [[2]])])


if __name__ == "__main__":
    print("*** PART ONE ***\n")
    print(f"Test result = {part_one('inputtest.txt')}\n")
    print(f"REAL RESULT = {part_one('input.txt')}\n\n")
    print("*** PART TWO ***\n")
    print(f"Test result = {part_two('inputtest.txt')}\n")
    print(f"REAL RESULT = {part_two('input.txt')}")
