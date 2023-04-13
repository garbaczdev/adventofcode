
ACTUAL_SYMBOLS = {
        "X": "A",
        "Y": "B",
        "Z": "C"
}

BEATS = {
    "A": "C",
    "B": "A",
    "C": "B"
}


POINTS = {
    "A": 1,
    "B": 2,
    "C": 3
}


def get_points(round: tuple) -> int:

    points = POINTS[round[1]]

    if round[0] == round[1]:
        # Draw
        points += 3

    elif BEATS[round[1]] == round[0]:
        # You win
        points += 6

    return points


def get_symbol(round: tuple) -> str:
    if round[1] == "X":
        # You need to lose
        return BEATS[round[0]]
    elif round[1] == "Y":
        # You need to draw
        return round[0]
    elif round[1] == "Z":
        # You need to win
        for symbol, beats in BEATS.items():
            if beats == round[0]:
                return symbol


def part2(game: list) -> None:
    game = [(round[0], get_symbol(round)) for round in game]
    score = sum(get_points(round) for round in game)
    print(score)
    

def part1(game: list) -> None:
    game = [(round[0], ACTUAL_SYMBOLS[round[1]]) for round in game]
    score = sum(get_points(round) for round in game)
    print(score)


def get_input() -> list:
    with open("input.txt", "r") as f:
        lines = [tuple(line.split()) for line in f.read().split("\n") if line.split()]

    return lines


def main():
    game = get_input()
    part1(game)
    part2(game)


if __name__ == "__main__":
    main()
