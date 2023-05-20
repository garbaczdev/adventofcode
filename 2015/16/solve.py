#!/usr/bin/env python3
from sys import argv
from datetime import datetime


GREATER_THAN_READINGS = ["cats", "trees"]
FEWER_THAN_READINGS = ["pomeranians", "goldfish"]


def is_possible_aunt(aunt: dict, requirements: dict) -> bool:
    return all(value == requirements[attr] for attr, value in aunt.items())


def is_possible_aunt_p2(aunt: dict, requirements: dict) -> bool:
    for attr, value in aunt.items():
        if attr in GREATER_THAN_READINGS:
            if value <= requirements[attr]:
                return False
        elif attr in FEWER_THAN_READINGS:
            if value >= requirements[attr]:
                return False
        else:
            if value != requirements[attr]:
                return False
    return True


def get_requirements(filename: str):
    with open(filename, "r") as f:
        requirements = {
            line.split(": ")[0] : int(line.split(": ")[1])
            for line in f.read().split("\n") 
            if line.split()
        }
    return requirements


def get_input(filename: str):
    with open(filename, "r") as f:
        _in = {
            int(line.split()[1][:-1]) : {
                component.split(": ")[0]: int(component.split(": ")[1])
                for component in " ".join(
                    line.split()[2:]
                ).split(", ")
            }
            for line in f.read().split("\n") 
            if line.split()
        }

    return _in


def part1(_in):
    requirements = get_requirements("req.txt")
    possible_aunts = [
        (n, aunt) 
        for n, aunt in _in.items() 
        if is_possible_aunt(aunt, requirements)
    ]
    return possible_aunts[0]


def part2(_in):
    requirements = get_requirements("req.txt")
    possible_aunts = [
        (n, aunt) 
        for n, aunt in _in.items() 
        if is_possible_aunt_p2(aunt, requirements)
    ]
    return possible_aunts[0]


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
