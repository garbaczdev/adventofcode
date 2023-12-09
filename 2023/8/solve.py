#!/usr/bin/env python3
from sys import argv
from datetime import datetime

from math import lcm


def get_input(filename: str):
    with open(filename, "r") as f:
        instructions, map_raw = f.read().split("\n\n")
        _map = { 
            line.split(" = ")[0]: tuple(
                line.split(" = ")[1].replace("(", "").replace(")", "").split(", ")
            )
            for line in map_raw.split("\n") if line.split()
        }

    return (instructions, _map)


def part1(_in):
    instructions, _map = _in

    current = "AAA"
    steps = 0
    while current != "ZZZ":
        current = _map[current][0] if instructions[steps % len(instructions)] == "L" else _map[current][1]
        steps += 1
    return steps


def get_cycle_data(instructions, _map, start_node) -> tuple:

    visited = [(start_node, instructions[0])]
    while visited[-1] not in visited[:-1]:
        current = visited[-1][0]
        step = (len(visited)-1) % len(instructions)
        visited.append((_map[current][0] if instructions[step] == "L" else _map[current][1], step))

    cycle_start_index = visited.index(visited[-1])
    cycle_length = len(visited) - cycle_start_index - 1
    first_z_in_cycle = [index for index, node in enumerate(visited) if node[0][-1] == "Z"][0] - cycle_start_index
    
    return (cycle_start_index, cycle_length, first_z_in_cycle)



def part2(_in):
    instructions, _map = _in

    start_nodes = {key: get_cycle_data(instructions, _map, key) for key in _map.keys() if key[-1] == "A"}
    return lcm(*[cycle_length for cycle_index, cycle_length, z_index in start_nodes.values()])



def benchmark(name: str, func, *_in) -> None:
    now = datetime.now()
    result = func(*_in)
    _time = datetime.now() - now
    print(f"({_time}) {name}: {result}")


def main() -> None:
    if len(argv) < 2:
        print("Provide the file name")
        return
    _in = get_input(argv[1])
    benchmark("PART 1", part1, _in)
    benchmark("PART 2", part2, _in)


if __name__ == "__main__":
    main()
