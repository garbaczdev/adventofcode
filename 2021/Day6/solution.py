

def task1(initial_state: list) -> None:
    
    current_state = initial_state

    for day_index in range(80):
        new_state = list()
        
        for fish in current_state:
            if fish == 0:
                new_state.append(6)
                new_state.append(8)
            else:
                new_state.append(fish - 1)

        current_state = new_state

    print(len(current_state))

def task2(initial_state: list) -> None:
    current_state = {num: 0 for num in range(9)}

    for num in initial_state:
        current_state[num] += 1

    for day_index in range(256):

        new_fish = current_state[0]

        for num in range(8):
            current_state[num] = current_state[num + 1]

        current_state[6] += new_fish
        current_state[8] = new_fish

    print(sum(current_state.values()))


def main() -> None:

    with open("input.txt", "r") as f:
        initial_state = [int(num) for num in f.read().split(",")]

    # task1(initial_state)
    task2(initial_state)


if __name__ == '__main__':
    main()
