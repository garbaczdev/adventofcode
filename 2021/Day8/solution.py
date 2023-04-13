
from typing import Union


TASK1_WANTED_LENGTHS = [2, 3, 4, 7]

ALL_SIGNALS = "abcdefg"

DIGIT_SIGNAL_PATTERNS = {
    0: frozenset("abcefg"),
    1: frozenset("cf"),
    2: frozenset("acdeg"),
    3: frozenset("acdfg"),
    4: frozenset("bcdf"),
    5: frozenset("abdfg"),
    6: frozenset("abdefg"),
    7: frozenset("acf"),
    8: frozenset("abcdefg"),
    9: frozenset("abcdfg")
}

REVERSED_DIGIT_SIGNAL_PATTERNS = {_frozenset: digit for digit, _frozenset in DIGIT_SIGNAL_PATTERNS.items()}

REVERSED_DIGIT_SIGNAL_PATTERN_LENGTHS = {length: list() for length in range(2, len(ALL_SIGNALS) + 1)}
for digit, _frozenset in DIGIT_SIGNAL_PATTERNS.items():
    REVERSED_DIGIT_SIGNAL_PATTERN_LENGTHS[len(_frozenset)].append(digit)


def decode_digit(decoding: dict, signal_pattern: frozenset) -> int:
    decoded_signal_pattern = frozenset(decoding[signal] for signal in signal_pattern)
    decoded_digit = REVERSED_DIGIT_SIGNAL_PATTERNS[decoded_signal_pattern]
    return decoded_digit


def decode(signal_patterns: list) -> dict:

    # Try every possible combination
    def dfs(current_possible_signals: list = list()) -> Union[dict, None]:

        if len(current_possible_signals) == len(ALL_SIGNALS):

            decoding = {signal: decoded_signal for signal, decoded_signal in zip(ALL_SIGNALS, current_possible_signals)}

            try:
                for signal_pattern in signal_patterns:
                    decoded_digit = decode_digit(decoding, signal_pattern)

            except KeyError:
                return None

            return decoding
            
        else:
            for possible_signal in ALL_SIGNALS:

                if possible_signal not in current_possible_signals:

                    decoding = dfs(current_possible_signals + [possible_signal])

                    if decoding is not None:
                        return decoding

    return dfs()




def task2(lines: list) -> None:

    numbers = list()

    for line in lines:

        decoding = decode(line[0])

        number = 0

        for output_signal_pattern in line[1]:
            number *= 10
            number += decode_digit(decoding, output_signal_pattern)

        numbers.append(number)

    print(sum(numbers))



def task1(lines: list) -> None:

    count = 0

    for _, output in lines:
        for sequence in output:
            if len(sequence) in TASK1_WANTED_LENGTHS:
                count += 1

    print(count)

def main() -> None:
    with open("input.txt", "r") as f:
        lines = [([frozenset(word) for word in line.split("|")[0].split()], [frozenset(word) for word in line.split("|")[1].split()]) 
                for line in f.read().split("\n") if line.strip()]

    # task1(lines)
    task2(lines)


if __name__ == '__main__':
    main()
