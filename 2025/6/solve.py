#!/usr/bin/env python3

# =============================================
#  Maciej Garbacz | garbaczdev@gmail.com
#  Advent of Code solutions
#  https://github.com/garbaczdev/adventofcode
# =============================================

from sys import argv
from datetime import datetime
from functools import reduce


def part1(_in):
    grand_total = 0

    for problem in _in:
        symbol = problem[-1].strip()
        numbers = [int(num.strip()) for num in problem[:-1]]

        if symbol == "+":
            grand_total += sum(numbers)
        elif symbol == "*":
            grand_total += reduce(lambda x, y: x * y, numbers)
        else:
            raise ValueError(f"Unsupported symbol {symbol}")

    return grand_total


def part2(_in):
    grand_total = 0

    for problem in _in:
        symbol = problem[-1].strip()
        numbers_unparsed = problem[:-1]

        # Recreate the vertical numbers
        numbers = []
        max_number_len = max(len(num) for num in numbers_unparsed)
        for i in range(max_number_len):
            number = ""
            for number_unparsed in numbers_unparsed:
                if i >= len(number_unparsed) or number_unparsed[i] == " ":
                    continue
                number += number_unparsed[i]
            numbers.append(int(number))

        if symbol == "+":
            grand_total += sum(numbers)
        elif symbol == "*":
            grand_total += reduce(lambda x, y: x * y, numbers)
        else:
            raise ValueError(f"Unsupported symbol {symbol}")

    return grand_total


def get_input(filename: str):
    with open(filename, "r") as f:
        lines = [
            line
            for line in f.read().split("\n")
            if line.split()
        ]

        # Find the column indices based on all characters
        # in a column being a space
        column_indices = [
            column_idx
            for column_idx in range(len(lines[0]))
            if all(
                lines[row_idx][column_idx] == " "
                for row_idx in range(len(lines))
            )
        ]
        # Add start and end as the indices aswell to account for first/last column
        column_indices = [-1] + column_indices + [max(len(line) for line in lines)]

        # Extract the numbers from lines based on the column indices
        _input = [
            [
                line[column1+1:column2]
                for column1, column2 in zip(column_indices, column_indices[1:])
            ]
            for line in lines
        ]

        _input_height = len(_input)
        _input_width = len(_input[0])

        # Rotate the input from vertical to horizontal
        _in = [
            [_input[y][x] for y in range(_input_height)]
            for x in range(_input_width)
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
