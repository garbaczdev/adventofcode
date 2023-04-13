
MAX_DEPTH = 40

def template_step(template: str, rules: dict) -> str:
    result = template[0]

    for current_char, next_char in zip(template, template[1:]):
        pair = current_char + next_char
        
        if rules.get(pair) is not None:
            result += rules[pair] + next_char

    return result


def task1(template: str, rules: dict) -> None:
    for _ in range(10):
        template = template_step(template, rules)

    letter_occurances = [template.count(letter) for letter in frozenset(template)]
    print(max(letter_occurances) - min(letter_occurances))


def calculate_pair_occurances(pair_occurances: str, rules: dict, iterations: int) -> dict:
    for _ in range(iterations):

        new_pair_occurances = dict()

        for pair in pair_occurances.keys():
            if rules.get(pair) is not None:

                new_pairs = [pair[0] + rules[pair], rules[pair] + pair[1]]
                
                for new_pair in new_pairs:
                    
                    if new_pair_occurances.get(new_pair) is None:
                        new_pair_occurances[new_pair] = 0

                    new_pair_occurances[new_pair] += pair_occurances[pair]

        pair_occurances = new_pair_occurances

    return pair_occurances

def get_initial_pair_occurances(template: str) -> dict:
    pair_occurances = dict()

    for char, next_char in zip(template, template[1:]):

        pair = char + next_char

        if pair_occurances.get(pair) is None:
            pair_occurances[pair] = 0

        pair_occurances[pair] += 1
    
    return pair_occurances

def calculate_letter_occurance(template: str, pair_occurances: dict, letter: str) -> int:

    count = 0

    for pair in pair_occurances:
        if pair[0] == letter:
            count += pair_occurances[pair]
    
    if template[-1] == letter:
        count += 1

    return count


def task2(template: str, rules: dict) -> None:

    pair_occurances = get_initial_pair_occurances(template)
    pair_occurances = calculate_pair_occurances(pair_occurances, rules, 40)

    possible_letters = frozenset(list(template) + [letter for letter in rules.values()])

    letter_occurances = {letter: calculate_letter_occurance(template, pair_occurances, letter) for letter in possible_letters}

    print(max(letter_occurances.values()) - min(letter_occurances.values()))


def main() -> None:
    with open("input.txt", "r") as f:
        segments = [segment for segment in f.read().split("\n\n") if segment.strip()]
        template = segments[0]
        rules = {line.split("->")[0].strip() : line.split("->")[1].strip() for line in segments[1].split("\n")}
    
    # task1(template, rules)
    task2(template, rules)


if __name__ == '__main__':
    main()
