#!/usr/bin/env python3

# =============================================
#  Maciej Garbacz | garbaczdev@gmail.com
#  Advent of Code solutions
#  https://github.com/garbaczdev/adventofcode
# =============================================

from sys import argv
from datetime import datetime

from math import sqrt
from dataclasses import dataclass
from functools import reduce


@dataclass
class JunctionBox:
    _id: int
    x: int
    y: int
    z: int

    def __repr__(self):
        return f"JunctionBox(id={self._id}, x={self.x}, y={self.y}, z={self.z})"

    def distance_to(self, other_box: "JunctionBox") -> int:
        return sqrt(
            (other_box.x - self.x)**2
            + (other_box.y - self.y)**2
            + (other_box.z - self.z)**2
        )


def are_junction_boxes_connected(connections: dict, box1_id: int, box2_id: int) -> bool:
    current_nodes = [box1_id]
    visited_nodes = set()

    while current_nodes:
        node = current_nodes.pop(0)

        if node in visited_nodes:
            continue
        # Mark the current node as visited
        visited_nodes.add(node)

        if node == box2_id:
            break

        for neigbour_node in connections[node]:
            if neigbour_node not in visited_nodes:
                current_nodes.append(neigbour_node)

    return box2_id in visited_nodes


def get_circuit(connections, start_id: int) -> int:
    current_nodes = [start_id]
    visited_nodes = set()

    while current_nodes:
        node = current_nodes.pop(0)

        if node in visited_nodes:
            continue

        # Mark the current node as visited
        visited_nodes.add(node)

        for neigbour_node in connections[node]:
            if neigbour_node not in visited_nodes:
                current_nodes.append(neigbour_node)

    return visited_nodes


def part1(junction_boxes):
    # Precompute all possible connections
    possible_connections = [
        (
            i,
            j,
            junction_boxes[i].distance_to(junction_boxes[j])
        )
        for i in range(len(junction_boxes))
        for j in range(i+1, len(junction_boxes))
    ]
    # Sort them by distance
    possible_connections.sort(key=lambda x: x[2])

    # Adjacency list for the graph
    connections = {
        _id: []
        for _id in range(len(junction_boxes))
    }

    # Connect the junction boxes based on the specified algorithm
    for connection_idx, possible_connection in enumerate(possible_connections):
        if connection_idx >= 1000:
            break

        id_from, id_to, distance = possible_connection

        # Only if there is no connection between those boxes
        if not are_junction_boxes_connected(connections, id_from, id_to):
            connections[id_from].append(id_to)
            connections[id_to].append(id_from)


    # Estimate the circuit sizes by finding distinct circuits
    circuit_sizes = []
    total_visited_nodes = set()
    for _id in range(len(junction_boxes)):
        if _id in total_visited_nodes:
            continue

        visited_nodes = get_circuit(connections, _id)

        circuit_sizes.append(len(visited_nodes))
        total_visited_nodes |= visited_nodes

    circuit_sizes.sort(reverse=True)

    return reduce(lambda x, y: x * y, circuit_sizes[:3])


def part2(junction_boxes):
    # Precompute all possible connections
    possible_connections = [
        (
            i,
            j,
            junction_boxes[i].distance_to(junction_boxes[j])
        )
        for i in range(len(junction_boxes))
        for j in range(i+1, len(junction_boxes))
    ]
    # Sort them by distance
    possible_connections.sort(key=lambda x: x[2])

    # Adjacency list for the graph
    connections = {
        _id: []
        for _id in range(len(junction_boxes))
    }

    # Connect the junction boxes based on the specified algorithm
    for connection_idx, possible_connection in enumerate(possible_connections):
        id_from, id_to, distance = possible_connection

        # Only if there is no connection between those boxes
        if not are_junction_boxes_connected(connections, id_from, id_to):
            connections[id_from].append(id_to)
            connections[id_to].append(id_from)

            # If the new circuit size is equal to all junction boxes,
            # we have the answer
            if len(get_circuit(connections, id_from)) == len(junction_boxes):
                return junction_boxes[id_from].x * junction_boxes[id_to].x



def get_input(filename: str):
    with open(filename, "r") as f:
        _in = [
            JunctionBox(
                idx,
                int(line.split(',')[0]),
                int(line.split(',')[1]),
                int(line.split(',')[2])
            )
            for idx, line in enumerate(f.read().split("\n"))
            if line.split()
        ]
    return _in


def benchmark(name: str, func, *_in) -> None:
    """
    Utility function to benchmark the given part function, printing timing and result.

    Parameters:
        name (str): A label to print alongside the benchmark.
        func (callable): The function to call.
        *_in: Arguments to pass to the function.

    Returns:
        None
    """
    now = datetime.now()
    result = func(*_in)
    _time = datetime.now() - now
    print(f"({_time}) {name}: {result}")

def main() -> None:
    """
    Reads command-line argument for the input file name, processes both parts,
    and prints their results and timings.

    Returns:
        None
    """
    if len(argv) < 2:
        print("Provide the file name")
        return
    _in = get_input(argv[1])
    benchmark("PART 1", part1, _in)
    benchmark("PART 2", part2, _in)

if __name__ == "__main__":
    main()
