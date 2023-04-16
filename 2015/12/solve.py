#!/usr/bin/env python3
from sys import argv
from datetime import datetime

from json import loads

ALLOWED_CHARS = "-"


def json_line_sum_recursive(line_json) -> int:

    if isinstance(line_json, list):
        return sum(json_line_sum_recursive(el) for el in line_json)
    elif isinstance(line_json, dict):
        if "red" in line_json.values():
            return 0
        return sum(
            json_line_sum_recursive(line_json[key]) 
            for key in line_json
        )
    elif isinstance(line_json, int):
        return line_json
    else:
        return 0

def is_int(n: int) -> bool:
    try:
        int(n)
        return True
    except ValueError:
        return False


def json_line_sum(line: str) -> int:
    wrong_chars = [
        char 
        for char in set(line) 
        if not is_int(char) and char not in ALLOWED_CHARS 
    ]

    for char in wrong_chars:
        line = line.replace(char, " ")

    return sum(int(num) for num in line.split())


def get_input(filename: str):
    with open(filename, "r") as f:
        _in = [line for line in f.read().split("\n") if line.split()]

    return _in


def part1(_in):
    return sum(json_line_sum(line) for line in _in)


def part2(_in):
    return sum(json_line_sum_recursive(loads(line)) for line in _in)


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
