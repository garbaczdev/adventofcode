#!/usr/bin/env python3

# =============================================
#  Maciej Garbacz | garbaczdev@gmail.com
#  Advent of Code solutions
#  https://github.com/garbaczdev/adventofcode
# =============================================

from sys import argv
from datetime import datetime


def part1(_in):
    current_rotation = 50
    number_of_zeros = 0

    for instruction in _in:
        direction, distance = instruction

        if direction == "L":
            distance = -distance

        current_rotation = (current_rotation + distance) % 100

        if current_rotation == 0:
            number_of_zeros += 1

    return number_of_zeros


def part2(_in):
    current_rotation = 50
    number_of_zeros = 0

    for instruction in _in:
        direction, distance = instruction
        direction_multiplier = 1 if direction == "R" else -1


        # Used to keep track of the rotation while simulating the "clicks"
        rotation_in_iteration = current_rotation
        for i in range(1, distance + 1):
            # Iterate over all of the clicks until you find a click on zero
            rotation_in_iteration += direction_multiplier
            rotation_in_iteration %= 100

            if rotation_in_iteration == 0:
                # It clicks atleast once and we also add the number of full rotations
                number_of_zeros += 1 + (distance - i) // 100
                break

        # Actually calculate the current rotation like in part 1
        current_rotation = (current_rotation + distance * direction_multiplier) % 100

    return number_of_zeros


def get_input(filename: str):
    with open(filename, "r") as f:
        _in = [
            (line[0], int(line[1:]))
            for line in f.read().split("\n")
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
