from helpers import helpers


def parse_crates(input_text):
    stacks = {n: [] for n in range(1, 10)}
    for line in input_text:
        if line == "":
            break
        offset_counter = 1
        offset = 1
        while True:
            try:
                if line[offset].isalpha():
                    stacks[offset_counter].append(line[offset])
                offset_counter += 1
                offset += 4
            except IndexError:
                break
    stacks = {k: v[::-1] for k, v in stacks.items()}
    return stacks


def get_quantity_source_dest(line):
    _, quantity, _, source, _, dest = [int(item) if item.isnumeric() else None for item in line.split(" ")]
    return quantity, source, dest


def part_one(input_filename):
    input = helpers.parse_input(input_filename)
    stacks = parse_crates(input)
    for line in input:
        if not line.startswith("move"):  # lazy, but good enough!
            continue
        quantity, source, dest = get_quantity_source_dest(line)
        for _ in range(int(quantity)):
            popped = stacks[source].pop()
            stacks[dest].append(popped)
    return "".join(stacks[key][-1] for key in range(1, 10) if stacks[key])


def part_two(input_filename):
    input = helpers.parse_input(input_filename)
    stacks = parse_crates(input)
    for line in input:
        if not line.startswith("move"):
            continue
        quantity, source, dest = get_quantity_source_dest(line)
        moved_crates = stacks[source][-1 * quantity:]
        stacks[source] = stacks[source][0:-1 * quantity]
        stacks[dest] = stacks[dest] + moved_crates
    return "".join(stacks[key][-1] for key in range(1, 10) if stacks[key])


if __name__ == "__main__":
    print("*** PART ONE ***\n")
    print(f"Test result = {part_one('inputtest.txt')}\n")
    print(f"REAL RESULT = {part_one('input.txt')}\n\n")
    print("*** PART TWO ***\n")
    print(f"Test result = {part_two('inputtest.txt')}\n")
    print(f"REAL RESULT = {part_two('input.txt')}")
