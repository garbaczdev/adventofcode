

def get_input() -> list:
    with open("input.txt", "r") as f:
        _in = [line for line in f.read().split("\n") if line.split()]

    return _in


def part1(_in: list) -> None:
    code = _in[0]
    
    for i in range(4, len(code)):
        if len(set(code[i-4:i])) == 4:
            print(i)
            return


def part2(_in: list) -> None:
    code = _in[0]
    
    for i in range(14, len(code)):
        if len(set(code[i-14:i])) == 14:
            print(i)
            return


def main() -> None:
    _in = get_input()
    part1(_in)
    part2(_in)


if __name__ == "__main__":
    main()
