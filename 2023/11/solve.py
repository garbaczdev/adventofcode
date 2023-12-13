#!/usr/bin/env python3
from sys import argv
from datetime import datetime


def get_input(filename: str):
    with open(filename, "r") as f:
        _in = [line for line in f.read().split("\n") if line.split()]

    return _in


def get_number_of_elements_between(el: list[int], x1:int, x2: int):
    if x1 == x2:
        return 0
    elif x1 > x2:
        x1, x2 = x2, x1

    for min_x_i, x in enumerate(el):
        if x > x1:
            break
    else:
        min_x_i += 1
    
    for max_x_i in range(len(el) - 1, -1, -1):
        if el[max_x_i] < x2:
            break
    else:
        max_x_i -= 1
    max_x_i += 1
    
    # print(x1, x2, min_x_i, max_x_i, el)

    return max_x_i - min_x_i


def get_galaxy_score(_in, mul):
    empty_rows = [
        y
        for y, row in enumerate(_in)
        if all(el == "." for el in row)
    ]
    
    empty_cols = [
        x
        for x in range(len(_in[0]))
        if all(el == "." for el in [
            row[x] for row in _in
        ])
    ]
    # print(empty_rows, empty_cols)

    gs = [
        (y, x)
        for y in range(len(_in))
        for x in range(len(_in[0]))
        if _in[y][x] == "#"
    ]

    return sum(
        abs(gs[i][0] - gs[j][0]) 
        + abs(gs[i][1] - gs[j][1])
        + get_number_of_elements_between(empty_rows, gs[i][0], gs[j][0])*mul
        + get_number_of_elements_between(empty_cols, gs[i][1], gs[j][1])*mul
        for i in range(len(gs))
        for j in range(i+1, len(gs))
    )



def part1(_in):
    return get_galaxy_score(_in, 1)


def part2(_in):
    return get_galaxy_score(_in, 1000000 - 1)
    # for _ in range(1000000):
    #     _in = expand(_in)
    # return get_galaxy_score(_in)


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
