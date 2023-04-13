

def get_input() -> list:
    with open("input.txt", "r") as f:
        _in = [[[int(number) for number in pair.split("-")] for pair in line.split(",")] for line in f.read().split("\n") if line.split()]

    return _in


def contains(interval1: list, interval2: list) -> bool:
    return interval1[0] <= interval2[0] and interval1[1] >= interval2[1]


def overlaps(pair: list) -> bool:
    interval1, interval2 = pair
    return len(set(range(interval1[0], interval1[1]+1)) & set(range(interval2[0], interval2[1]+1))) > 0


def part1(_in: list) -> None:
    count = 0
    for pair in _in:
        interval1, interval2 = pair
        if contains(interval1, interval2) or contains(interval2, interval1):
            count += 1

    print(count)


def part2(_in: list) -> None:
    count = 0
    for pair in _in:
        if overlaps(pair):
            count += 1
    print(count)


def main() -> None:
    _in = get_input()
    part1(_in)
    part2(_in)


if __name__ == "__main__":
    main()
