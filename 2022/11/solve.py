#!/usr/bin/env python3
from sys import argv

from math import gcd
from copy import deepcopy


class Monkey:
    def __init__(self, monkey_str: str):
        self._monkey_str = monkey_str
        lines = monkey_str.split("\n")

        self.id = int(lines[0][7:-1])
        self.items = [int(item) for item in lines[1][18:].split(", ")]

        self.operation = lines[2][19:]
        
        self._divider = int(lines[3][21:])
        self._test_true = int(lines[4][29:])
        self._test_false = int(lines[5][30:])

        self._inspect_count = 0
    
    @property
    def inspect_count(self):
        return self._inspect_count

    def test(self, value: int) -> int:
        if not value % self._divider:
            return self._test_true
        return self._test_false

    def get_worry_level(self, old:int):
        return int(eval(self.operation) / 3)

    def inspect(self, old: int) -> tuple[int, int]:
        new = self.get_worry_level(old)

        new_monkey = self.test(new)

        self._inspect_count += 1

        return new, new_monkey


class AdvancedMonkey(Monkey):
    def __init__(self, monkey_str: str, supermodulo: int):
        super().__init__(monkey_str)
        
        self.supermodulo = supermodulo
        
        self.operation_optimized = self.get_optimized_operation()

    def get_optimized_operation(self):
        components = self.operation.split()
        if components[1] == "+":
            if components[2] == "old":
                return lambda x: x*2
            else:
                return lambda x: x + int(components[2])
        else:
            if components[2] == "old":
                return lambda x: x**2
            else:
                return lambda x: x * int(components[2])


    def get_worry_level(self, old:int):
        new = self.operation_optimized(old)
        return new % self.supermodulo


def get_input(filename: str) -> list:
    with open(filename, "r") as f:
        _in = [Monkey(monkey_str) for monkey_str in f.read().split("\n\n") if monkey_str.split()]

    return _in


def part1(_in: list) -> None:
    monkeys = deepcopy(_in)
    for round_number in range(20):
        for monkey in monkeys:
            for item in monkey.items:
                new_item, new_monkey = monkey.inspect(item)
                monkeys[new_monkey].items.append(new_item)
            monkey.items = []

    monkeys.sort(key=lambda monkey: monkey.inspect_count)
    monkey_business_level = monkeys[-1].inspect_count * monkeys[-2].inspect_count
    print("PART 1:",monkey_business_level)

def part2(_in: list) -> None:

    divisors = [monkey._divider for monkey in _in]
    supermodulo = 1 
    for divisor in divisors:
        supermodulo *= divisor

    monkeys = [AdvancedMonkey(monkey._monkey_str, supermodulo) for monkey in _in]

    for round_number in range(10000):
        for monkey in monkeys:
            for item in monkey.items:
                new_item, new_monkey = monkey.inspect(item)
                monkeys[new_monkey].items.append(new_item)
            monkey.items = []

    monkeys.sort(key=lambda monkey: monkey.inspect_count)
    monkey_business_level = monkeys[-1].inspect_count * monkeys[-2].inspect_count
    print("PART 2:", monkey_business_level)


def main() -> None:
    if len(argv) < 2:
        print("Provide the file name")
        return
    _in = get_input(argv[1])
    part1(_in)
    part2(_in)


if __name__ == "__main__":
    main()
