#!/usr/bin/env python3

# =============================================
#  Maciej Garbacz | garbaczdev@gmail.com
#  Advent of Code solutions
#  https://github.com/garbaczdev/adventofcode
# =============================================

# -----------------------------------------------------------
# This script solves Advent of Code 2016 Day 3.
#
# The task involves determining the valid triangles in a list,
# given the lengths of their sides. "Valid" triangles are those
# whose two smallest sides sum to more than the largest side.
# 
# Part 1 checks triangles as given line by line.
# Part 2 constructs triangles vertically from groups of three
# consecutive rows, as per AoC 2016 Day 3's second part.
#
# Input is expected as a text file with three side lengths
# (integers) per line, space or tab separated.
#
# Usage:
#    python3 solve.py input.txt
#
# -----------------------------------------------------------

from sys import argv
from datetime import datetime

def part1(_in):
    """
    Counts valid triangles from the input list.
    For each triangle, sorts the sides and checks if
    the sum of the two smallest sides is greater than the largest.

    Parameters:
        _in (list[list[int]]): List of triangle sides.

    Returns:
        int: Number of valid triangles.
    """
    # Sort each triangle's sides to simplify validity logic
    _in = [sorted(line) for line in _in]
    return sum(
        1 if tr[0] + tr[1] > tr[2] else 0
        for tr in _in
    )


def part2(_in):
    """
    Counts valid triangles when reading columns of groups of three lines
    as triangles (per problem's part 2).
    Constructs new triangles by taking the first element from each of 
    three consecutive lines, then the second elements, etc.

    Transposes groups of three rows to convert columns to triangles.

    Parameters:
        _in (list[list[int]]): List of triangle sides.

    Returns:
        int: Number of valid triangles built from columns.
    """
    # _in is assumed to have length that is a multiple of 3
    _in = [
        [_in[i][j], _in[i+1][j], _in[i+2][j]]
        for i in range(0, len(_in), 3)
        for j in range(3)
    ]
    # Now process the new triangles as in part1
    return part1(_in)

def get_input(filename: str):
    """
    Reads input file and parses it into a list of triangles (lists of ints).

    Parameters:
        filename (str): Input file path.

    Returns:
        list[list[int]]: Parsed triangle side lengths.
    """
    with open(filename, "r") as f:
        # Split lines, filter out empty ones, and parse integers
        _in = [
            [int(num.strip()) for num in line.split()]
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
    Main entry point of the script. Reads input file from command line,
    parses input, and runs benchmarks for both parts.

    Returns:
        None

    Assumptions:
        - There must be a valid input filename provided as the first argument.
        - The input file must contain groups of three numbers per line and,
          for part2, the number of rows should be a multiple of 3.
    """
    if len(argv) < 2:
        print("Provide the file name")
        return
    _in = get_input(argv[1])
    benchmark("PART 1", part1, _in)
    benchmark("PART 2", part2, _in)

if __name__ == "__main__":
    main()

