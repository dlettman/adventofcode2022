from helpers import helpers

from collections import deque

import networkx as nx
import matplotlib.pyplot as plt

from functools import lru_cache

# Defining a Class
class GraphVisualization:

    def __init__(self):
        # visual is a list which stores all
        # the set of edges that constitutes a
        # graph
        self.visual = []

    # addEdge function inputs the vertices of an
    # edge and appends it to the visual list
    def addEdge(self, a, b):
        temp = [a, b]
        self.visual.append(temp)

    # In visualize function G is an object of
    # class Graph given by networkx G.add_edges_from(visual)
    # creates a graph with a given list
    # nx.draw_networkx(G) - plots the graph
    # plt.show() - displays the graph
    def visualize(self):
        G = nx.Graph()
        G.add_edges_from(self.visual)
        nx.draw_networkx(G)
        plt.savefig('thegraph.png', dpi = 300)
        plt.show()


# Driver code
# G = GraphVisualization()
# G.addEdge(0, 2)
# G.addEdge(1, 2)
# G.addEdge(1, 3)
# G.addEdge(5, 3)
# G.addEdge(3, 4)
# G.addEdge(1, 0)
# G.visualize()


class State(object):

    def __init__(self, time_remaining, location, pressure_released, open_valves):
        self.time_remaining = time_remaining
        self.location = location
        self.pressure_released = pressure_released
        self.open_valves = open_valves
        self.seen = set()


def make_graph(input_text):
    graph = {}
    G = GraphVisualization()
    for line in input_text:
        valve = line.split(" has ")[0].split(" ")[1]
        flow_rate = int(line.split("=")[1].split(";")[0])
        dests = line.split(" to ")[1].split(" ")[1:]
        dests = [item.strip(", ") for item in dests]
        graph[valve] = {"rate": flow_rate, "dests": dests}
        for dest in dests:
            G.addEdge(valve, dest)
    G.visualize()
    return graph


def add_pressure(graph, open_valves):
    return sum([graph[open_valve]["rate"] for open_valve in open_valves])


def part_one(input_filename):
    input_text = helpers.parse_input(input_filename)
    most_pressure = 0
    graph = make_graph(input_text)
    print(graph)
    queue = deque([State(30, "AA", 0, [])])
    while queue:
        current_state = queue.popleft()
        print(f"location = {current_state.location} time remaining = {current_state.time_remaining} ")
        if current_state.time_remaining == 0:
            most_pressure = max(current_state.pressure_released, most_pressure)
            continue
        moved = False
        current_state.seen.add(current_state.location)
        if not current_state.location in current_state.open_valves and graph[current_state.location]["rate"] > 0: # open valve
            queue.append(State(current_state.time_remaining - 1, current_state.location, current_state.pressure_released + add_pressure(graph, current_state.open_valves), current_state.open_valves + [current_state.location]))
            moved = True
        for location in graph[current_state.location]["dests"]: # move to each possible destination
            if location not in current_state.seen:
                queue.append(State(current_state.time_remaining - 1, location, current_state.pressure_released + add_pressure(graph, current_state.open_valves), current_state.open_valves))
                moved = True
        if not moved:
            most_pressure = max(current_state.pressure_released, most_pressure)
            continue
    return most_pressure


def part_two(input_filename):
    input = helpers.parse_input(input_filename)
    score = 0
    for line in input:
        pass
    return score


if __name__ == "__main__":
    print("*** PART ONE ***\n")
    print(f"Test result = {part_one('inputtest.txt')}\n")
    # print(f"REAL RESULT = {part_one('input.txt')}\n\n")
    print("*** PART TWO ***\n")
    print(f"Test result = {part_two('inputtest.txt')}\n")
    print(f"REAL RESULT = {part_two('input.txt')}")
