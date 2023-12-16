#!/usr/bin/env python3
from sys import argv
from datetime import datetime

import numpy as np


def get_input(filename: str):
    with open(filename, "r") as f:
        _in = np.array([list(line) for line in f.read().split("\n") if line.split()])

    return _in


def can_move(_in: np.array, new_pos: tuple[int, int]) -> None:

    height = len(_in)
    width = len(_in[0])

    y = new_pos[0]
    x = new_pos[1]
    
    if y < 0 or y >= height or x < 0 or x >= width:
        return False
    
    return _in[y][x] == "."



def move_rock(_in: np.array, pos: tuple[int, int], vector: tuple[int, int]) -> None:

    new_pos = pos
    while can_move(_in, (new_pos[0] + vector[0], new_pos[1] + vector[1])):
        new_pos = (new_pos[0] + vector[0], new_pos[1] + vector[1])
    
    _in[pos[0]][pos[1]] = "."
    _in[new_pos[0]][new_pos[1]] = "O"


def get_ranges(_in: np.array, vector: tuple[int, int]) -> tuple[range, range]:
    y = vector[0]
    x = vector[1]
    
    if x < 0 or y < 0:
        return range(len(_in)), range(len(_in[y]))
    else:
        return range(len(_in)-1, -1, -1), range(len(_in[y])-1, -1, -1), 


def move_board(_in: np.array, vector: tuple[int, int]) -> None:
    
    y_range, x_range = get_ranges(_in, vector)

    for y in y_range:
        for x in x_range:
            if _in[y][x] == "O":
                move_rock(_in, (y, x), vector)


def get_board_score(_in: np.array) -> int:

    height = len(_in)
    width = len(_in[0])

    score = 0

    for y in range(height):
        for x in range(width):
            if _in[y][x] == "O":
                score += height - y

    return score


def part1(_in):
    move_board(_in, (-1, 0))
    
    return get_board_score(_in)


def get_board_hash(_in) -> int:
    return hash("".join("".join(char for char in row) for row in _in))


def part2(_in):
    board_hashes = []
    while get_board_hash(_in) not in board_hashes:
        board_hashes.append(get_board_hash(_in))
        for vector in [
            (-1, 0),
            (0, -1),
            (1, 0),
            (0, 1)
        ]:
            move_board(_in, vector)
    
    cycle_start_index = board_hashes.index(get_board_hash(_in))
    cycle_length = len(board_hashes) - cycle_start_index

    target = 1000000000 - cycle_start_index
    target %= cycle_length

    for _ in range(target):
        for vector in [
            (-1, 0),
            (0, -1),
            (1, 0),
            (0, 1)
        ]:
            move_board(_in, vector)

    # print(cycle_start_index, len(board_hashes), cycle_length, board_hashes)
    return get_board_score(_in)


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
