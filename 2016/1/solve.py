#!/usr/bin/env python3
from sys import argv
from datetime import datetime


def get_input(filename: str):
    with open(filename, "r") as f:
        _in = f.read().strip("\n").strip().split(", ")
    return _in


def part1(_in):
    x_dir = 0
    y_dir = 1

    x = 0
    y = 0

    for instruction in _in:
        rotation_direction = instruction[0]
        distance = int(instruction[1:])
        if rotation_direction == "R":
            # Rotate clockwise
            x_dir, y_dir = y_dir, -x_dir
        elif rotation_direction == "L":
            # Rotate counterclockwise
            x_dir, y_dir = -y_dir, x_dir
        
        x += distance * x_dir
        y += distance * y_dir
    
    return abs(x) + abs(y)


def part2(_in):
    x_dir = 0
    y_dir = 1

    x = 0
    y = 0

    visited_locations = set((0, 0))

    for instruction in _in:
        rotation_direction = instruction[0]
        distance = int(instruction[1:])
        if rotation_direction == "R":
            # Rotate clockwise
            x_dir, y_dir = y_dir, -x_dir
        elif rotation_direction == "L":
            # Rotate counterclockwise
            x_dir, y_dir = -y_dir, x_dir
        
        for _ in range(1, distance + 1):
            x += x_dir
            y += y_dir

            if (x, y) in visited_locations:
                return abs(x) + abs(y) 
            visited_locations.add((x, y))
    
    return None


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
