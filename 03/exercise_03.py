import sys
sys.path.append("..")
import helpers


LETTERS = "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ"
LETTER_SCORE = {char: idx + 1 for idx, char in enumerate(LETTERS)}


def part_one(input_filename):
    input = helpers.parse_input(input_filename)
    score = 0
    for line in input:
        midpoint = len(line) // 2
        first, second = set(line[0:midpoint]), set(line[midpoint:])
        for letter in first.intersection(second):  # Only 1 element in the intersection
            score += LETTER_SCORE[letter]
    return score


def part_two(input_filename):
    input = helpers.parse_input(input_filename)
    ticker = 0
    working_set = None
    score = 0
    for line in input:
        working_set = set(line) if not working_set else working_set.intersection(set(line))
        ticker += 1
        if ticker == 3:
            letter = next(iter(working_set))  # Only 1 element in the set
            score += LETTER_SCORE[letter]
            working_set = None
            ticker = 0
    return score


if __name__ == "__main__":
    print("*** PART ONE ***\n")
    print(f"Test result = {part_one('inputtest.txt')}\n")
    print(f"REAL RESULT = {part_one('input.txt')}\n\n")
    print("*** PART TWO ***\n")
    print(f"Test result = {part_two('inputtest.txt')}\n")
    print(f"REAL RESULT = {part_two('input.txt')}")
