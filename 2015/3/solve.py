#!/usr/bin/env python3
from sys import argv
from datetime import datetime


def get_input(filename: str):
    with open(filename, "r") as f:
        _in = f.read().replace("\n", "").strip()
    return _in


def part1(_in):
    houses = list()
    x = 0
    y = 0
    houses.append((x, y))
    for chr in _in:
        x += 1 if chr == ">" else -1 if chr == "<" else 0
        y += 1 if chr == "^" else -1 if chr == "v" else 0
        houses.append((x, y))
    return len(set(houses))


def part2(_in):
    houses = list()
    x = [0,0]
    y = [0,0]
    houses.append((x[0], y[0]))
    houses.append((x[1], y[1]))
    for index, chr in enumerate(_in):
        turn = index % 2
        x[turn] += 1 if chr == ">" else -1 if chr == "<" else 0
        y[turn] += 1 if chr == "^" else -1 if chr == "v" else 0
        houses.append((x[turn], y[turn]))
    return len(set(houses))


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
