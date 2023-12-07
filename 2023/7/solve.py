#!/usr/bin/env python3
from sys import argv
from datetime import datetime

from functools import cmp_to_key


CARD_STRENGTH_ORDER = ['2', '3', '4', '5', '6', '7', '8', '9', 'T', 'J', 'Q', 'K', 'A']
CARD_STRENGTH_ORDER2 = ['J','2', '3', '4', '5', '6', '7', '8', '9', 'T', 'Q', 'K', 'A']


def get_input(filename: str):
    with open(filename, "r") as f:
        _in = [(line.split()[0], int(line.split()[1])) for line in f.read().split("\n") if line.split()]

    return _in


def is_better(hand1_composed, hand2_composed):
    hand1 = hand1_composed[0]
    hand2 = hand2_composed[0]
    counts1 = set(hand1.count(card) for card in hand1)
    counts2 = set(hand2.count(card) for card in hand2)
    for count in range(5, 0, -1):
        if count not in counts1 and count not in counts2:
            continue
        if count not in counts2:
            return True
        if count not in counts1:
            return False
        pairs_count1 = len([card for card in hand1 if hand1.count(card) == 2]) 
        pairs_count2 = len([card for card in hand2 if hand2.count(card) == 2]) 
        if pairs_count1 != pairs_count2:
            return pairs_count1 > pairs_count2

    # Same type now
    for card1, card2 in zip(hand1, hand2):
        card1_ord = CARD_STRENGTH_ORDER.index(card1)
        card2_ord = CARD_STRENGTH_ORDER.index(card2)
        if card1_ord != card2_ord:
            return card1_ord > card2_ord


def modify_hand(hand: str) -> str:
    jokers_count = hand.count("J")
    if jokers_count == 0:
        return hand

    hand_without_joker = hand.replace("J", "")
    cards_with_max_count = [
        card for card in hand_without_joker
        if hand_without_joker.count(card) == max(hand_without_joker.count(card) for card in hand)
    ]
    if not cards_with_max_count:
        return hand
    
    max_card = max(cards_with_max_count, key=lambda card: CARD_STRENGTH_ORDER2.index(card))
    # print(hand, hand + max_card*jokers_count)
    return hand.replace("J", max_card)


def is_better2(hand1_composed, hand2_composed):
    CARD_STRENGTH_ORDER = CARD_STRENGTH_ORDER2
    hand1 = hand1_composed[0]
    hand2 = hand2_composed[0]
    modified_hand1 = modify_hand(hand1)
    modified_hand2 = modify_hand(hand2)
    counts1 = set(modified_hand1.count(card) for card in modified_hand1)
    counts2 = set(modified_hand2.count(card) for card in modified_hand2)
    for count in range(5, 0, -1):
        if count not in counts1 and count not in counts2:
            continue
        if count not in counts2:
            return True
        if count not in counts1:
            return False
        pairs_count1 = len([card for card in modified_hand1 if modified_hand1.count(card) == 2]) 
        pairs_count2 = len([card for card in modified_hand2 if modified_hand2.count(card) == 2]) 
        if pairs_count1 != pairs_count2:
            return pairs_count1 > pairs_count2

    # Same type now
    for card1, card2 in zip(hand1, hand2):
        card1_ord = CARD_STRENGTH_ORDER.index(card1)
        card2_ord = CARD_STRENGTH_ORDER.index(card2)
        if card1_ord != card2_ord:
            return card1_ord > card2_ord


def part1(_in):
    return sum(
        (i+1)*hand[1]
        for i, hand in enumerate(
            sorted(_in, key=cmp_to_key(lambda a, b: 1 if is_better(a, b) else -1))
        )
    )


def part2(_in):
    return sum(
        (i+1)*hand[1]
        for i, hand in enumerate(
            sorted(_in, key=cmp_to_key(lambda a, b: 1 if is_better2(a, b) else -1))
        )
    )


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
