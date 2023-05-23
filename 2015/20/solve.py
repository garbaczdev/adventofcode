#!/usr/bin/env python3
from sys import argv
from datetime import datetime

import math
from functools import lru_cache


def prime_factors(n: int) -> list[int]:

    factors = list()

    while n % 2 == 0:
        factors.append(2)
        n = n / 2

    for i in range(3, int(math.sqrt(n)) + 1, 2):
        # while i divides n
        while n % i == 0:
            factors.append(i)
            n = n / i
    # if n is a prime
    if n > 2:
        factors.append(int(n))
    
    return factors


def get_dividers(n: int) -> list[int]:
    dividers = list()

    for i in range(1, int(n/2)+1):
        if n % i == 0:
            dividers.append(i)

    dividers.append(n)

    return dividers


def get_smallest_divider(n: int) -> int:
    for i in range(2, int(n/2)+1):
        if n % i == 0:
            return i
    return i


@lru_cache
def get_house_presents(house_num: int) -> int:
    
    if house_num == 1:
        return 10
    
    smallest_divider = get_smallest_divider(house_num)

    return get_house_presents(house_num // smallest_divider)


def get_input(filename: str):
    with open(filename, "r") as f:
        _in = int(f.read().replace("\n", "").strip())
    return _in


def part1(_in):

    i = 2
    while get_house_presents(i) <= _in:
        i += 1

    return i


def part2(_in):
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
