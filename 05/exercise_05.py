from helpers import helpers


def part_one(input_filename):
    input = helpers.parse_input(input_filename)
    score = 0
    # parse input
    stacks = {n: [] for n in range(1, 10)}
    for line in input:
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
                else:
                    offset_counter +=1
                    offset += 4
            except IndexError:
                offset_counter = 1
                offset = 1
                break
    print(stacks)
    print("***")
    stacks = {k: v[::-1] for k, v in stacks.items()}
    # do stuff here
    for line in input:
        if not line.startswith("move"):
            continue
        print(line)
        _, quantity, _, source, _, dest = line.split(" ")
        for _ in range(int(quantity)):
            popped = stacks[int(source)].pop()
            stacks[int(dest)].append(popped)
            print(stacks)
    print(stacks)

    return "".join(stacks[key][-1] for key in range(1,10) if stacks[key])


def part_two(input_filename):
    input = helpers.parse_input(input_filename)
    score = 0
    # parse input
    stacks = {n: [] for n in range(1, 10)}
    for line in input:
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
                else:
                    offset_counter +=1
                    offset += 4
            except IndexError:
                offset_counter = 1
                offset = 1
                break
    print(stacks)
    print("***")
    stacks = {k: v[::-1] for k, v in stacks.items()}
    # do stuff here
    for line in input:
        if not line.startswith("move"):
            continue
        print(line)
        _, quantity, _, source, _, dest = line.split(" ")
        popoff = stacks[int(source)][-1 * int(quantity):]
        stacks[int(source)] = stacks[int(source)][0:-1 * int(quantity)]
        stacks[int(dest)] = stacks[int(dest)] + popoff
        # for _ in range(int(quantity)):
        #     popped = stacks[int(source)].pop()
        #     stacks[int(dest)].append(popped)
        #     print(stacks)
    print(stacks)

    return "".join(stacks[key][-1] for key in range(1,10) if stacks[key])


if __name__ == "__main__":
    print("*** PART ONE ***\n")
    print(f"Test result = {part_one('inputtest.txt')}\n")
    # print(f"REAL RESULT = {part_one('input.txt')}\n\n")
    print("*** PART TWO ***\n")
    print(f"Test result = {part_two('inputtest.txt')}\n")
    print(f"REAL RESULT = {part_two('input.txt')}")
