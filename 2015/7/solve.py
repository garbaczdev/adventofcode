#!/usr/bin/env python3
from sys import argv
from datetime import datetime

from functools import lru_cache


class Register:
    def __init__(self, registers: dict, instruction_str: str):
        self.registers = registers
        self.instruction_str = instruction_str

    def get_value(self) -> int:

        instruction_str = self.instruction_str

        part1, part2 = self.instruction_str.split(" -> ")
        part1 = part1.split()

        if "AND" in instruction_str:
            return self.get_register_value(part1[0]) & self.get_register_value(part1[-1])
        elif "OR" in instruction_str:
            return self.get_register_value(part1[0]) | self.get_register_value(part1[-1])
        elif "NOT" in instruction_str:
            return self.get_register_value(part1[-1]) ^ 0xFFFF
        elif "LSHIFT" in instruction_str:
            return (self.get_register_value(part1[0]) << self.get_register_value(part1[-1])) & 0xFFFF
        elif "RSHIFT" in instruction_str:
            return (self.get_register_value(part1[0]) >> self.get_register_value(part1[-1])) & 0xFFFF
        else:
            # Register definition
            return self.get_register_value(part1[0])

    @lru_cache
    def get_register_value(self, register_name: str) -> int:
        try:
            return int(register_name)
        except ValueError:
            return self.registers[register_name].get_value()


def get_input(filename: str):
    with open(filename, "r") as f:
        _in = [line for line in f.read().split("\n") if line.split()]

    return _in


def part1(_in):

    registers = dict()
    for instruction_str in _in:
        registers[instruction_str.split(" -> ")[-1]] = Register(
            registers, 
            instruction_str
        )

    return registers["a"].get_value()


def part2(_in):

    b_rule = f"{part1(_in)} -> b" 

    _in = [instruction_str for instruction_str in _in if "-> b " not in instruction_str]
    _in.append(b_rule)

    registers = dict()
    for instruction_str in _in:
        registers[instruction_str.split(" -> ")[-1]] = Register(
            registers, 
            instruction_str
        )

    return registers["a"].get_value()


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
