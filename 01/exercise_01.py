import helpers

def part_one(input_filename):
    input = helpers.parse_input(input_filename)
    elves = []
    current_tot = 0
    for n in input:
        if n == "":
            elves.append(current_tot)
            current_tot = 0
        else:
            current_tot += int(n)
    elves.append(current_tot)
    return max(elves)

def part_two(input_filename):
    input = helpers.parse_input(input_filename)
    elves = []
    current_tot = 0
    for n in input:
        if n == "":
            elves.append(current_tot)
            current_tot = 0
        else:
            current_tot += int(n)
    elves.append(current_tot)
    return sum(sorted(elves)[-3:])

if __name__ == "__main__":
    print("*** PART ONE ***\n")
    print(f"Test result = {part_one('inputtest.txt')}\n")
    print(f"REAL RESULT = {part_one('input.txt')}\n\n")
    print("*** PART TWO ***\n")
    print(f"Test result = {part_two('inputtest.txt')}\n")
    print(f"REAL RESULT = {part_two('input.txt')}")
