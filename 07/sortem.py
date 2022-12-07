from helpers import helpers

def part_one(input_filename):
    input = helpers.parse_input(input_filename)
    input = [item.split(", ") for item in input]
    input.sort(key=lambda x: int(x[1]))
    input = input
    for item in input:
        if int(item[1]) >= 8518336:
            print(f"YOOOO {item}")
            break
    # do stuff here
    output = input
    return output




if __name__ == "__main__":
    print("*** PART ONE ***\n")
    print(f"Test result = {part_one('dumbput.txt')}\n")
