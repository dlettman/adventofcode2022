from helpers import helpers
from copy import copy

class Dumber(object):

    def __init__(self, number):
        self.number = int(number)

    def __repr__(self):
        return str(self.number)

    def __add__(self, other):
        if isinstance(other, Dumber):
            return self.number + other.number
        else:
            return self.number + other

    def __radd__(self, other):
        if isinstance(other, Dumber):
            return self.number + other.number
        else:
            return self.number + other


def mix_it_up(input, times_to_mix = 1):
    length = len(input)
    initial_order = copy(input)
    working_order = copy(input)
    for _ in range(times_to_mix):
        for number in initial_order:
            previous_index = working_order.index(number)
            new_index = previous_index + number.number
            if new_index > length - 2:
                new_index %= length - 1
            if new_index < 1:
                new_index %= length - 1
            del working_order[previous_index]
            working_order.insert(new_index, number)
    return working_order


def part_one(input_filename):
    input = [Dumber(item) for item in helpers.parse_input(input_filename)]
    mixed_order = mix_it_up(input)
    for idx, dumber in enumerate(mixed_order):
        if dumber.number == 0:
            start_index = idx
    important_indices = [item + start_index for item in [1000, 2000, 3000]]
    mix_result = (mixed_order[important_indices[0] % (len(mixed_order))]) + (
    mixed_order[important_indices[1] % (len(mixed_order))]) + (mixed_order[important_indices[2] % (len(mixed_order))])
    return mix_result


def part_two(input_filename):
    input = [Dumber(int(item) * 811589153) for item in helpers.parse_input(input_filename)]
    mixed_order = mix_it_up(input, times_to_mix=10)
    for idx, dumber in enumerate(mixed_order):
        if dumber.number == 0:
            start_index = idx
    important_indices = [item + start_index for item in [1000, 2000, 3000]]
    mix_result = (mixed_order[important_indices[0] % (len(mixed_order))]) + (mixed_order[important_indices[1] % (len(mixed_order))]) + (mixed_order[important_indices[2] % (len(mixed_order))])
    return mix_result


if __name__ == "__main__":
    print("*** PART ONE ***\n")
    print(f"Test result = {part_one('inputtest.txt')}\n")
    print(f"REAL RESULT = {part_one('input.txt')}\n\n")
    print("*** PART TWO ***\n")
    print(f"Test result = {part_two('inputtest.txt')}\n")
    print(f"REAL RESULT = {part_two('input.txt')}")
