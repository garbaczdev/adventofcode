#!/usr/bin/env python3
from sys import argv
from datetime import datetime


def count_characters(line: str) -> int:
    i = 0
    l = 0
    while i < len(line):
        if line[i] == "\\":
            next = line[i+1]
            if next == "\\" or next == '"':
                i += 2
            elif next == "x":
                i += 4
        else:
            i += 1
        l += 1
    return l


def encode_str(_str: str) -> str:

    _str = _str.replace("\\", "\\\\")
    _str = _str.replace('"', '\\"')
    return f'"{_str}"'


def get_input(filename: str):
    with open(filename, "r") as f:
        _in = [line for line in f.read().split("\n") if line.split()]

    return _in


def part1(_in):
    return sum(len(line) - count_characters(line[1:-1]) for line in _in) 

def part2(_in):
    _in = [encode_str(line) for line in _in] 
    return part1(_in)

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
