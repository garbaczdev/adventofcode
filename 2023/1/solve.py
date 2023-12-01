#!/usr/bin/env python3
from sys import argv
from datetime import datetime

from re import finditer


WORDS_TO_DIGITS = {
    "one": 1,
    "two": 2,
    "three": 3,
    "four": 4,
    "five": 5,
    "six": 6,
    "seven": 7,
    "eight": 8,
    "nine": 9,
}


def is_int(num: str) -> bool:
    try:
        int(num)
        return True
    except:
        return False


def get_occurring_digits(line: str) -> dict:
    return {
        word: [m.start() for m in finditer(word, line)] 
        for word in WORDS_TO_DIGITS
        if word in line
    }


def get_first_digit(line: str) -> str:
    for index in range(len(line)):
        if is_int(line[index]):
            return line[index]
        for word in WORDS_TO_DIGITS:
            if word in line[:index+1]:
                return str(WORDS_TO_DIGITS[word])
    return ""


def get_last_digit(line: str) -> str:
    for index in range(len(line) - 1, -1, -1):
        if is_int(line[index]):
            return line[index]
        for word in WORDS_TO_DIGITS:
            if word in line[index:]:
                return str(WORDS_TO_DIGITS[word])
    return ""


def get_line_score_p2(line: str) -> int:
    score = get_first_digit(line) + get_last_digit(line)
    return int(score)


def get_input(filename: str):
    with open(filename, "r") as f:
        _in = [line for line in f.read().split("\n") if line.split()]

    return _in


def part1(_in):
    _in = [
        "".join(char for char in line if is_int(char))
        for line in _in
    ]
    _in = [int(line[0] + line[-1]) for line in _in]
    return sum(_in)


def part2(_in):
    return sum(get_line_score_p2(line) for line in _in)


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
