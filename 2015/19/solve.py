#!/usr/bin/env python3
from sys import argv
from datetime import datetime

from re import finditer
from functools import lru_cache


def get_input(filename: str):
    with open(filename, "r") as f:
        replacements_str, molecule = [
            segment.strip() 
            for segment in f.read().split("\n\n") 
            if segment.split()
        ]

        replacements = [
            (line.split(" => ")[0], line.split(" => ")[1])
            for line in replacements_str.split("\n") 
            if line.split()
        ]

    return (tuple(replacements), molecule)


@lru_cache
def get_possible_molecules(molecule: str, replacements: tuple[tuple]) -> frozenset[str]:

    possible_molecules = set()

    for key, val in replacements:
        occurences = [m.start() for m in finditer(key, molecule)]
        for occurence in occurences:
            new_molecule = molecule[:occurence] + val + molecule[occurence + len(key):]
            possible_molecules.add(new_molecule)

    return frozenset(possible_molecules)

def part1(_in):
    replacements, molecule = _in
    molecules = get_possible_molecules(molecule, replacements)

    return len(list(get_possible_molecules(molecule, replacements)))

def part2(_in):
    replacements, wanted_molecule = _in

    possible_molecules = set()
    possible_molecules.add("e")

    step = 0

    while wanted_molecule not in possible_molecules:
        new_possible_molecules = set()
    
        for molecule in possible_molecules:
            current_possible_molecules = get_possible_molecules(molecule, replacements)
            for possible_molecule in current_possible_molecules:
                new_possible_molecules.add(possible_molecule)

        possible_molecules = new_possible_molecules
        step += 1
        print(step, len(possible_molecules))
        print(possible_molecules)

    return step


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
