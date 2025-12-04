#!/usr/bin/env python3

# =============================================
#  Maciej Garbacz | garbaczdev@gmail.com
#  Advent of Code solutions
#  https://github.com/garbaczdev/adventofcode
# =============================================

import math

from sys import argv
from datetime import datetime


def is_valid_id_part1(_id: int) -> bool:
    str_id = str(_id)
    id_len = len(str_id)

    # The ids with an even number of digits are always valid
    if id_len % 2 == 1:
        return True

    middle_idx = id_len // 2
    if str_id[:middle_idx] == str_id[middle_idx:]:
        # If the left part of id is the same as the right part, it is invalid
        return False

    return True


def find_divisors_generator(n: int):
    for i in range(1, int(math.sqrt(n)) + 1):  # Loop up to √n
        if n % i == 0:
            yield i
            if i != n // i:
                yield n // i      # Yield the paired divisor


def is_valid_id_part2(_id: int) -> bool:
    str_id = str(_id)
    id_len = len(str_id)

    for divisor in find_divisors_generator(id_len):

        count_per_sequence = dict()
        for part_idx in range(0, id_len, divisor):
            sequence = str_id[part_idx:part_idx + divisor]

            if count_per_sequence.get(sequence) is None:
                count_per_sequence[sequence] = 1
            else:
                count_per_sequence[sequence] += 1

        if len(count_per_sequence) == 1 and list(count_per_sequence.values())[0] >= 2:
            return False

    return True

def part1(_in):
    invalid_id_sum = 0
    for id_range in _in:
        start_id, end_id = id_range
        # Iterate over ids in the range
        for _id in range(start_id, end_id + 1):
            # If its ivnalid, add it to the sum
            if not is_valid_id_part1(_id):
                invalid_id_sum += _id
    return invalid_id_sum


def part2(_in):
    invalid_id_sum = 0
    for id_range in _in:
        start_id, end_id = id_range
        # Iterate over ids in the range
        for _id in range(start_id, end_id + 1):
            # If its ivnalid, add it to the sum
            if not is_valid_id_part2(_id):
                invalid_id_sum += _id
    return invalid_id_sum


def get_input(filename: str):
    with open(filename, "r") as f:
        _in = [
            (
                int(range_str.split("-")[0]),
                int(range_str.split("-")[1])
            )
            for range_str in f.read().strip("\n").split(",")
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
