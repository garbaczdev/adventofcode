
def task1(positions: list) -> None:
    possible_positions = [i for i in range(min(positions), max(positions) + 1)]

    fuels = list()

    for possible_position in possible_positions:
        fuels.append(sum([abs(position - possible_position) for position in positions]))

    print(min(fuels))

def task2(positions: list) -> None:
    possible_positions = [i for i in range(min(positions), max(positions) + 1)]

    fuels = list()

    for possible_position in possible_positions:
        fuel = 0
        for position in positions:
            distance = abs(position - possible_position)
            fuel += int(distance*(distance+1)/2)

        fuels.append(fuel)

    print(min(fuels))

def main() -> None:
    with open("input.txt", "r") as f:
        positions = [int(num) for num in f.read().split(",")]

    task2(positions)


if __name__ == '__main__':
    main()
