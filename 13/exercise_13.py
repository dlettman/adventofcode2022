from helpers import helpers

import ast
import itertools
import json


class FunkyList(object):
    def __init__(self, data):

        self.data = data

    def __eq__(self, other):
        return not self < other and not other < self

    def __lt__(self, other):
        iterables = ((itertools.chain(g, [f"generator {i} was exhausted"]) for i, g in enumerate([self.data, other])))
        for a_elem, b_elem in zip(*iterables):
            print("a elem = ", a_elem, "b elem = ", b_elem)
            if type(a_elem) == int and type(b_elem) == int:
                if a_elem < b_elem:
                    raise Exception
                elif a_elem > b_elem:
                    return False
                else:
                    continue
            elif type(a_elem) == list and type(b_elem) == list:
                if not is_in_right_order(a_elem, b_elem):
                    return False
                else:
                    continue
            elif type(a_elem) == list and type(b_elem) == int:
                if not is_in_right_order(a_elem, [b_elem]):
                    return False
                else:
                    continue
            elif type(a_elem) == int and type(b_elem) == list:
                if not is_in_right_order([a_elem], b_elem):
                    return False
                else:
                    continue
            elif type(a_elem) != str and type(b_elem) == str:
                print("b exhausted")
                return False
            elif type(a_elem) == str and type(b_elem) != str:
                print("a exhausted")
                raise Exception("oh shit")
        return True


def is_in_right_order(a, b):
    iterables = ((itertools.chain(g, [f"generator {i} was exhausted"]) for i, g in enumerate([a, b])))
    for a_elem, b_elem in zip(*iterables):
        print("a elem = ", a_elem, "b elem = ", b_elem)
        if type(a_elem) == int and type(b_elem) == int:
            if a_elem < b_elem:
                raise Exception
            elif a_elem > b_elem:
                return False
            else:
                continue
        elif type(a_elem) == list and type(b_elem) == list:
            if not is_in_right_order(a_elem, b_elem):
                return False
            else:
                continue
        elif type(a_elem) == list and type(b_elem) == int:
            if not is_in_right_order(a_elem, [b_elem]):
                return False
            else: continue
        elif type(a_elem) == int and type(b_elem) == list:
            if not is_in_right_order([a_elem], b_elem):
                return False
            else:
                continue
        elif type(a_elem) != str and type(b_elem) == str:
            print("b exhausted")
            return False
        elif type(a_elem) == str and type(b_elem) != str:
            print("a exhausted")
            raise Exception("oh shit")
    return True



def part_one(input_filename):
    correct_order_count = 0
    pair_number = 0
    with open(input_filename) as file:
        input_list = file.read().split("\n\n")
    for pair in input_list:
        pair_number += 1
        first, second = pair.split("\n")
        first, second = ast.literal_eval(first), ast.literal_eval(second)
        # first, second = FunkyList(ast.literal_eval(first)), FunkyList(ast.literal_eval(second))
        try:
            if is_in_right_order(first, second):
                print(is_in_right_order(first, second))
                print("pair ", pair_number, " is correct")
                correct_order_count += pair_number
            else:
                print("pair ", pair_number, "is NOT correct")
        except Exception:
            print("pair ", pair_number, " is correct VIA EXCEPTION")
            correct_order_count += pair_number
    return correct_order_count


def part_two(input_filename):
    input = helpers.parse_input(input_filename)
    if not input:
        return "*** NO INPUT SUPPLIED ***"
    # do stuff here
    output = input
    return output


if __name__ == "__main__":
    print("*** PART ONE ***\n")
    print(f"Test result = {part_one('inputtest.txt')}\n")
    print(f"REAL RESULT = {part_one('input.txt')}\n\n")
    # print("*** PART TWO ***\n")
    # print(f"Test result = {part_two('inputtest.txt')}\n")
    # print(f"REAL RESULT = {part_two('input.txt')}")
