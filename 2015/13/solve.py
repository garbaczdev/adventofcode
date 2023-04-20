#!/usr/bin/env python3
from sys import argv
from datetime import datetime
from itertools import permutations


def count_score(arrangement: list, relations: dict) -> int:
    n = len(arrangement)
    return sum(
        relations[arrangement[i]][arrangement[(i+1)%n]]
        + relations[arrangement[i]][arrangement[(i-1)%n]]
        for i in range(n)
    )


def get_input(filename: str):
    with open(filename, "r") as f:
        _in = [line for line in f.read().split("\n") if line.split()]

    return _in


def part1(_in):

    _in = _in[:]

    _in = [
            line.split()[:1] + line.split()[2:4] + [line.split()[-1][:-1]]
        for line in _in
    ]

    relations = {
        name: dict()
        for name in set(line[0] for line in _in)
    }

    for line in _in:
        sign = 1 if line[1] == "gain" else -1
        relations[line[0]][line[-1]] = int(line[2])*sign

    return max(
        count_score(permutation, relations) 
        for permutation in permutations(relations.keys())
    )


def part2(_in):

    _in = _in[:]

    names = set(line.split()[0] for line in _in)
    for name in names:
        _in.append(f"You would gain 0 happiness units by sitting next to {name}.")
        _in.append(f"{name} would gain 0 happiness units by sitting next to You.")
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
