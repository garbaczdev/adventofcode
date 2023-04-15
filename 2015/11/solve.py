#!/usr/bin/env python3
from sys import argv
from datetime import datetime


LETTER = lambda x: chr(65 + x)

REQUIRED_SEQUENCES = [
    "".join(LETTER(i+j) for j in range(3)).lower()
    for i in range(24)
]

FORBIDDEN_LETTERS = "iol"


def next_password(password: str) -> str:

    if password[-1] == "z":
        return next_password(password[:-1]) + "a"
    else:
        return password[:-1] + chr(ord(password[-1])+1)


def is_password_correct(password: str) -> bool:
    if all(sequence not in password for sequence in REQUIRED_SEQUENCES):
        return False

    if any(letter in password for letter in FORBIDDEN_LETTERS):
        return False

    count = 0
    i = 0
    
    while i < len(password) - 1:
        if password[i] == password[i+1]:
            count += 1
            i += 2
        else:
            i+= 1

    if count < 2:
        return False

    return True


def get_input(filename: str):
    with open(filename, "r") as f:
        _in = f.read().replace("\n", "").strip()
    return _in


def part1(_in):
    while not is_password_correct(_in):
        _in = next_password(_in)
    return _in


def part2(_in):
    return part1(next_password(part1(_in)))

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
