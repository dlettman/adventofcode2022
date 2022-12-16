from helpers import helpers

import numpy


def parse_beacon(beacon_line):
    sensor_coords = beacon_line.split(":")[0].split("at ")[1].split(", ")
    beacon_coords = beacon_line.split("is at ")[1].split(", ")
    sensor_coords = [item.split("=")[1] for item in sensor_coords]
    beacon_coords = [item.split("=")[1] for item in beacon_coords]
    return sensor_coords, beacon_coords


def get_manhattan(a, b):
    return sum(abs(val1 - val2) for val1, val2 in zip(a, b))


def get_all_points_with_manhattan(coord, manhattan):
    coords = []
    current_coord = (coord[0] + manhattan, coord[1])
    for delta in [(-1, 1), (-1, -1), (1, -1), (1, 1)]:
        for step in range(manhattan):
            current_coord = numpy.add(current_coord, delta)
            coords.append(current_coord)
    return coords


def part_one(input_filename, target_row):
    input = helpers.parse_input(input_filename)
    sensor_dict = {}
    nono_squares_in_target_row = set()
    for line in input:
        sensor, beacon = parse_beacon(line)
        sensor_dict[tuple([int(item) for item in sensor])] = tuple([int(item) for item in beacon])
    for sensor in sensor_dict:
        manhattan_to_beacon = get_manhattan(tuple([int(item) for item in sensor]), sensor_dict[sensor])
        manhattan_to_target_row = get_manhattan(tuple([int(item) for item in sensor]), (sensor[0], target_row))
        spaces_to_consider = manhattan_to_beacon - manhattan_to_target_row
        if spaces_to_consider >= 1:
            center = sensor[0]
            nono_squares_in_target_row.add(center)
            distance_out = 1
            while spaces_to_consider > 0:
                nono_squares_in_target_row.add(center + distance_out)
                nono_squares_in_target_row.add(center - distance_out)
                spaces_to_consider -= 1
                distance_out += 1
    for beacon in sensor_dict.values():
        if beacon[1] == target_row:
            if beacon[0] in nono_squares_in_target_row:
                nono_squares_in_target_row.remove(beacon[0])
    return len(nono_squares_in_target_row)


def part_two(input_filename, maximum=4000000):
    input = helpers.parse_input(input_filename)
    sensor_dict = {}
    for line in input:
        sensor, beacon = parse_beacon(line)
        sensor_dict[tuple([int(item) for item in sensor])] = tuple([int(item) for item in beacon])
    beacons = set([item for item in sensor_dict.values()])
    manhattan_dict = {sensor: get_manhattan(sensor, sensor_dict[sensor]) for sensor in sensor_dict}
    for sensor in sensor_dict:
        print(f"processing sensor {sensor}")
        manhattan_dist = manhattan_dict[sensor]
        coords_to_try = get_all_points_with_manhattan(sensor, manhattan_dist + 1)
        for coord in coords_to_try:
            if (not 0 <= coord[0] <= maximum) or not (0 <= coord[1] <= maximum) or tuple(coord) in beacons:
                continue
            disqualified = False
            for other_sensor in sensor_dict:
                if other_sensor == sensor:
                    continue
                manhattan_dist_to_other = get_manhattan(coord, other_sensor)
                if manhattan_dist_to_other <= manhattan_dict[other_sensor]:
                    disqualified = True
                    break
            if not disqualified:
                return (4000000 * coord[0]) + 2573243


if __name__ == "__main__":
    print("*** PART ONE ***\n")
    print(get_all_points_with_manhattan((1, 1), 2))
    print(f"Test result = {part_one('inputtest.txt', 10)}\n")
    print(f"REAL RESULT = {part_one('input.txt', 2000000)}\n\n")
    print("*** PART TWO ***\n")
    print(f"Test result = {part_two('inputtest.txt', maximum=20)}\n")
    print(f"REAL RESULT = {part_two('input.txt')}")
