#!/usr/bin/env python3
from sys import argv


def get_input(filename: str) -> list:
    with open(filename, "r") as f:
        _in = [line for line in f.read().split("\n") if line.split()]

    return _in


def part1(_in: list) -> None:
    pass


def part2(_in: list) -> None:
    pass


def main() -> None:
    if len(argv) < 2:
        print("Provide the file name")
        return
    _in = get_input(argv[1])
    part1(_in)
    part2(_in)


if __name__ == "__main__":
    main()
