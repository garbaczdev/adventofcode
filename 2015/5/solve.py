#!/usr/bin/env python3
from sys import argv
from datetime import datetime


VOWELS = "aeiou"
FORBIDDEN_STRINGS = ["ab", "cd", "pq", "xy"]


def is_nice(word: str) -> bool:
    # Count the vowels
    if sum(word.count(vowel) for vowel in VOWELS) < 3:
        return False

    # Check whether there is a letter twice in a row
    if all(char1 != char2 for char1, char2 in zip(word, word[1:])):
        return False

    # Check whether it has a forbidden fragment
    if any(word.find(forbidden) != -1 for forbidden in FORBIDDEN_STRINGS):
        return False
    
    return True


def is_nicer(word: str) -> bool:

    if all(word.count(char1+char2) < 2 for char1, char2 in zip(word, word[1:])):
        return False

    if all(
        char1 != char3 
        for char1, char2, char3
        in zip(word, word[1:], word[2:])
    ):
        return False

    return True


def get_input(filename: str):
    with open(filename, "r") as f:
        _in = [line for line in f.read().split("\n") if line.split()]

    return _in


def part1(_in):
    nice_words = [word for word in _in if is_nice(word)]
    return len(nice_words)


def part2(_in):
    nicer_words = [word for word in _in if is_nicer(word)]
    return len(nicer_words)


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
