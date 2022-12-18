from collections import deque, namedtuple
from dataclasses import dataclass

import heapq

from helpers import helpers

@dataclass(frozen=True, order=True)
class State:
    """Track current state of system
    Will have a bunch of them running around at once."""
    # Score is NEGATIVE, b/c we want to be able to sort on it
    golf_score: int
    curr_node_key: str
    time_left: int
    # This is a STRING of space separated node keys for all opened valves
    open_node_keys: str


@dataclass(frozen=True, order=True)
class HumEleState:
    """Track current state of system of both Humans and Elephants
    Will have a bunch of them running around at once."""
    # Score is NEGATIVE, b/c we want to be able to sort on it
    # human or elephant being en route to valve still changes score
    # just knowing it will eventually happen causes score to improve.
    golf_score: int
    # Human -- Will be at node and done opening at human time
    hum_node: str
    hum_time_active: int
    # Elephant -- Will be at node and done opening at human time
    ele_node: str
    ele_time_active: int
    # This is a STRING of space separated node keys for all opened valves
    # It ALSO includes valves that /will/ be opened according to current plan
    # i.e., a human or an elephant is currently en route there
    open_node_keys: str
    cycle: int


class Node:
    def __init__(self, valve: str, flow_rate: int, neighbors: list[str]):
        self.valve = valve
        self.flow_rate = flow_rate
        self.neighbors = neighbors

    def __repr__(self):
        return f"Node<{self.valve}, {self.flow_rate}, {self.neighbors}>"

    def add_in_dist_map(self, graph):
        """Puts in a self.dist_map
        {valve: distance to that valve from this Node (int)}
        """
        self.graph = graph
        dist_map = {}
        for node_key, target_node in graph.items():
            if node_key == self.valve:
                continue
            if target_node.flow_rate:
                seen = set()
                queue = deque([(self.valve, 0)]) # (location, cost)
                found = False
                while (not found) and queue:
                    current_loc, current_cost = queue.popleft()
                    seen.add(current_loc)
                    for neighbor in graph[current_loc].neighbors:
                        if neighbor == target_node.valve:
                            dist_map[node_key] = current_cost + 1
                            found = True
                            break
                        if neighbor in seen:
                            continue
                        queue.append(tuple([neighbor, current_cost + 1]))
        self.dist_map = dist_map
        return dist_map

    def humele_find_best_option_from_here(self, time_remaining, disallowed_nodes=None):
        """NOTE score returned is POSITIVE here, not a golf score
        disallowed_nodes could be because they're already opened /and/or/ we
        are excluding them from consideration to consider alternative universes
        disallowed_nodes is same structure as `open_node_keys`, space separated
        """
        disallowed_nodes = disallowed_nodes or ""
        best_node = None  # This returning as None signals there is no better from here
        best_score = 0
        best_time_remaining = None
        for node, dist in self.dist_map.items():
            if node in disallowed_nodes:
                continue
            if time_remaining < dist + 2:
                # no reason to investigate, not going to get value from opening the valve
                print("couldn't get any value")
                continue
            time_remaining_once_done = time_remaining - (dist + 1)
            expected_value = time_remaining_once_done * self.graph[node].flow_rate
            print(f" expected value of moving {dist} and pumping {node} on turn {26 - time_remaining_once_done} = {expected_value}")
            if best_score < expected_value:
                best_node = node
                best_score = expected_value
                best_time_remaining = time_remaining_once_done
        return (best_score, best_node, best_time_remaining)


def make_graph(input_text):
    # input_text is a list of strings where each line in the input is a string
    graph = {}
    for line in input_text:
        valve = line.split(" has ")[0].split(" ")[1]
        flow_rate = int(line.split("=")[1].split(";")[0])
        dests = line.split(" to ")[1].split(" ")[1:]
        dests = [item.strip(", ") for item in dests]
        node = Node(valve, flow_rate, dests)
        graph[valve] = node
    return graph


def make_humele_state_using_option(curr_state: HumEleState, option, actor: str = "human"):
    """Creates a new State from current and a best_option
    if option indicated no better option, returns None
    """
    pos_score, dest_node, time_remaining_once_opened = option
    if dest_node is None:  # option said there was nowhere else to go
        return None
    hum_node, hum_time_active, ele_node, ele_time_active = curr_state.hum_node, curr_state.hum_time_active, curr_state.ele_node, curr_state.ele_time_active
    if actor == "human":  # update human stuff
        hum_node = dest_node
        hum_time_active = 26 - (time_remaining_once_opened + 2)
        print("hum next active = ", hum_time_active)
    elif actor == "elephant":  # update elephant stuff
        ele_node = dest_node
        ele_time_active = 26 - (time_remaining_once_opened + 2)
        print("ele next active = ", ele_time_active)
    newstate = HumEleState(
        curr_state.golf_score - pos_score,
        hum_node,
        hum_time_active,
        ele_node,
        ele_time_active,
        curr_state.open_node_keys + " " + dest_node,
        curr_state.cycle
    )
    # print(f"returning {newstate}")
    return newstate

