from helpers import helpers


IMPORTANT_CYCLES = [20, 60, 100, 140, 180, 220]


def part_one(input_filename):
    input_text = helpers.parse_input(input_filename)
    cycle, register_x, score = 1, 1, 0
    for line in input_text:
        if cycle in IMPORTANT_CYCLES:
            score += register_x * cycle
        cycle += 1
        if line == "noop":
            continue
        _, mag = line.split(" ")
        if cycle in IMPORTANT_CYCLES:
            score += register_x * cycle
        cycle += 1
        register_x += int(mag)
    return score


def write_pixel(drawing, cycle, pos):
    symbol = "#" if (cycle % 40) - 1 <= pos <= (cycle % 40) + 1 else "."
    for row in drawing:
        if len(row) >= 40:
            continue
        else:
            row.append(symbol)
            break


def part_two(input_filename):
    input_text = helpers.parse_input(input_filename)
    cycle, register_x = 0, 1
    drawing = [[] for _ in range(6)]
    for line in input_text:
        write_pixel(drawing, cycle, register_x)
        cycle += 1
        if line == "noop":
            continue
        write_pixel(drawing, cycle, register_x)
        cycle += 1
        _, mag = line.split(" ")
        register_x += int(mag)
    for row in drawing:
        print(row)


if __name__ == "__main__":
    print("*** PART ONE ***\n")
    print(f"Test result = {part_one('inputtest.txt')}\n")
    print(f"REAL RESULT = {part_one('input.txt')}\n\n")
    print("*** PART TWO ***\n")
    print(f"Test result = {part_two('inputtest.txt')}\n")
    print(f"REAL RESULT = {part_two('input.txt')}")
