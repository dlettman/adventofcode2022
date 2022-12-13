from helpers import helpers

import ast
import itertools


class FunkyList(object):
    def __init__(self, data):
        self.data = data

    def __repr__(self):
        return str(self.data)

    def __eq__(self, other):
        return not self < other and not other < self

    def __lt__(self, other):
        try:
            return self.is_in_right_order(self.data, other.data)
        except Exception:
            return True

    def is_in_right_order(self, a, b):
        for a_elem, b_elem in itertools.zip_longest(a, b, fillvalue="I'M OUT!"):
            if type(a_elem) == int and type(b_elem) == int:
                if a_elem < b_elem:
                    raise Exception
                elif a_elem > b_elem:
                    return False
            elif type(a_elem) == list and type(b_elem) == list:
                if not self.is_in_right_order(a_elem, b_elem):
                    return False
            elif type(a_elem) == list and type(b_elem) == int:
                if not self.is_in_right_order(a_elem, [b_elem]):
                    return False
            elif type(a_elem) == int and type(b_elem) == list:
                if not self.is_in_right_order([a_elem], b_elem):
                    return False
            elif type(a_elem) != str and type(b_elem) == str:
                return False
            elif type(a_elem) == str and type(b_elem) != str:
                raise Exception
        return True


def part_one(input_filename):
    correct_order_count = 0
    pair_number = 0
    with open(input_filename) as file:
        input_list = file.read().split("\n\n")
    for pair in input_list:
        pair_number += 1
        first, second = pair.split("\n")
        first, second = FunkyList(ast.literal_eval(first)), FunkyList(ast.literal_eval(second))
        if first < second:
            correct_order_count += pair_number
    return correct_order_count


def part_two(input_filename):
    input_text = helpers.parse_input(input_filename)
    list_of_funky_lists = [FunkyList(ast.literal_eval(line)) for line in input_text if line]
    list_of_funky_lists.append(FunkyList([[6]]))
    list_of_funky_lists.append(FunkyList([[2]]))
    list_of_funky_lists = sorted(list_of_funky_lists)
    indices = []
    for idx, funky_list in enumerate(list_of_funky_lists):
        if funky_list.data == [[6]] or funky_list.data == [[2]]:
            indices.append(idx + 1)
    return indices[0] * indices[1]


if __name__ == "__main__":
    print("*** PART ONE ***\n")
    print(f"Test result = {part_one('inputtest.txt')}\n")
    print(f"REAL RESULT = {part_one('input.txt')}\n\n")
    print("*** PART TWO ***\n")
    print(f"Test result = {part_two('inputtest.txt')}\n")
    print(f"REAL RESULT = {part_two('input.txt')}")
