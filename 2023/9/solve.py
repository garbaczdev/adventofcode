#!/usr/bin/env python3
from sys import argv
from datetime import datetime

from functools import reduce


def get_input(filename: str):
    with open(filename, "r") as f:
        _in = [tuple(map(int, line.split())) for line in f.read().split("\n") if line.split()]

    return _in



def extrapolate(sequence: tuple[int]) -> int:
    sequences = [sequence]
    while any(value != 0 for value in sequences[-1]):
        sequences.append([n - c for c, n in zip(sequences[-1], sequences[-1][1:])])
    return reduce(lambda c, n: c + n[-1], sequences[::-1], 0)


def part1(_in):
    return sum(extrapolate(sequence) for sequence in _in)


def extrapolate_backwards(sequence: tuple[int]) -> int:
    sequences = [sequence]
    while any(value != 0 for value in sequences[-1]):
        sequences.append([n - c for c, n in zip(sequences[-1], sequences[-1][1:])])
    return reduce(lambda c, n: n[0] - c, sequences[::-1], 0)


def part2(_in):
    return sum(extrapolate_backwards(sequence) for sequence in _in)


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
