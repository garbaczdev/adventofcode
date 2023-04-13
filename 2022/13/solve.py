#!/usr/bin/env python3
from sys import argv

from copy import deepcopy
from functools import lru_cache

import numpy as np


LEGAL_CHARACTERS = set([str(i) for i in range(0, 10)] + list("[], \n"))

def get_input(filename: str) -> list:
    with open(filename, "r") as f:
        content = f.read()
        for char in content:
            if char not in LEGAL_CHARACTERS:
                raise Exception("The input contains illegal characters")
        _in = [[eval(line) for line in pair.split("\n") if line.split()] for pair in content.split("\n\n") if pair.split()]

    return _in

def compare_inputs(left_input: list, right_input: list) -> int:
    """
    Return 0 if no decision has been done.
    1 if the inputs are right.
    -1 if the inputs are wrong.
    """
    for left, right in zip(left_input, right_input):
        if isinstance(left, int) and isinstance(right, list):
            left = [left]

        if isinstance(left, list) and isinstance(right, int):
            right = [right]
        
        if isinstance(left, int) and isinstance(right, int):
            if left != right:
                return 1 if left < right else -1

        if isinstance(left, list) and isinstance(right, list):
            result = compare_inputs(left, right)
            if result != 0:
                return result
    
    if len(left_input) == len(right_input):
        return 0

    return 1 if len(left_input) < len(right_input) else -1


def part1(_in: list) -> None:
    _in = deepcopy(_in)
    results = []
    for left_input, right_input in _in:
        results.append(compare_inputs(left_input, right_input))

    _sum = 0
    for i, result in enumerate(results):
        if result == 1:
            _sum += i + 1

    print("PART 1:", _sum)


def part2(_in: list) -> None:
    _in = deepcopy(_in)
    _in = [_input for pair in _in for _input in pair]
    _in.append([[2]])
    _in.append([[6]])

    bigger_inputs = dict()
    for in1 in _in:
        bigger_inputs[str(in1)] = []
        for in2 in _in:
            if compare_inputs(in1, in2) == 1:
                bigger_inputs[str(in1)].append(in2)


    _inputs_ranking = [(key, len(value)) for key, value in bigger_inputs.items()]
    _inputs_ranking.sort(key=lambda x: x[1], reverse=True)
    _inputs_sorted = list(map(lambda x: x[0], _inputs_ranking))
    # print("\n".join(_inputs_sorted))

    solution = (_inputs_sorted.index("[[2]]") + 1) * (_inputs_sorted.index("[[6]]") + 1)

    print("PART 2:", solution)


def main() -> None:
    if len(argv) < 2:
        print("Provide the file name")
        return
    _in = get_input(argv[1])
    part1(_in)
    part2(_in)


if __name__ == "__main__":
    main()
