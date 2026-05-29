#!/usr/bin/env python3

# =============================================
#  Maciej Garbacz | garbaczdev@gmail.com
#  Advent of Code solutions
#  https://github.com/garbaczdev/adventofcode
# =============================================

from sys import argv
from datetime import datetime
from hashlib import md5


LEGAL_POSITIONS = set(str(i) for i in range(0, 8))


def part1(_in):
    door_id = _in[0]
    password = []
    idx = 0
    while len(password) < 8:
        _hash = md5((door_id + str(idx)).encode()).hexdigest()
        if all(char == '0' for char in _hash[:5]):
            password.append(_hash[5])
        idx += 1
    return "".join(password)


def part2(_in):
    door_id = _in[0]

    password = [None for _ in range(8)]
    password_positions_filled = 0

    idx = 0
    while password_positions_filled < 8:
        _hash = md5((door_id + str(idx)).encode()).hexdigest()
        if all(char == '0' for char in _hash[:5]) and _hash[5] in LEGAL_POSITIONS:
            position = int(_hash[5])
            if password[position] is None:
                # Fill in the password field
                password[position] = _hash[6]
                password_positions_filled += 1
        idx += 1
    return "".join(password)


def get_input(filename: str):
    with open(filename, "r") as f:
        _in = [
            line
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
