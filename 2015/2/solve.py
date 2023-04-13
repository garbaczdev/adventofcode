#!/usr/bin/env python3
from sys import argv
from datetime import datetime


def get_input(filename: str):
    with open(filename, "r") as f:
        _in = [[int(dim) for dim in line.split("x")] for line in f.read().split("\n") if line.split()]

    return _in


def part1(_in):
    return sum(
        2*l*w + 2*w*h + 2*h*l 
        + min([l*w, w*h, h*l])
        for (w, h, l)
        in _in
    )


def part2(_in):
    return sum(
        w*h*l
        + sorted([w, h, l])[0]*2
        + sorted([w, h, l])[1]*2
        for (w, h, l)
        in _in
    )


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
