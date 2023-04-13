

def get_input() -> list:
    with open("input.txt", "r") as f:
        _in = [line for line in f.read().split("\n") if line.split()]

    return _in


def get_item_value(item: str) -> int:
    item = ord(item)
    if 65 <= item <= 90:
        return item - 38
    else:
        return item - 96


def get_items_value(items: list) -> int:
    return sum(get_item_value(item) for item in items)


def part1(_in: list) -> None:
    
    items = list()

    for rucksack in _in:
        pivot = int(len(rucksack)/2)
        common_item = set(rucksack[:pivot]) & set(rucksack[pivot:])
        items.append(list(common_item)[0])

    print(get_items_value(items))
    

def part2(_in: list) -> None:
    badges = list()
    for i in range(0, len(_in), 3):
        group = _in[i:i+3]
        badge = set(_in[i]) & set(_in[i+1]) & set(_in[i+2])
        badges.append(list(badge)[0])

    print(get_items_value(badges))


def main() -> None:
    _in = get_input()
    part1(_in)
    part2(_in)


if __name__ == "__main__":
    main()
