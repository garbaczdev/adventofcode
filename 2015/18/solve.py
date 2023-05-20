#!/usr/bin/env python3
from sys import argv
from datetime import datetime

import numpy as np



WIDTH = 100
HEIGHT = 100


# --- MACIEJ GARBACZ 2D COORDINATE LIBRARY ---
ADJACENT_VECTORS = [
    (x, y) 
    for x in range(-1, 2) 
    for y in range(-1, 2) 
    if x != 0 or y != 0
]

def is_in_bounds(width: int, height: int, x: int, y: int) -> bool:
    return x >= 0 and x < width and y >= 0 and y < height

def get_adjacent_cords(width: int, height: int, x: int, y: int) -> list[tuple[int, int]]:
    return [
        (x + x_diff, y + y_diff)
        for x_diff, y_diff in ADJACENT_VECTORS
        if is_in_bounds(width, height, x + x_diff, y + y_diff)
    ]
# -/- MACIEJ GARBACZ 2D COORDINATE LIBRARY -/-


def get_input(filename: str):
    with open(filename, "r") as f:
        _in = np.array([
            [0 if char == "." else 1 for char in line] 
            for line in f.read().split("\n") 
            if line.split()
        ])
        # For 1 line inputs
        # _in = f.read().replace("\n", "").strip()

    return _in


def part1(_in, steps=100):
    _in = np.copy(_in)

    for step in range(steps):

        new = np.copy(_in)
        for x in range(WIDTH):
            for y in range(HEIGHT):
                adj_values = [
                    _in[y_adj][x_adj]
                    for x_adj, y_adj in get_adjacent_cords(WIDTH, HEIGHT, x, y)
                ]

                on_count = adj_values.count(1)
                
                if _in[y][x]:
                    if on_count != 2 and on_count != 3:
                        new[y][x] = 0
                else:
                    if on_count == 3:
                        new[y][x] = 1
        _in = new
    
    return sum(_in.sum(axis=1))

def part2(_in, steps=100):
    _in = np.copy(_in)

    for step in range(steps):
        _in[0][0] = 1
        _in[0][WIDTH-1] = 1
        _in[HEIGHT-1][0] = 1
        _in[HEIGHT-1][WIDTH-1] = 1

        new = np.copy(_in)
        for x in range(WIDTH):
            for y in range(HEIGHT):
                adj_values = [
                    _in[y_adj][x_adj]
                    for x_adj, y_adj in get_adjacent_cords(WIDTH, HEIGHT, x, y)
                ]

                on_count = adj_values.count(1)
                
                if _in[y][x]:
                    if on_count != 2 and on_count != 3:
                        new[y][x] = 0
                else:
                    if on_count == 3:
                        new[y][x] = 1

        _in = new

    _in[0][0] = 1
    _in[0][WIDTH-1] = 1
    _in[HEIGHT-1][0] = 1
    _in[HEIGHT-1][WIDTH-1] = 1

    return sum(_in.sum(axis=1))


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
