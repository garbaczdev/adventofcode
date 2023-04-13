#!/usr/bin/env python3
from sys import argv
from datetime import datetime

from enum import Enum
from abc import ABC, abstractmethod

import numpy as np



class Instruction(ABC):
    def __init__(self, _str: str):
        part1, part2 = _str.split(" through ")

        self._from = [int(num) for num in part1.split()[-1].split(",")]
        self._to = [int(num) for num in part2.split(",")]

    def get_slice(self) -> slice:
        return (slice(self._from[0], self._to[0]+1), slice(self._from[1], self._to[1]+1))

    @abstractmethod
    def perform(self, table: np.ndarray) -> None:
        pass


class OnInstruction(Instruction):
    def perform(self, table: np.ndarray) -> None:
        # PART 1
        # table[self.get_slice()].fill(1)

        # PART 2
        diff = np.zeros(np.shape(table[self.get_slice()]))
        diff.fill(1)
        table[self.get_slice()] += diff


class OffInstruction(Instruction):
    def perform(self, table: np.ndarray) -> None:
        # PART 1
        # table[self.get_slice()].fill(0)

        # PART 2

        table_slice = table[self.get_slice()]

        for y in range(len(table_slice)):
            for x in range(len(table_slice[y])):
                if table_slice[y][x] > 0:
                    table_slice[y][x] -= 1

        table[self.get_slice()] = table_slice

class ToggleInstruction(Instruction):

    def perform(self, table: np.ndarray) -> None:
        # PART 1
        # table[self.get_slice()] = np.logical_not(table[self.get_slice()])

        # PART 2
        diff = np.zeros(np.shape(table[self.get_slice()]))
        diff.fill(2)
        table[self.get_slice()] += diff



TYPE_TO_CLASS = {
    "turn on": OnInstruction,
    "turn off": OffInstruction,
    "toggle": ToggleInstruction,
}


def parse_instruction(_str: str) -> Instruction:
    part1, part2 = _str.split(" through ")
    return TYPE_TO_CLASS[" ".join(part1.split()[:-1])](_str)


def get_input(filename: str):
    with open(filename, "r") as f:
        _in = [parse_instruction(line) for line in f.read().split("\n") if line.split()]

    return _in


def part1(_in):

    table = np.zeros((1000, 1000))

    for instruction in _in:
        instruction.perform(table)

    print(table[500:, 500:])

    return int(np.sum(table))

def part2(_in):
    # FOR PART 1 CHANGE THE COMMENT IN INSTRUCTION CLASSES
    pass

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
