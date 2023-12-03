#!/usr/bin/env python3
from sys import argv
from datetime import datetime

from itertools import chain


ADJACENT_VECTORS = [
    (x, y)
    for x in range(-1, 2)
    for y in range(-1, 2)
    if (x, y) != (0, 0)
]


def get_adjacent_cords(_in: list[str], x: int, y: int) -> list[tuple[int, int]]:
    height = len(_in)
    width = len(_in[0])

    adjacent_cords = []

    for x_d, y_d in ADJACENT_VECTORS:

        x_n = x + x_d
        y_n = y + y_d
        
        if all([
            x_n >= 0,
            x_n < width,
            y_n >= 0,
            y_n < height
        ]):
            adjacent_cords.append((x_n, y_n))

    return adjacent_cords


def is_int(num: str) -> bool:
    try:
        int(num)
        return True
    except:
        return False


def get_number_groups(row: str) -> list[list[int]]:
    number_indices = [index for index in range(len(row)) if is_int(row[index])]
    groups = []
    current_group = []
    for number_index in number_indices:
        if not current_group or current_group[-1] == number_index - 1:
            current_group.append(number_index)
        else:
            groups.append(current_group)
            current_group = [number_index]
    if current_group:
        groups.append(current_group)
    return groups


def get_input(filename: str):
    with open(filename, "r") as f:
        _in = [line for line in f.read().split("\n") if line.split()]

    return _in


def part1(_in):
    score = 0
    for y_row, row in enumerate(_in):
        for group in get_number_groups(row):
            group_cords = [(x, y_row) for x in group]
            adjacent_cords = set(
                item 
                for group_adj in [get_adjacent_cords(_in, x, y_row) for x in group]
                for item in group_adj
                if item not in group_cords
            )
            adjacent_chars = set(_in[y][x] for x, y in adjacent_cords)
            symbols = [char for char in adjacent_chars if char != "." and not is_int(char)]
            if symbols:
                number = int("".join(row[x] for x in group))
                score += number

    return score


def part2(_in):
    gears = dict()

    for y_row, row in enumerate(_in):
        for group in get_number_groups(row):

            number = int("".join(row[x] for x in group))
            group_cords = [(x, y_row) for x in group]

            adjacent_cords = set(
                item 
                for group_adj in [get_adjacent_cords(_in, x, y_row) for x in group]
                for item in group_adj
                if item not in group_cords
            )

            for x, y in adjacent_cords:
                if _in[y][x] == "*":
                    if gears.get((x, y)) is None:
                        gears[(x, y)] = []
                    gears[(x, y)].append(number)

    return sum(
        gear_adj_numbers[0]*gear_adj_numbers[1]
        for gear, gear_adj_numbers in gears.items()
        if len(gear_adj_numbers) == 2
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
