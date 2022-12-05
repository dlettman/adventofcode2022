from helpers import helpers

SYMBOL_SCORE_MAP = {"X": 1, "Y": 2, "Z": 3}
SCORE_NESTED_MAP = {"A": {"X": 3, "Y": 6, "Z": 0}, "B": {"X": 0, "Y": 3, "Z": 6}, "C": {"X": 6, "Y": 0, "Z": 3}}

INDEX_MAP_THEM = {"A": 0, "B": 1, "C": 2}
VICTORY_SCORE_MAP = {"X": 0, "Y": 3, "Z": 6}
HOW_MANY_TO_GO_BACK = {"X": 1, "Y": 3, "Z": 2}  # back 1 = lose, back 2 = win, back 3 = draw
SYMBOL_CYCLE = "XYZ"


def part_one(input_filename):
    input = helpers.parse_input(input_filename)
    output = 0
    for line in input:
        them, me = line.split(" ")
        output += (SYMBOL_SCORE_MAP[me] + SCORE_NESTED_MAP[them][me])
    return output


def part_two(input_filename):
    input = helpers.parse_input(input_filename)
    output = 0
    for line in input:
        them, me = line.split(" ")
        start_index = INDEX_MAP_THEM[them]
        my_symbol = SYMBOL_CYCLE[(start_index - HOW_MANY_TO_GO_BACK[me]) % 3]
        output += (VICTORY_SCORE_MAP[me] + SYMBOL_SCORE_MAP[my_symbol])
    return output


if __name__ == "__main__":
    print("*** PART ONE ***\n")
    print(f"Test result = {part_one('inputtest.txt')}\n")
    print(f"REAL RESULT = {part_one('input.txt')}\n\n")
    print("*** PART TWO ***\n")
    print(f"Test result = {part_two('inputtest.txt')}\n")
    print(f"REAL RESULT = {part_two('input.txt')}")
