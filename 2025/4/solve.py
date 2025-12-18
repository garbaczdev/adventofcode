#!/usr/bin/env python3

# =============================================
#  Maciej Garbacz | garbaczdev@gmail.com
#  Advent of Code solutions
#  https://github.com/garbaczdev/adventofcode
# =============================================

from sys import argv
from datetime import datetime

import numpy as np


# Get all of the neighbouring directions
DIRECTIONS = [
    (x, y)
    for x in range(-1, 2)
    for y in range(-1, 2)
    if abs(x) + abs(y) != 0
]


def get_element(arr: np.array, x: int, y: int):
    """
    Safely gets the element at coordinates (x, y) from the given 2D numpy array.
    If (x, y) is out of array bounds, returns '.' as a placeholder.
    
    Parameters:
        arr (np.array): The 2D numpy array representing the grid.
        x (int): The column index.
        y (int): The row index.
    
    Returns:
        The element at (y, x) if within bounds, else '.'.
    """
    height, width = arr.shape
    if 0 <= y < height and  0 <= x < width:
        return arr[y][x]
    return '.'


def part1(_in):
    """
    Counts the number of "pickupable" paper rolls ('@') in the grid.
    A paper roll is "pickupable" if it has fewer than 4 neighboring paper rolls
    (neighbors checked in the directions defined by DIRECTIONS).
    The input grid is not modified.

    Parameters:
        _in (np.array): The 2D numpy array representing the current state of the grid.
    
    Returns:
        int: The number of pickupable paper rolls.
    """
    height, width = _in.shape

    pickupable_paper_rolls = 0

    # Iterate over all cells in the grid.
    for y in range(height):
        for x in range(width):

            element = _in[y][x]
            # Proceed only if the current element is a paper roll ('@')
            if element != "@":
                continue

            neighbouring_paper_rolls = 0

            # Check all neighboring positions in the specified DIRECTIONS.
            for x_d, y_d in DIRECTIONS:
                x_n = x + x_d
                y_n = y + y_d
                if get_element(_in, x_n, y_n) == "@":
                    neighbouring_paper_rolls += 1

            # If fewer than 4 '@' neighbors, the roll is pickupable
            if neighbouring_paper_rolls < 4:
                pickupable_paper_rolls += 1

    return pickupable_paper_rolls


def part2(_in):
    """
    Counts the total number of paper rolls ('@') that can be picked up over multiple rounds.
    In each round, all currently "pickupable" rolls (less than 4 neighbors) are picked up (set to '.').
    The process repeats until no more rolls can be picked up.
    The input grid is modified in-place.

    Parameters:
        _in (np.array): The 2D numpy array representing the grid's current state.
    
    Returns:
        int: The total number of paper rolls picked up across all rounds.
    """
    height, width = _in.shape

    total_pickupable_paper_rolls = 0

    while True:
        pickupable_paper_rolls = 0

        # Iterate through all cells each round to select pickupable paper rolls.
        for y in range(height):
            for x in range(width):

                element = _in[y][x]
                # Consider only paper roll ('@') positions.
                if element != '@':
                    continue

                neighbouring_paper_rolls = 0

                # Count number of adjacent '@'s using DIRECTIONS.
                for x_d, y_d in DIRECTIONS:
                    x_n = x + x_d
                    y_n = y + y_d
                    if get_element(_in, x_n, y_n) == '@':
                        neighbouring_paper_rolls += 1

                # If fewer than 4 '@' neighbors, mark for pickup.
                if neighbouring_paper_rolls < 4:
                    pickupable_paper_rolls += 1
                    # Immediately set this cell to '.' to remove the paper roll.
                    _in[y][x] = '.'

        # No pickupable paper rolls left; end process.
        if pickupable_paper_rolls == 0:
            break
        total_pickupable_paper_rolls += pickupable_paper_rolls

    return total_pickupable_paper_rolls


def get_input(filename: str):
    with open(filename, "r") as f:
        _in = np.array([
            list(line)
            for line in f.read().split("\n")
            if line.split()
        ])
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
