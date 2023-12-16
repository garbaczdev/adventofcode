#!/usr/bin/env python3
from sys import argv
from datetime import datetime

import numpy as np


def get_input(filename: str):
    with open(filename, "r") as f:
        _in = [
            np.array([
                list(line) 
                for line in segment.split("\n") 
                if line.split()
            ])
            for segment in f.read().split("\n\n")
        ]

    return _in


def is_vertical_reflection(_in: np.array, l_col_i: int, r_col_i: int, acceptance: int = 0) -> bool:

    width = len(_in[0])
    height = len(_in)

    reflection_width = min(width - r_col_i, l_col_i+1)
    
    smudges = 0

    for y in range(height):
        for i in range(reflection_width):
            if _in[y][l_col_i - i] != _in[y][r_col_i + i]:
                smudges += 1

    return smudges == acceptance


def get_vertical_reflections(_in: np.array, acceptance: int = 0) -> list[tuple[int]]:

    width = len(_in[0])
    
    return [
        (l_col_i, r_col_i) 
        for l_col_i, r_col_i in zip(
            range(width-1), range(1, width)
        ) if is_vertical_reflection(_in, l_col_i, r_col_i, acceptance)
    ]


def is_horizontal_reflection(_in: np.array, u_row_i: int, d_row_i: int, acceptance: int = 0) -> bool:

    width = len(_in[0])
    height = len(_in)

    reflection_height = min(height - d_row_i, u_row_i+1)

    smudges = 0

    for x in range(width):
        for i in range(reflection_height):
            if _in[u_row_i - i][x] != _in[d_row_i + i][x]:
                smudges += 1

    return smudges == acceptance


def get_horizontal_reflections(_in: np.array, acceptance: int = 0) -> list[tuple[int]]:

    height = len(_in)
    
    return [
        (u_row_i, d_row_i) 
        for u_row_i, d_row_i in zip(
            range(height-1), range(1, height)
        ) if is_horizontal_reflection(_in, u_row_i, d_row_i, acceptance)
    ]


def part1(segments):
    return sum(
        sum(
            left + 1
            for left, right in get_vertical_reflections(_in)
        ) + sum(
            100*(up+1)
            for up, down in get_horizontal_reflections(_in)
        )
        for _in in segments
    )


def part2(segments):
    return sum(
        sum(
            left + 1
            for left, right in get_vertical_reflections(_in, 1)
        ) + sum(
            100*(up+1)
            for up, down in get_horizontal_reflections(_in, 1)
        )
        for _in in segments
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
