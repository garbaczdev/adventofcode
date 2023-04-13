#!/usr/bin/env python3
from sys import argv
from datetime import datetime


def get_input(filename: str):
    with open(filename, "r") as f:
        _in = f.read().replace("\n", "").strip()
    return _in


def part1(_in):
    return _in.count("(") - _in.count(")")


def part2(_in):
    floor = 0
    for index, char in enumerate(_in):
        floor += 1 if char == "(" else -1
        if floor == -1:
            return index + 1

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
