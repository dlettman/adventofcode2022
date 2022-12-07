from helpers import helpers


def get_subfoders_under_100k(folder):
    total = 0
    can_add_more = True
    for subfolder in folder.keys():
        if subfolder in ["size"]:
            continue
        else:
            guaranteed, for_now_can_add_more = get_subfoders_under_100k(folder[subfolder])
            if not for_now_can_add_more:
                can_add_more = False
            total += guaranteed
    if can_add_more:
        if "size" in folder:
            print("NO", folder)
            if folder["size"] + total <= 100000:
                total += folder["size"] + total
            else:
                can_add_more = False
        else:
            total += total

    return (total, can_add_more)


def get_size(folder):
    total = 0
    for subfolder in folder.keys():
        if subfolder in ["size"]:
            continue
        else:
            sub_size = get_size(folder[subfolder])
            print(f"{subfolder}, {sub_size}")
            total += sub_size
    # total += total
    if "size" in folder:
        total += folder["size"]
    return total



def part_one(input_filename):
    input = helpers.parse_input(input_filename)
    hierarchy = {"/": {}}
    current_dir = hierarchy["/"]
    outer_dirs = []
    for line in input:
        if line.startswith("$"):
            command = line.split(" ")[1:]
            if command[0] == "cd":
                if command[1] == "/":
                    current_dir = hierarchy["/"]
                    outer_dirs = []
                elif command[1] == "..":
                    current_dir = hierarchy["/"]
                    if len(outer_dirs):
                        for dir in outer_dirs[:-1]:
                            current_dir = current_dir[dir]
                        outer_dirs.pop()
                else:
                    outer_dirs.append(command[1])
                    current_dir = current_dir[command[1]]
            elif command[0] == "ls":
                continue
        else:  # ls or dir
            split_line = line.split(" ")
            if split_line[0].isnumeric():
                if "size" not in current_dir:
                    current_dir["size"] = int(split_line[0])
                else:
                    current_dir["size"] += int(split_line[0])

            elif split_line[0] == "dir":
                # make new directory
                current_dir[split_line[1]] = {}

    print(hierarchy)

    return get_subfoders_under_100k(hierarchy["/"])



def part_two(input_filename):
    input = helpers.parse_input(input_filename)
    hierarchy = {"/": {}}
    current_dir = hierarchy["/"]
    outer_dirs = []
    for line in input:
        if line.startswith("$"):
            command = line.split(" ")[1:]
            if command[0] == "cd":
                if command[1] == "/":
                    current_dir = hierarchy["/"]
                    outer_dirs = []
                elif command[1] == "..":
                    current_dir = hierarchy["/"]
                    if len(outer_dirs):
                        for dir in outer_dirs[:-1]:
                            current_dir = current_dir[dir]
                        outer_dirs.pop()
                else:
                    outer_dirs.append(command[1])
                    current_dir = current_dir[command[1]]
            elif command[0] == "ls":
                continue
        else:  # ls or dir
            split_line = line.split(" ")
            if split_line[0].isnumeric():
                if "size" not in current_dir:
                    current_dir["size"] = int(split_line[0])
                else:
                    current_dir["size"] += int(split_line[0])

            elif split_line[0] == "dir":
                # make new directory
                current_dir[split_line[1]] = {}


    return get_size(hierarchy["/"])


if __name__ == "__main__":
    print("*** PART ONE ***\n")
    # print(f"Test result = {part_one('inputtest.txt')}\n")
    # print(f"REAL RESULT = {part_one('input.txt')}\n\n")
    print("*** PART TWO ***\n")
    print(f"Test result = {part_two('inputtest.txt')}\n")
    print(f"REAL RESULT = {part_two('input.txt')}")
