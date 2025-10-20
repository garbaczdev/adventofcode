#!/usr/bin/env python3

# =============================================
#  Maciej Garbacz | garbaczdev@gmail.com
#  Advent of Code solutions
#  https://github.com/garbaczdev/adventofcode
# =============================================

# --------------------------------------------------------------------------------------
# Advent of Code 2016 Day 1: No Time for a Taxicab
#
# This script reads a list of instructions describing moves on a 2D grid,
# starting from the origin facing north. Each instruction consists of a turn
# (either 'L' for left or 'R' for right) followed by a distance to travel.
# 
# Part 1: Determines the total distance (Manhattan distance) from the starting point
# after all instructions are performed.
#
# Part 2: Finds the first location that is visited twice along the path and reports
# its Manhattan distance from the origin.
#
# Usage: python solve.py <input-file>
#
# Assumptions:
#   - Input file contains a single line, a comma-separated list of instructions.
#   - No validation is performed on input correctness.
# --------------------------------------------------------------------------------------

from sys import argv
from datetime import datetime

def get_input(filename: str):
    with open(filename, "r") as f:
        _in = f.read().strip("\n").strip().split(", ")
    return _in

def part1(_in):
    """
    Processes the list of turn/move instructions and computes the Manhattan distance
    from the starting position to the final position after moving.

    Parameters:
        _in (list[str]): List of instruction strings (e.g., "R2", "L3")

    Returns:
        int: Manhattan distance from the origin after all moves.
    """
    # Initial direction vector: facing north (0,1)
    x_dir = 0
    y_dir = 1

    # Initial coordinates
    x = 0
    y = 0

    for instruction in _in:
        rotation_direction = instruction[0]  # First character denotes turn direction
        distance = int(instruction[1:])      # Remaining characters denote number of steps
        if rotation_direction == "R":
            # Rotate direction clockwise by 90 degrees:
            # For (x_dir, y_dir), after right turn: (y_dir, -x_dir)
            x_dir, y_dir = y_dir, -x_dir
        elif rotation_direction == "L":
            # Rotate direction counterclockwise by 90 degrees:
            # For (x_dir, y_dir), after left turn: (-y_dir, x_dir)
            x_dir, y_dir = -y_dir, x_dir
        
        # Move in the new direction by the given distance
        x += distance * x_dir
        y += distance * y_dir
    
    return abs(x) + abs(y)  # Manhattan distance from origin

def part2(_in):
    """
    Processes the instruction list and finds the first position visited twice while walking.
    Returns the Manhattan distance to that location from the origin.

    Parameters:
        _in (list[str]): List of instruction strings

    Returns:
        int or None: Manhattan distance to the first revisited location, or None if none found.
    """
    # Initial direction: facing north
    x_dir = 0
    y_dir = 1

    # Starting position
    x = 0
    y = 0

    # Set for visited locations, initialized with the origin
    visited_locations = set((0, 0))

    for instruction in _in:
        rotation_direction = instruction[0]
        distance = int(instruction[1:])
        if rotation_direction == "R":
            # Rotate direction clockwise by 90 degrees
            x_dir, y_dir = y_dir, -x_dir
        elif rotation_direction == "L":
            # Rotate direction counterclockwise by 90 degrees
            x_dir, y_dir = -y_dir, x_dir
        
        # Walk step by step to detect revisited locations
        # Must check each individual position between moves
        for _ in range(1, distance + 1):
            x += x_dir
            y += y_dir

            # If this position was already visited, return its distance
            if (x, y) in visited_locations:
                return abs(x) + abs(y) 
            visited_locations.add((x, y))
    
    # No location visited twice
    return None

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

