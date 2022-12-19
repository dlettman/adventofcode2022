from helpers import helpers
from dataclasses import dataclass
from collections import deque
from copy import deepcopy


class State(object):
    ingredients: dict
    bots: dict
    bot_factory = dict
    minute = int

    def __init__(self, ingredients, bots, bot_factory, minute):
        self.ingredients = ingredients
        self.bots = bots
        self.bot_factory = bot_factory
        self.minute = minute

    def __repr__(self):
        return f"MINUTE {self.minute + 1}: BOTS = {self.bots}, INGREDIENTS = {self.ingredients}, BOTS IN FACTORY = {self.bot_factory}"


    def __hash__(self):
        return hash(self.__repr__)


NO_BOTS = {"ore": 0,
           "clay": 0,
           "obsidian": 0,
           "geode": 0}


def get_bot_options(state, blueprint):
    possible_results = []
    options_queue = deque([deepcopy(state)])
    while options_queue:
        cur_option = options_queue.popleft()
        possible_results.append(State(deepcopy(cur_option.ingredients),
                                      deepcopy(cur_option.bots),
                                      deepcopy(cur_option.bot_factory),
                                      cur_option.minute))
        for bot_type, recipe in blueprint.items():
            can_make_it = True
            for ingredient in recipe:
                if not cur_option.ingredients[ingredient] >= recipe[ingredient]:
                    can_make_it = False
                    break
            if can_make_it:
                new_ingredients = deepcopy(cur_option.ingredients)
                for ingredient in recipe:
                    new_ingredients[ingredient] -= recipe[ingredient]
                new_bots = deepcopy(cur_option.bot_factory)
                print(new_bots)
                new_bots[bot_type] += 1
                possible_results.append(State(deepcopy(new_ingredients),
                                              deepcopy(cur_option.bots),
                                              deepcopy(new_bots),
                                              cur_option.minute))
                options_queue.append(State(deepcopy(new_ingredients),
                                           deepcopy(cur_option.bots),
                                           deepcopy(new_bots),
                                           cur_option.minute))
    return possible_results




def part_one(input_filename):
    max_geodes = 0
    ingredients = {"ore": 0,
                   "clay": 0,
                   "obsidian": 0,
                   "geode": 0}
    bots = {"ore": 1,
           "clay": 0,
           "obsidian": 0,
           "geode": 0}
    with open(input_filename) as file:
        input_list = file.read()
    blueprints = input_list.split("\n")
    blueprints = [item.split(". ") for item in blueprints]
    blueprint_map = {}
    for idx, blueprint in enumerate(blueprints):
        recipes = {}
        for line in blueprint[1:]:
            robo_type = line.split(" ")[1]
            if "and" in line:
                line = [item.strip(".") for item in line.split(" ")[4:]]
                quantity1, ingredient1, _, quantity2, ingredient2 = line
                recipes[robo_type] = {ingredient1: int(quantity1), ingredient2: int(quantity2)}
            else:
                quantity1, ingredient1, = line.split(" ")[4:]
                recipes[robo_type] = {ingredient1: int(quantity1)}
        blueprint_map[idx + 1] = recipes
    seen_states = set([State(ingredients, bots, deepcopy(NO_BOTS), 0)])
    queue = deque([State(ingredients, bots, deepcopy(NO_BOTS), 0)])
    for idx in blueprint_map:
        blueprint = blueprint_map[idx]
        while queue:
            cur_state = queue.popleft()
            if cur_state.minute > 25:
                queue.append(cur_state)
                break
            options = get_bot_options(cur_state, blueprint)
            for option in options:
                for bot_type in option.bots:  # harvest resources
                    option.ingredients[bot_type] += option.bots[bot_type]
                print(option)
                for bot_type in option.bot_factory: # produce bots
                    if option.bot_factory[bot_type]:
                        option.bots[bot_type] += option.bot_factory[bot_type]
                        option.bot_factory[bot_type] = 0
                option.minute += 1
                if option not in seen_states:
                    seen_states.add(option)
                queue.append(option)
        num_geodes = 0
        for option in queue:
            num_geodes = max(num_geodes, option.ingredients["geode"])
        max_geodes = max(num_geodes, max_geodes)
    return f"blueprint {idx}, num geodes: {max_geodes}"




def part_two(input_filename):
    input = helpers.parse_input(input_filename)
    if not input:
        return "*** NO INPUT SUPPLIED ***"
    # do stuff here
    output = input
    return output


if __name__ == "__main__":
    print("*** PART ONE ***\n")
    print(f"Test result = {part_one('inputtest.txt')}\n")
    print(f"REAL RESULT = {part_one('input.txt')}\n\n")
    print("*** PART TWO ***\n")
    print(f"Test result = {part_two('inputtest.txt')}\n")
    print(f"REAL RESULT = {part_two('input.txt')}")

