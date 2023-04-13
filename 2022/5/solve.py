from copy import deepcopy


def get_input() -> list:
    with open("input.txt", "r") as f:
        piles_in, instructions_in = f.read().split("\n\n")

    piles_lines = piles_in.split("\n")
    piles_numbers = [int(pile_num) for pile_num in piles_lines[-1].split()]

    piles = {pile_num: [] for pile_num in piles_numbers}
    
    max_pile_num = max(piles_numbers)
    
    # Parse piles input
    for line in reversed(piles_lines[:-1]):
        for i in range(max_pile_num):
            crate = line[i*4 + 1]
            if crate != " ":
                piles[i+1].append(crate)
        
    # instructions = [[how_many, from, to]]
    instructions = list()

    for instruction in instructions_in.split("\n"):
        if instruction.split():
            for word in ["move ", "from ", "to "]:
                instruction = instruction.replace(word, "")
            
            instruction_parsed = [int(num) for num in instruction.split()]
            instructions.append(instruction_parsed)

    _in = [piles, instructions]
    return _in


def part1(_in: list) -> None:
    piles, instructions = _in
    # This will be modified so we copy this
    piles = deepcopy(piles)

    for instruction in instructions:
        # i = how many piles to move
        for i in range(instruction[0]):
            crate = piles[instruction[1]].pop()
            piles[instruction[2]].append(crate)

    piles_sorted = sorted(piles.items(), key=lambda x: x[0])
    last_symbols = [pile[-1] for pile_num, pile in piles_sorted]
    solution = "".join(last_symbols)
    print(solution)
    


def part2(_in: list) -> None:
    piles, instructions = _in
    # This will be modified so we copy this
    piles = deepcopy(piles)

    for instruction in instructions:
        # i = how many piles to move
        crates = list()
        for i in range(instruction[0]):
            crate = piles[instruction[1]].pop()
            crates.append(crate)
        
        crates.reverse()

        for crate in crates:
            piles[instruction[2]].append(crate)

    piles_sorted = sorted(piles.items(), key=lambda x: x[0])
    last_symbols = [pile[-1] for pile_num, pile in piles_sorted]
    solution = "".join(last_symbols)
    print(solution)


def main() -> None:
    _in = get_input()
    part1(_in)
    part2(_in)


if __name__ == "__main__":
    main()
