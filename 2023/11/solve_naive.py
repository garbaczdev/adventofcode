#!/usr/bin/env python3
from sys import argv
from datetime import datetime


def get_input(filename: str):
    with open(filename, "r") as f:
        _in = [line for line in f.read().split("\n") if line.split()]

    return _in


def get_galaxy_score(_in, i):
    gs = [
        (y, x)
        for y in range(len(_in))
        for x in range(len(_in[0]))
        if _in[y][x] == "#"
    ]

    return sum(
        abs(gs[i][0] - gs[j][0]) + abs(gs[i][1] - gs[j][1])
        for i in range(len(gs))
        for j in range(i+1, len(gs))
    )


def expand(_in):
    expanded_rows = []
    
    for row in _in:
        expanded_rows.append(row)
        if all(el == "." for el in row):
            expanded_rows.append(row)

    expanded_cols = []
    
    for x in range(len(_in[0])):
        col = [row[x] for row in expanded_rows]
        expanded_cols.append(col)
        if all(el == "." for el in col):
            expanded_cols.append(col)
    
    
    return [
        "".join(col[y] for col in expanded_cols) 
        for y in range(len(expanded_cols[0]))
    ]


def part1(_in):
    # print("\n".join(expand(_in)))
    return get_galaxy_score(expand(_in))


def part2(_in):
    for _ in range(1000000):
        _in = expand(_in)
    return get_galaxy_score(_in)


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
