from helpers import helpers


def get_size_of_folders_under_100k(folder):
    total = 0
    size_under_limit = True
    for subfolder in folder.keys():
        if subfolder == "size":
            continue
        else:
            bubbled_up_size, subfolder_size_under_limit = get_size_of_folders_under_100k(folder[subfolder])
            if not subfolder_size_under_limit:
                size_under_limit = False
            total += bubbled_up_size
    if size_under_limit:
        if "size" in folder:
            if folder["size"] + total <= 100000:
                total += folder["size"] + total
            else:
                size_under_limit = False
        else:  # No files in this folder. The size is just the sum of the subfolder sizes
            total += total
    return total, size_under_limit


def get_size(folder, size_map):
    total = 0
    for subfolder in folder.keys():
        if subfolder in ["size"]:
            continue
        else:
            _, sub_size = get_size(folder[subfolder], size_map)
            size_map[subfolder] = sub_size
            total += sub_size
    if "size" in folder:
        total += folder["size"]
    return size_map, total


def make_file_system(input_text):
    file_system = {"/": {}}
    current_dir = file_system["/"]
    current_working_path = []
    for line in input_text:
        if line.startswith("$"):
            command = line.split(" ")[1:]

            if command[0] == "cd":
                parameter = command[1]
                if parameter == "/":
                    current_dir = file_system["/"]
                    current_working_path = []
                elif parameter == "..":
                    current_dir = file_system["/"]
                    if len(current_working_path):
                        for dir in current_working_path[:-1]:
                            current_dir = current_dir[dir]
                        current_working_path.pop()
                else:
                    current_working_path.append(parameter)
                    current_dir = current_dir[parameter]

            elif command[0] == "ls":  # output of ls gets handled below, so the line itself is a noop
                continue

        else:  # parse output of ls
            split_line = line.split(" ")
            if split_line[0].isnumeric():
                if "size" not in current_dir:
                    current_dir["size"] = int(split_line[0])
                else:
                    current_dir["size"] += int(split_line[0])
            elif split_line[0] == "dir":
                # add directory to file_system
                current_dir[split_line[1]] = {}

    return file_system


def part_one(input_filename):
    input_text = helpers.parse_input(input_filename)
    file_system = make_file_system(input_text)
    return get_size_of_folders_under_100k(file_system["/"])


def part_two(input_filename):
    input_text = helpers.parse_input(input_filename)
    file_system = make_file_system(input_text)
    folder_size_map, _ = get_size(file_system, {})
    folder_size_list = [[folder, size] for folder, size in folder_size_map.items()]
    folder_size_list.sort(key=lambda x: int(x[1]))
    total_file_system_size = folder_size_list[-1][1]
    min_to_delete = 30000000 - (70000000 - total_file_system_size)
    for folder in folder_size_list:
        if int(folder[1]) >= min_to_delete:
            return folder[1]
    return None  # it done broke



if __name__ == "__main__":
    print("*** PART ONE ***\n")
    print(f"Test result = {part_one('inputtest.txt')}\n")
    print(f"REAL RESULT = {part_one('input.txt')}\n\n")
    print("*** PART TWO ***\n")
    print(f"Test result = {part_two('inputtest.txt')}\n")
    print(f"REAL RESULT = {part_two('input.txt')}")
