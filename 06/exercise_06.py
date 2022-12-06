from helpers import helpers
from collections import deque


def get_unique_char_marker(input_string, char_count):
    chars = deque()
    for idx, char in enumerate(input_string):
        chars.append(char)
        if len(set(chars)) == char_count:
            return idx
        if len(chars) >= char_count:
            chars.popleft()
    return None

def part_one(input_filename):
    input_text = helpers.parse_input(input_filename)
    return get_unique_char_marker(input_text[0], 4)


def part_two(input_filename):
    input_text = helpers.parse_input(input_filename)
    return get_unique_char_marker(input_text[0], 14)


if __name__ == "__main__":
    print("*** PART ONE ***\n")
    print(f"Test result = {part_one('inputtest.txt')}\n")
    print(f"REAL RESULT = {part_one('input.txt')}\n\n")
    print("*** PART TWO ***\n")
    print(f"Test result = {part_two('inputtest.txt')}\n")
    print(f"REAL RESULT = {part_two('input.txt')}")
