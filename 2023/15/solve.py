#!/usr/bin/env python3
from sys import argv
from datetime import datetime


def get_input(filename: str):
    with open(filename, "r") as f:
        _in = [instruction for instruction in f.read().split("\n")[0].split(",")]

    return _in


def hash_algo(_str: str) -> int:
    current = 0
    for char in _str:
        current = ((current + ord(char)) * 17) % 256
    return current


def part1(_in):
    return sum(hash_algo(step) for step in _in)


def part2(_in):
    boxes = [[] for _ in range(256)]
    for step in _in:
        if "=" in step:
            lens, strength = step.split("=")
            strength = int(strength)
            box_idx = hash_algo(lens)

            if any(lens==box_lens for box_lens, strength in boxes[box_idx]):
                boxes[box_idx] = [
                    (box_lens, strength)
                    if box_lens == lens 
                    else (box_lens, box_strength)
                    for box_lens, box_strength in boxes[box_idx]
                ]
            else:
                boxes[box_idx].append((lens, strength))
        else:
            # "-" in step
            lens = step.replace("-", "")
            box_idx = hash_algo(lens)
            boxes[box_idx] = [
                (box_lens, box_strength)
                for box_lens, box_strength in boxes[box_idx]
                if box_lens != lens
            ]

    return sum(
        (box_idx+1)*sum(
            (el_idx+1)*el[1] 
            for el_idx, el in enumerate(box)
        )
        for box_idx, box in enumerate(boxes)
    )

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
