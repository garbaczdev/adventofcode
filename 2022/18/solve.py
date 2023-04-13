#!/usr/bin/env python3
import sys
from sys import argv
from datetime import datetime

sys.setrecursionlimit(100000)


ADJACENT_CUBES_DIRECTIONS = [(-1, 0, 0), (0, -1, 0), (0, 0, -1), (0, 0, 1), (0, 1, 0), (1, 0, 0)]

def get_input(filename: str) -> list:
    with open(filename, "r") as f:
        _in = [tuple(int(cord) for cord in line.split(",")) for line in f.read().split("\n") if line.split()]

    return _in


def get_sides(points: set) -> int:

    checked_points = set()
    sides = []

    def discover_dfs(current_point: tuple):
        nonlocal sides
        checked_points.add(current_point)
        
        for direction in ADJACENT_CUBES_DIRECTIONS:
            new_cell = tuple(a + b for a, b in zip(current_point, direction))
            if new_cell in points:
                if new_cell not in checked_points:
                    discover_dfs(new_cell)
            else:
                sides.append((current_point, direction))
        
    for point in points:
        if point not in checked_points:
            discover_dfs(point)

    return sides


def is_facing(side: tuple[tuple, tuple], other_side: tuple[tuple, tuple]) -> bool:

    
    diff_vector = tuple(dir2 - dir1 for dir1, dir2 in zip(side[0], other_side[0]))

    if diff_vector.count(0) != 2:
        return False

    directions_vector = tuple(dir1 + dir2 for dir1, dir2 in zip(side[1], other_side[1]))
    if any(vec != 0 for vec in directions_vector):
        return False

    diff = [d for d in diff_vector if d != 0][0]
    direction = [d for d in side[1] if d != 0][0]

    
    if diff_vector.index(diff) != side[1].index(direction):
        return False


    return diff * direction > 0


def get_adjacent_directions(side: tuple) -> tuple:
    return [
            direction 
            for direction in ADJACENT_CUBES_DIRECTIONS
            if all(
                side_dir == 0 or (side_dir != 0 and _dir == 0)
                for side_dir, _dir 
                in zip(side[1], direction)
            )
    ]


def get_sides_groups(sides: list) -> list:

    checked_sides = set()
    current_group = []

    def group_sides(current_side: tuple):

        if current_side not in sides or current_side in checked_sides:
            return

        checked_sides.add(current_side)
        current_group.append(current_side)

        next_cell = tuple(a + b for a, b in zip(current_side[0], current_side[1]))
        
        for direction in get_adjacent_directions(current_side):

            next_side = (
                    tuple(a + b for a, b in zip(next_cell, direction)), 
                    tuple(_dir * -1 for _dir in direction)
            )
            group_sides(next_side)
            if next_side not in sides:
                adj_cell = tuple(a + b for a, b in zip(current_side[0], direction))
                group_sides((adj_cell, current_side[1]))
                group_sides((current_side[0], direction))
            

        
    groups = []

    for side in sides:
        if side not in checked_sides:
            group_sides(side)
            groups.append(current_group)
            current_group = []

    return groups


def part1(_in: list) -> None:
    points = set(_in)
    sides = get_sides(points)
    return len(sides)
    

def part2(_in: list) -> None:
    points = set(_in)
    sides = get_sides(points)

    sides_groups = get_sides_groups(sides)

    return max([len(group) for group in sides_groups])


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
