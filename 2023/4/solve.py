#!/usr/bin/env python3
from sys import argv
from datetime import datetime

from functools import lru_cache


def get_input(filename: str):
    with open(filename, "r") as f:
        _in = [
                [
                    [int(num) for num in part.split()] 
                    for part in line.split(": ")[1].split(" | ")
                ] 
                for line in f.read().split("\n") if line.split()
            ]

    return _in


def part1(_in):
    matches = [
        len(set(winning) & set(hand))
        for winning, hand in _in
    ]
    return sum(
        2**(match - 1)
        for match in matches
        if match > 0
    )




def part2(_in):
    matches = [
        len(set(winning) & set(hand))
        for winning, hand in _in
    ]
    matches = [len(matches)] + matches

    @lru_cache
    def get_scratchcards(card_num: int) -> dict:
        won_cards = list(range(card_num+1, card_num + matches[card_num] + 1))
        won_cards_count = {
            won_card: 0
            for won_card in won_cards + [card_num]
        }
        won_cards_count[card_num] = 1
        for won_card in won_cards:
            new_won_cards_count = get_scratchcards(won_card)
            for new_won_card, count in new_won_cards_count.items():
                if won_cards_count.get(new_won_card) is None:
                    won_cards_count[new_won_card] = count
                else:
                    won_cards_count[new_won_card] += count

        return won_cards_count
    
    matches_count = get_scratchcards(0)
    matches_count[0] = 0
    return sum(matches_count.values())


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
