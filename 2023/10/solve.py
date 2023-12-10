#!/usr/bin/env python3
from sys import argv
from datetime import datetime

import numpy as np


#(y, x)
PIPE_CONNECTIONS = {
    "|": frozenset([(-1, 0), (1, 0)]),
    "-": frozenset([(0, -1), (0, 1)]),
    "L": frozenset([(-1, 0), (0, 1)]),
    "J": frozenset([(-1, 0), (0, -1)]),
    "7": frozenset([(1, 0), (0, -1)]),
    "F": frozenset([(1, 0), (0, 1)])
}


ADJACENT_VECTORS = [
    (y, x)
    for x in range(-1, 2)
    for y in range(-1, 2)
    if abs(x) + abs(y) == 1
]


def get_adjacent_cords(
    _in: list[str], 
    pos: tuple, 
    adjacent_vectors = ADJACENT_VECTORS
) -> list[tuple[int, int]]:

    y = pos[0]
    x = pos[1]

    height = len(_in)
    width = len(_in[0])

    adjacent_cords = []

    for y_d, x_d in adjacent_vectors:

        y_n = y + y_d
        x_n = x + x_d
        
        if all([
            x_n >= 0,
            x_n < width,
            y_n >= 0,
            y_n < height
        ]):
            adjacent_cords.append((y_n, x_n))

    return adjacent_cords



def get_input(filename: str):
    with open(filename, "r") as f:
        _in = np.array([list(line) for line in f.read().split("\n") if line.split()])

    return _in


# Checks whether pos_2 can be connected to pos_1
def can_be_adjacent(_in, pos_1, pos_2) -> bool:
    if _in[pos_2] == ".":
        return False
    
    return pos_1 in get_adjacent_cords(_in, pos_2, PIPE_CONNECTIONS[_in[pos_2]])


def get_pipe_type(_in: np.array, pos: tuple) -> str:
    adjacent_cords = get_adjacent_cords(_in, pos)

    adjacent_pipes_relative_cords = frozenset(
        (y_a - pos[0], x_a - pos[1])
        for y_a, x_a in adjacent_cords
        if can_be_adjacent(_in, pos, (y_a, x_a))
    )

    pipe_type = [
        pipe_type 
        for pipe_type, adjacent_cords in PIPE_CONNECTIONS.items()
        if adjacent_cords == adjacent_pipes_relative_cords
    ][0]
    # print(adjacent_pipes_relative_cords, pipe_type)
    return pipe_type


def get_pipe_map(_in: np.array) -> tuple[tuple, dict]:
    _in = np.copy(_in)

    # (y, x)
    s_pos = tuple(map(lambda x: int(x[0]), np.where(_in == "S")))
    s_type = get_pipe_type(_in, s_pos)
    _in[s_pos] = s_type
    # print(_in)

    pipe_map = {
        (y, x): get_adjacent_cords(_in, (y, x), PIPE_CONNECTIONS[_in[y][x]])
        for y in range(len(_in))
        for x in range(len(_in[0]))
        if _in[y][x] != "."
    }
    
    return s_pos, pipe_map 
                                


def part1(_in):
    s_pos, pipe_map = get_pipe_map(_in)

    cycle_length = 0
    current_pos = s_pos
    last_pos = s_pos

    while current_pos != s_pos or cycle_length == 0:
        last_pos, current_pos = current_pos, [
            pos for pos in pipe_map[current_pos] 
            if pos != last_pos
        ][0]
        cycle_length += 1
    
    return int(cycle_length / 2)


def get_flow_bitmask(_in, loop_set) -> np.array:
    loop_bitmask = np.copy(_in)
    for y in range(len(_in)):
        for x in range(len(_in[0])):
            loop_bitmask[y][x] = 2 if (y, x) in loop_set else 0
    
    large_flow_bitmask = np.zeros((loop_bitmask.shape[0] + 2, loop_bitmask.shape[1] + 2))
    large_flow_bitmask[1:loop_bitmask.shape[0]+1, 1:loop_bitmask.shape[1]+1] = loop_bitmask

    next_pos = [(0, 0)]
    while next_pos:
        pos = next_pos.pop(0)
        if large_flow_bitmask[pos] != 0:
            continue

        large_flow_bitmask[pos] = 1
        for adj_pos in get_adjacent_cords(large_flow_bitmask, pos):
            if large_flow_bitmask[adj_pos] == 0:
                next_pos.append(adj_pos)

    flow_bitmask = large_flow_bitmask[1:-1, 1:-1]
    return flow_bitmask


def is_closed_vertically(up_row_el, down_row_el):
    if up_row_el == "." or down_row_el == ".":
        return False
    
    return (1, 0) in PIPE_CONNECTIONS[up_row_el] and (-1, 0) in PIPE_CONNECTIONS[down_row_el]


def is_closed_horizontaly(left_row_el, right_row_el):
    if left_row_el == "." or right_row_el == ".":
        return False
    
    return (0, 1) in PIPE_CONNECTIONS[left_row_el] and (0, -1) in PIPE_CONNECTIONS[right_row_el]


def expand_tunnels(_in):

    _in = np.copy(_in)
    s_pos = tuple(map(lambda x: int(x[0]), np.where(_in == "S")))
    s_type = get_pipe_type(_in, s_pos)
    _in[s_pos] = s_type

    in_expanded_horizontally = []

    # Expand Horizontally
    for row, next_row in zip(_in, _in[1:]):
        generated_row = np.copy(row)
        for x in range(len(row)):
            if is_closed_vertically(row[x], next_row[x]):
                generated_row[x] = "|"
            else:
                generated_row[x] = "."
        in_expanded_horizontally.append(row)
        in_expanded_horizontally.append(generated_row)

    in_expanded_horizontally.append(_in[-1])
    in_expanded_horizontally = np.array(in_expanded_horizontally)

    expanded_columns = []
    for x in range(len(in_expanded_horizontally[0]) - 1):

        current_col = in_expanded_horizontally[:, x]
        next_col = in_expanded_horizontally[:, x+1]

        generated_col = np.copy(current_col)

        for y in range(len(current_col)):
            if is_closed_horizontaly(current_col[y], next_col[y]):
                generated_col[y] = "-"
            else:
                generated_col[y] = "."

        expanded_columns.append(current_col)
        expanded_columns.append(generated_col) 
    
    expanded_columns.append(in_expanded_horizontally[:, -1])
    in_expanded = np.array(expanded_columns).T

    in_expanded[s_pos[0]*2][s_pos[1]*2] = "S"

    return in_expanded


def part2(_in):
    
    _in = expand_tunnels(_in)
    # print(_in)

    s_pos, pipe_map = get_pipe_map(_in)

    loop = list()
    current_pos = s_pos
    last_pos = s_pos

    while current_pos != s_pos or len(loop) == 0:
        loop.append(current_pos)
        last_pos, current_pos = current_pos, [
            pos for pos in pipe_map[current_pos] 
            if pos != last_pos
        ][0]

    loop_set = set(loop)
    flow_bitmask = get_flow_bitmask(_in, loop_set)
    flow_bitmask = flow_bitmask[::2, ::2]
    # print(flow_bitmask)
    return np.count_nonzero(flow_bitmask == 0)
    


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
