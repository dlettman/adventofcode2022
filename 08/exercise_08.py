from math import prod

from helpers import helpers


def is_visible(x, y, forest, tree):
    for dir in helpers.NEIGHBORS_ORTH:
        distance = 1
        while True:
            try:
                (x_coord, y_coord) = (x + (dir[0] * distance), y + (dir[1] * distance))
                if x_coord < 0 or y_coord < 0:  # off the edge of the map, visible
                    return True
                if forest[y_coord][x_coord] >= tree:  # same size tree or taller, not visible
                    break
                else:
                    distance += 1
            except IndexError:  # off the edge of the map, visible
                return True
    return False


def get_scenic_score(x, y, forest, tree):
    scores = [0, 0, 0, 0]
    for idx, dir in enumerate(helpers.NEIGHBORS_ORTH):
        distance = 1
        while True:
            try:
                (x_coord, y_coord) = (x + (dir[0] * distance), y + (dir[1] * distance))
                if x_coord < 0 or y_coord < 0:   # off the edge of the map, no additional tree
                    scores[idx] = distance - 1
                    break
                if forest[y_coord][x_coord] >= tree:  # same size or larger tree, but we can see it
                    scores[idx] = distance
                    break
                else:  # keep going
                    distance += 1
            except IndexError:  # off the edge of the map, no additional tree
                scores[idx] = distance - 1
                break
    return prod(scores)


def part_one(input_filename):
    input_text = helpers.parse_input(input_filename)
    total = 0
    for y, line in enumerate(input_text):
        for x, tree in enumerate(line):
            if is_visible(x, y, input_text, tree):
                total += 1
    return total


def part_two(input_filename):
    input_text = helpers.parse_input(input_filename)
    top_score = 0
    for y, line in enumerate(input_text):
        for x, tree in enumerate(line):
            top_score = max(get_scenic_score(x, y, input_text, tree), top_score)
    return top_score


if __name__ == "__main__":
    print("*** PART ONE ***\n")
    print(f"Test result = {part_one('inputtest.txt')}\n")
    print(f"REAL RESULT = {part_one('input.txt')}\n\n")
    print("*** PART TWO ***\n")
    print(f"Test result = {part_two('inputtest.txt')}\n")
    print(f"REAL RESULT = {part_two('input.txt')}")
