#!/usr/bin/env python3
from sys import argv
from datetime import datetime


def get_input(filename: str):
    with open(filename, "r") as f:
        _in = f.read().replace("\n", "").strip()

    return _in


def iteration(_str: str) -> str:

    new_str = ""

    count = 0
    digit = ""

    for chr in _str:
        if chr == digit:
            count += 1
        else:
            if count != 0:
                new_str += str(count) + digit
            digit = chr
            count = 1
    
    new_str += str(count) + digit

    return new_str


def part1(_in):
    _str = _in
    for _ in range(40):
        _str = iteration(_str)
    return len(_str)

def part2(_in):
    _str = _in
    for _ in range(50):
        _str = iteration(_str)
    return len(_str)


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