def part_two(inp):
    # how many branching universes we try from every node
    BRANCH_COUNT = 10000
    # how many states we consider at maximum, drop worst scoring
    MAX_UNIVERSE_COUNT = 10000
    STARTING_NODE_KEY = "AA"
    STARTING_TIME = 26

    inp = helpers.parse_input(inp)

    graph = make_graph(inp)
    for node in graph.values():
        node.add_in_dist_map(graph)

    # where we hold all of our states we consider worth investigation
    start_state = HumEleState(0, STARTING_NODE_KEY, 0, STARTING_NODE_KEY, 0, "", 0)
    # IMPORTANT, we assume multiverse is sorted, because it comes from
    # the `heap` below every cycle. We RELY ON IT BEING SORTED.
    multiverse = deque([start_state])
    for cycle in range(0, STARTING_TIME - 1):
        print("X" * 20 + "DEBUG -- on cycle", cycle + 1,  "\n")
        print("DEBUG -- on cycle", cycle + 1)
        heap = []  # heap of next possibilities
        while multiverse:
            state = multiverse.popleft()
            new_cycle = state.cycle + 1
            if state.cycle == state.hum_time_active or state.cycle == state.ele_time_active:
                next_state = None
                hum_options_tried, ele_options_tried = "", ""
                print("open nodes = ", state.open_node_keys)
                branches_explored = 0
                while branches_explored < BRANCH_COUNT:
                    hum_dest = ""
                    disallowed_node_keys = state.open_node_keys
                    if state.cycle == state.hum_time_active:  # human takes their turn
                        branches_explored += 1
                        hum_curr_node: Node = graph[state.hum_node]
                        option = hum_curr_node.humele_find_best_option_from_here(
                            STARTING_TIME - state.cycle,
                            disallowed_node_keys + " " + hum_options_tried,
                        )
                        next_state = make_humele_state_using_option(state, option, actor="human")
                        if not next_state:
                            continue
                        print("hum going to ", next_state.hum_node)
                        hum_options_tried += " " + next_state.hum_node
                        hum_dest =  next_state.hum_node
                        while branches_explored < BRANCH_COUNT:
                            branches_explored += 1
                            ele_curr_node: Node = graph[state.ele_node]
                            option = ele_curr_node.humele_find_best_option_from_here(
                                STARTING_TIME - state.cycle,
                                disallowed_node_keys + " " + ele_options_tried + " " + hum_dest,
                            )
                            if next_state:
                                print("hum and ele both acting")
                                next_state = make_humele_state_using_option(next_state, option, actor="elephant")
                            else:
                                next_state = make_humele_state_using_option(state, option, actor="elephant")
                            if not next_state:
                                continue
                            print("ele going to ", next_state.ele_node)
                            disallowed_node_keys += " " + next_state.ele_node
                            ele_options_tried += " " + next_state.ele_node
                            if next_state:
                                next_state = HumEleState(next_state.golf_score, next_state.hum_node,
                                                         next_state.hum_time_active, next_state.ele_node,
                                                         next_state.ele_time_active, next_state.open_node_keys,
                                                         new_cycle)
                                heapq.heappush(heap, next_state)
                            else:
                                next_state = HumEleState(state.golf_score, state.hum_node, state.hum_time_active,
                                                         state.ele_node, state.ele_time_active, state.open_node_keys,
                                                         new_cycle)
                                heapq.heappush(heap, next_state)
                            next_state = None
                    elif state.cycle == state.ele_time_active: # ele takes their turn
                        ele_curr_node: Node = graph[state.ele_node]
                        option = ele_curr_node.humele_find_best_option_from_here(
                            STARTING_TIME - state.cycle,
                            disallowed_node_keys + " " + ele_options_tried + " " + hum_dest,
                        )
                        if next_state:
                            print("hum and ele both acting")
                            next_state = make_humele_state_using_option(next_state, option, actor="elephant")
                        else:
                            next_state = make_humele_state_using_option(state, option, actor="elephant")
                        if not next_state:
                            continue
                        print("ele going to ", next_state.ele_node)
                        disallowed_node_keys += " " + next_state.ele_node
                        ele_options_tried += " " + next_state.ele_node
                    if next_state:
                        next_state = HumEleState(next_state.golf_score, next_state.hum_node, next_state.hum_time_active, next_state.ele_node, next_state.ele_time_active, next_state.open_node_keys, new_cycle)
                        heapq.heappush(heap, next_state)
                    else:
                        next_state = HumEleState(state.golf_score, state.hum_node, state.hum_time_active, state.ele_node, state.ele_time_active, state.open_node_keys, new_cycle)
                        heapq.heappush(heap, next_state)
                if not heap:
                    next_state = HumEleState(state.golf_score, state.hum_node, state.hum_time_active, state.ele_node,
                                             state.ele_time_active, state.open_node_keys, new_cycle)
                    heapq.heappush(heap, next_state)
            else:
                # print("no moves")
                next_state = HumEleState(state.golf_score, state.hum_node, state.hum_time_active,
                                         state.ele_node, state.ele_time_active, state.open_node_keys,
                                         new_cycle)
                heapq.heappush(heap, next_state)
        heap.sort()
        top_range = max(MAX_UNIVERSE_COUNT, len(heap))
        print(f"{len(heap)} possibilities")
        multiverse = deque(heap[0:top_range])
    heap.sort()
    return heap[0]


if __name__ == "__main__":
    print("*** PART ONE ***\n")
    # print(f"Test result = {part_one('inputtest.txt')}\n")
    # print(f"REAL RESULT = {part_one('input.txt')}\n\n")
    print("*** PART TWO ***\n")
    print(f"Test result = {part_two('inputtest.txt')}\n")
    # print(f"REAL RESULT = {part_two('input.txt')}")