from collections import deque
from copy import deepcopy
from math import prod


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
        return f"MINUTE {self.minute}: BOTS = {self.bots}, INGREDIENTS = {self.ingredients}"

    def __hash__(self):
        return hash(self.__repr__)


NO_BOTS = {"ore": 0,
           "clay": 0,
           "obsidian": 0,
           "geode": 0}

STARTING_INGREDIENTS = {"ore": 0,
               "clay": 0,
               "obsidian": 0,
               "geode": 0}

STARTING_BOTS = {"ore": 1,
        "clay": 0,
        "obsidian": 0,
        "geode": 0}


def create_blueprint_map(blueprint_text):  # I should really use regex
    blueprint_map = {}
    for idx, blueprint in enumerate(blueprint_text):
        recipes = {}
        for line in blueprint:
            robo_type = line.split(" ")[1]
            if "and" in line:
                line = [item.strip(".") for item in line.split(" ")[4:]]
                quantity1, ingredient1, _, quantity2, ingredient2 = line
                recipes[robo_type] = {ingredient1: int(quantity1), ingredient2: int(quantity2)}
            else:
                quantity1, ingredient1, = line.split(" ")[4:]
                recipes[robo_type] = {ingredient1: int(quantity1)}
        blueprint_map[idx + 1] = recipes
    return blueprint_map


def get_bot_options(state, blueprint):
    possible_results = []
    options_queue = deque([deepcopy(state)])  # deepcopy everything JUST TO BE SAFE
    while options_queue:
        cur_option = options_queue.popleft()
        options = get_reasonable_options(blueprint, cur_option.ingredients, cur_option.bots)
        if options:
            for option in options:
                if option == "don't build":
                    possible_results.append(State(deepcopy(state.ingredients),
                                                  deepcopy(state.bots),
                                                  deepcopy(NO_BOTS),
                                                  cur_option.minute))
                else:
                    new_bots = deepcopy(NO_BOTS)
                    new_ingredients = deepcopy(cur_option.ingredients)
                    for ingredient in blueprint[option]:
                        new_ingredients[ingredient] -= blueprint[option][ingredient]
                    new_bots[option] += 1
                    possible_results.append(State(deepcopy(new_ingredients),
                                                  deepcopy(cur_option.bots),
                                                  deepcopy(new_bots),
                                                  cur_option.minute))
    return possible_results


def can_make_it(recipe, resources):
    for ingredient in recipe:
        if not resources[ingredient] >= recipe[ingredient]:
            return False
    return True


def get_reasonable_options(blueprint, resources, bots):
    max_needed = {}  # Since we can only produce one bot per round, we won't build more bots than we'd need in order to harvest enough each turn to build the bot that costs the most of that resource
    options = []
    if can_make_it(blueprint["geode"], resources):
        return ["geode"]  # Always make a geode bot if we can
    for resource in ["ore", "clay", "obsidian"]:
        max_needed[resource] = 0
        for recipe in blueprint:
            if resource in blueprint[recipe]:
                max_needed[resource] = max(blueprint[recipe][resource], max_needed[resource])
    if can_make_it(blueprint["obsidian"], resources):  # If we can't build a geode bot but we can build an obsidian, do it.
        if not bots["obsidian"] >= max_needed["obsidian"]:
            return["obsidian"]
    for resource in ["ore", "clay"]:
        if not bots[resource] >= max_needed[resource]:
            if can_make_it(blueprint[resource], resources):
                options.append(resource)
    if not resources["ore"] > 2 * max_needed["ore"]:  # This seems reasonable...
        options.append("don't build")
    return options


def play_factorio(input_filename, rounds=24):
    with open(input_filename) as file:
        input_list = file.read()
    blueprints = input_list.split("\n")
    blueprints = [item.split(": ")[1].split(". ") for item in blueprints]
    if rounds == 32:
        if len(blueprints) > 3:
            blueprints = blueprints[0:3]
    blueprint_map = create_blueprint_map(blueprints)
    max_geodes = {}
    for idx in blueprint_map:
        queue = deque([State(deepcopy(STARTING_INGREDIENTS), deepcopy(STARTING_BOTS), deepcopy(NO_BOTS), 0)])
        seen_states = set([State(deepcopy(STARTING_INGREDIENTS), deepcopy(STARTING_BOTS), deepcopy(NO_BOTS), 0)])
        blueprint = blueprint_map[idx]
        print(blueprint)

        #  Main 'gameplay' loop
        while queue:
            cur_state = queue.popleft()
            if cur_state in seen_states:  # Does this help? Maybe.
                continue
            seen_states.add(cur_state)
            if cur_state.minute >= rounds:
                queue.append(cur_state)
                break
            if cur_state.minute >= 28:
                if cur_state.bots["geode"] == 0:  # Prune it - at this point we should have at least one geode bot
                    continue
            options = get_bot_options(cur_state, blueprint)
            for option in options:
                for bot_type in option.bots:  # harvest resources
                    option.ingredients[bot_type] += option.bots[bot_type]
                for bot_type in option.bot_factory:  # produce bots
                    option.bots[bot_type] += option.bot_factory[bot_type]
                    option.bot_factory[bot_type] = 0
                option.minute += 1
                queue.append(option)

        # compare scores for this blueprint
        num_geodes = max([option.ingredients["geode"] for option in options])
        max_geodes[idx] = num_geodes

    if rounds == 32:
        print(max_geodes)
        return prod(max_geodes.values())

    return sum([k * v for k, v in max_geodes.items()])


if __name__ == "__main__":
    print("*** PART ONE ***\n")
    print(f"Test result = {play_factorio('inputtest.txt')}\n")
    print(f"REAL RESULT = {play_factorio('input.txt')}\n\n")
    print("*** PART TWO ***\n")
    print(f"Test result = {play_factorio('inputtest.txt', rounds = 32)}\n")
    print(f"REAL RESULT = {play_factorio('input.txt', rounds = 32)}")

