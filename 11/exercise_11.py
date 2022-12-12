from math import prod
from operator import add, mul


OPERATION_MAP = {
    "+": add,
    "*": mul
}


class Monkey(object):

    def __init__(self, number, starting_items, operation, test_factor, true_target, false_target, part_1=True):
        self.number = number
        self.items = starting_items
        self.operation = operation
        self.divisor = test_factor
        self.true_target = true_target
        self.false_target = false_target
        self.inspection_count = 0
        self.part_1 = part_1

    def __str__(self):
        return f"Monkey {self.number}"

    def inspect_items(self):
        for idx, item in enumerate(self.items):
            self.inspection_count += 1
            new_value = self.operation(item) if not self.part_1 else self.operation(item) // 3
            self.items[idx] = new_value

    def throw_items(self, monkey_map):
        for item in self.items:
            if int(item) % self.divisor == 0:
                monkey_map[self.true_target].items.append(item)
            else:
                monkey_map[self.false_target].items.append(item)
        self.items = []


def parse_monkey_info(monkey):
    monkey_lines = monkey.split("\n")
    number = int(monkey_lines[0].split(" ")[1][0])
    starting_items = [int(item) for item in monkey_lines[1].split(":")[1].strip().split(", ")]
    operation = parse_operation(monkey_lines[2].split(" = ")[1])
    divisor = int(monkey_lines[3].split(" by ")[1])
    true_result = int(monkey_lines[4].split(" ")[-1])
    false_result = int(monkey_lines[5].split(" ")[-1])
    return number, starting_items, operation, divisor, true_result, false_result


def parse_operation(operation):  # Hacky!
    operator, number = operation[4:].split(" ")
    if number == "old":
        return lambda x: mul(x, x)
    return lambda x: OPERATION_MAP[operator](int(number), x)


def part_one(input_filename):
    rounds = 20
    with open(input_filename) as file:
        input_list = file.read()
    monkey_info = input_list.split("\n\n")
    monkey_map = {}
    for monkey in monkey_info:
        args = parse_monkey_info(monkey)
        monkee = Monkey(*args)
        monkey_map[monkee.number] = monkee
    for _ in range(rounds):
        for monkey in range(len(monkey_map)):  # makes sure we go in order
            monkey_map[monkey].inspect_items()
            monkey_map[monkey].throw_items(monkey_map)
    monkey_business = sorted([monkey.inspection_count for monkey in monkey_map.values()])
    print(monkey_business[-2:])
    return prod(monkey_business[-2:])


def part_two(input_filename):
    rounds = 10000
    with open(input_filename) as file:
        input_list = file.read()
    monkey_info = input_list.split("\n\n")
    monkey_map = {}
    for monkey in monkey_info:
        args = parse_monkey_info(monkey)
        this_monkey_right_here_officer = Monkey(*args, part_1=False)
        monkey_map[this_monkey_right_here_officer.number] = this_monkey_right_here_officer
    divisors = [monkey.divisor for monkey in monkey_map.values()]
    divisor_product = prod(divisors)
    for _ in range(rounds):
        for monkey in range(len(monkey_map)):
            monkey_map[monkey].inspect_items()
            monkey_map[monkey].throw_items(monkey_map)
        for monkey in monkey_map.values():
            monkey.items = [item % divisor_product for item in monkey.items]
    monkey_business = sorted([monkey.inspection_count for monkey in monkey_map.values()])
    return prod(monkey_business[-2:])


if __name__ == "__main__":
    print("*** PART ONE ***\n")
    print(f"Test result = {part_one('inputtest.txt')}\n")
    print(f"REAL RESULT = {part_one('input.txt')}\n\n")
    print("*** PART TWO ***\n")
    print(f"Test result = {part_two('inputtest.txt')}\n")
    print(f"REAL RESULT = {part_two('input.txt')}")
