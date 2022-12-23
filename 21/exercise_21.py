from helpers import helpers
from operator import add, sub, mul, floordiv, eq
from sympy import symbols, solve


OPERATOR_MAP = {"+": add,
                "-": sub,
                "/": floordiv,
                "*": mul,
                "=": eq}


class GetYourPawsOffMeYouDirtyApe(Exception):
    pass


class MonkeyNode(object):

    def __init__(self, name, left=None, right=None, number=None, operation=None):
        self.name = name
        self.left = left
        self.right = right
        self.number = number
        self.operation = operation

    def __repr__(self) -> str:
        return f"Monkeynode: {self.name}"
        # return f"{self.name}: Number: {self.number}, Left = {self.left.name if self.left else 'None'}, Right = {self.right.name if self.right else 'None'}, Operation = {self.operation}"

    def addleft(self, node):
        self.left = node

    def addright(self, node):
        self.right = node

    def solve(self):
        print(f"solving {self.name}")
        print(f"left right = {self.left}, {self.right}")
        if self.name == "humn":
            raise GetYourPawsOffMeYouDirtyApe
        try:
            if self.number:
                print(f"hit bottom, returning {self.number}")
                return self.number
            else:
                print("solving left")
                print(f"self.left = {self.left}")
                left = self.left.solve()
                print("solving right")
                print(f"self.right = {self.right}")
                right = self.right.solve()
                print(f"self.operation = {self.operation}")
                self.number = self.operation(left, right)
                return self.number
        except GetYourPawsOffMeYouDirtyApe:
            print("Human is on this side")
            raise GetYourPawsOffMeYouDirtyApe



def parse_monkeys(input_text):
    monkey_list = []
    monkey_dict = {}
    for line in input_text:
        print(line)
        name, command = line.split(": ")
        command = command.split(" ")
        monkey_list.append(name)
        monkey_dict[name] = {}
        if len(command) == 1:
            monkey_dict[name]["number"] = int(command[0])
        else:
            monkey_dict[name]["operation"] = command
    return monkey_dict, monkey_list


def parse_monkeys_into_nodes(input_text):
    monkey_dict = {}
    for line in input_text:
        name, command = line.split(": ")
        command = command.split(" ")
        monkey = monkey_dict[name] if name in monkey_dict else MonkeyNode(name)
        if len(command) == 1:
            monkey.number = int(command[0])
        else:
            left, operation, right = command
            if left not in monkey_dict:
                left_monkey = MonkeyNode(left)
                monkey_dict[left] = left_monkey
            monkey.left = monkey_dict[left]
            if right not in monkey_dict:
                right_monkey = MonkeyNode(right)
                monkey_dict[right] = right_monkey
            monkey.right = monkey_dict[right]
            monkey.operation = OPERATOR_MAP[operation]
            # print(f"{monkey.name} left = {monkey.left}, {monkey.name} right = {monkey.right}")
            if name == "root":
                monkey.operation = "="
        monkey_dict[monkey.name] = monkey
    return monkey_dict


def part_one(input_filename):
    input = helpers.parse_input(input_filename)
    monkey_dict, monkey_list = parse_monkeys(input)
    print(monkey_dict)

    while True:
        for monkey in monkey_list:
            print(monkey)
            if monkey == "root":
                if "number" in monkey_dict[monkey]:
                    return monkey_dict[monkey]["number"]
            if "number" in monkey_dict[monkey]:
                continue
            elif "operation" in monkey_dict[monkey]:
                print(monkey_dict[monkey])
                print(monkey_dict[monkey_dict[monkey]["operation"][0]])
                if "number" in monkey_dict[monkey_dict[monkey]["operation"][0]] and "number" in monkey_dict[monkey_dict[monkey]["operation"][2]]:
                    print(monkey_dict[monkey]["operation"])
                    print(monkey_dict[monkey_dict[monkey]["operation"][0]])
                    print(monkey_dict[monkey_dict[monkey]["operation"][2]])
                    monkey_dict[monkey]["number"] = OPERATOR_MAP[monkey_dict[monkey]["operation"][1]](monkey_dict[monkey_dict[monkey]["operation"][0]]["number"], monkey_dict[monkey_dict[monkey]["operation"][2]]["number"])





def part_two(input_filename):
    input = helpers.parse_input(input_filename)
    monkey_dict = parse_monkeys_into_nodes(input)
    print(monkey_dict)

    root = monkey_dict["root"]
    print(root)
    root_left, root_right = root.left, root.right
    print(root_left, root_right)
    pointer = root
    magic_number = None
    while True:
        # Solve the side the human is not on, that gives us our 'magic number'
        # Apply the inverse operation to the magic magic number (e.g. 1 + x =
        for top_node in [pointer.left, pointer.right]:
            try:
                top_node.number = top_node.solve()
            except GetYourPawsOffMeYouDirtyApe:
                pointer = top_node
                continue
            pointer.number = solve(pointer.left.number, magic_number
            magic_number = solve(top_node.left.number)



if __name__ == "__main__":
    print("*** PART ONE ***\n")
    # print(f"Test result = {part_one('inputtest.txt')}\n")
    # print(f"REAL RESULT = {part_one('input.txt')}\n\n")
    print("*** PART TWO ***\n")
    print(f"Test result = {part_two('inputtest.txt')}\n")
    # print(f"REAL RESULT = {part_two('input.txt')}")
