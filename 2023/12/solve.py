#!/usr/bin/env python3
from sys import argv
from datetime import datetime

from functools import lru_cache, reduce


def get_input(filename: str):
    with open(filename, "r") as f:
        _in = [
            (
                line.split()[0], 
                tuple(map(int, line.split()[1].split(",")))
            )
            for line in f.read().split("\n") 
            if line.split()
        ]

    return _in


@lru_cache
def get_possible_line_after_use(
    line: str,
    current_required: int
) -> str:
   
    if current_required > len(line):
        return "X"

    if any(
        line[required_idx] == "."
        for required_idx in range(current_required)
    ):
        return "X"

    if current_required < len(line) and line[current_required] == "#":
        return "X"

    return line[current_required+1:]


# Dynamic Programming Backtracking Solution
@lru_cache
def count_possibilities(
    line: str,
    required: tuple[int]
) -> int:

    if line.count("#") + line.count("?") < sum(required):
        return 0

    if not required and line.count("#") > 0:
        return 0

    if not required:
        return 1

    current_required = required[0]

    possibilities = 0

    for line_idx in range(len(line)):
        possible_line = get_possible_line_after_use(
            line[line_idx:],
            current_required
        )
        if possible_line != "X":
            possibilities += count_possibilities(
                possible_line,
                required[1:]
            )
        if line[line_idx] == "#":
            break

    return possibilities

# Brute force 2^n solution
def count_possibilities_dumb(
    line: str,
    required: tuple[int]
) -> int:

    n = len(line)
    possibilities = 0
    current_line = ""

    def rec(i):
        nonlocal possibilities, current_line
        
        if i == n:
            if tuple(
                len(seg) 
                for seg in current_line.split(".") if seg
            ) == required:
                possibilities += 1
        else:
            if line[i] == "?":
                current_line += "#"
                rec(i+1)
                current_line = current_line[:i]

                current_line += "."
                rec(i+1)
                current_line = current_line[:i]
            else:
                current_line += line[i]
                rec(i+1)
                current_line = current_line[:i]

          
    rec(0)
    
    return possibilities


def part1(_in):
    return sum(
        count_possibilities(line, required)
        for line, required in _in
    )


def part2(_in):

    _in = [
        (
            "?".join(line for _ in range(5)),
            tuple(reduce(lambda a,b: a+b, [
                required for _ in range(5)
            ]))
        )
        for line, required in _in
    ]

    return sum(
        count_possibilities(line, required)
        for line, required in _in
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
