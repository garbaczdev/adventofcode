#!/usr/bin/env python3
from sys import argv
from datetime import datetime

from functools import reduce
from operator import mul


def get_input(filename: str):
    with open(filename, "r") as f:
        _in = [list(map(int, line.split(":")[1].split())) for line in f.read().split("\n") if line.split()]

    return _in


def part1(_in):
    return reduce(mul, [
        len([
            (time-i)*i
            for i in range(time+1)
            if (time-i)*i > dist
        ])
        for time, dist in zip(_in[0], _in[1])
    ])


def part2(_in):
    return part1([[int("".join(map(str, attr)))] for attr in _in])


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
