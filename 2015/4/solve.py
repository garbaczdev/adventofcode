#!/usr/bin/env python3
from sys import argv
from datetime import datetime

from hashlib import md5


def get_input(filename: str):
    with open(filename, "r") as f:
        _in = f.read().replace("\n", "").strip()

    return _in


def part1(_in):
    i = 0
    while md5((_in + str(i)).encode()).hexdigest()[:5] != "00000":
        i += 1
    return i


def part2(_in):
    i = 0
    while md5((_in + str(i)).encode()).hexdigest()[:6] != "000000":
        i += 1
    return i


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
