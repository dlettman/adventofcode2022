from operator import add, sub, mul, truediv
import re

OPERATION_MAP = {"+": add, "-": sub, "*": mul, "/": truediv}

class Node(object):
    def __init__(self, name, left_name=None, right_name=None, number=None, operation=None):
        self.name = name
        self.left_name = left_name
        self.right_name = right_name
        # This is a HARD locked in number
        self.number = number
        if operation not in OPERATION_MAP and operation is not None:
            raise ValueError("WTF is that operator??")
        self._operation = operation

    def __repr__(self) -> str:
        return self.name

    def calculate_number(self, is_part_1=True):
        if self.number is not None:
            return self.number
        # need to calculate
        left_monkey = self.node_map[self.left_name]
        right_monkey = self.node_map[self.right_name]
        left_number = left_monkey.calculate_number()
        right_number = right_monkey.calculate_number()
        if self.name != "root" or is_part_1:
            return self.operation(left_number, right_number)
        # we have entered part2 and are on root
        return left_number, right_number, left_number - right_number

    @property
    def operation(self):
        if not self._operation:
            raise ValueError("Operation not defined for this Node!")
        return OPERATION_MAP[self._operation]

    @operation.setter
    def operation(self, val):
        if val not in OPERATION_MAP:
            print("just saw val", val)
            raise ValueError("WTF is that operator??")
        self._operation = val

    def add_in_node_map(self, node_map):
        self.node_map =node_map

def transform(line):
    m = re.match(
        r"(?P<monkey_name>\w+): (?P<monkey_number>\d+)",
        line,
    )
    if m is not None:
        # Monkey is a number monkey
        info = m.groupdict()
        return Node(info["monkey_name"], number=int(info["monkey_number"]))
    m = re.match(
        r"(?P<monkey_name>\w+): (?P<monkey_left_name>\w+) (?P<operation_symbol>[-/+*]) (?P<monkey_right_name>\w+)",
        line,
    )
    if m is None:
        # should not happen! but JIC...
        raise RuntimeError("uh oh boss, there's a tiger out here")
    info = m.groupdict()
    return Node(info["monkey_name"], info["monkey_left_name"], info["monkey_right_name"], operation=info["operation_symbol"])


def part1(inp):
    node_map = {}
    for node in inp:
        node_map[node.name] = node
    for node in inp:
        node.add_in_node_map(node_map)
    root_node = node_map["root"]
    return root_node.calculate_number()


def part2():
    with open("input.txt") as file:
        inp = file.readlines()
    inp = [transform(line) for line in inp]

    node_map = {}
    for node in inp:
        node_map[node.name] = node
    for node in inp:
        node.add_in_node_map(node_map)

    human_node = node_map["humn"]
    root_node = node_map["root"]

    EPSILON = 0.01
    # NOTE you might need to flip-flop `difference` to negative depending on input
    difference = 999999999999  # arbitrarily big
    delta_size = 1_000_000_000_000
    direction = 1  # +1 or -1, increment or decrement
    step_scale = 10
    human_number = 0
    while abs(difference) > EPSILON:
        human_number += (delta_size * direction)
        print(f"human_number: {human_number}")
        human_node.number = human_number
        left_number, right_number, difference = root_node.calculate_number(is_part_1=False)
        print(f"left: {'{:.1E}'.format(left_number)} -- right: {'{:.1E}'.format(right_number)}")
        print(f"difference: {'{:.4E}'.format(difference)}")
        if (direction > 0 and difference < 0) or (direction < 0 and difference > 0):
            # we jumped the 0 line!, change directions, shrink scale!
            delta_size = delta_size / step_scale
            direction = -1 * direction
    return human_number


if __name__=="__main__":
    print(part2())