#!/usr/bin/env python3
from sys import argv
from datetime import datetime

from math import ceil


class Player:
    def __init__(self, hit_points: int, damage: int, armor: int):
        self.hit_points = hit_points
        self.damage = damage
        self.armor = armor

    def __repr__(self) -> str:
        return f"Player(h={self.hit_points}, d={self.damage}, a={self.armor})"

    def copy(self):
        return Player(self.hit_points, self.damage, self.armor)
    
    def will_beat(self, other_player) -> bool:
        # print(self, other_player, self.get_kill_time(other_player), other_player.get_kill_time(self))
        return self.get_kill_time(other_player) <= other_player.get_kill_time(self)

    def get_kill_time(self, other_player) -> int:
        damage_dealt = self.damage - other_player.armor

        if damage_dealt < 1:
            damage_dealt = 1

        return ceil(other_player.hit_points / damage_dealt)


def get_input(filename: str):
    with open(filename, "r") as f:
        boss_params = [
            int(line.split(": ")[1]) 
            for line in f.read().split("\n") 
            if line.split()
        ]
    boss = Player(boss_params[0], boss_params[1], boss_params[2])

    with open("shop.txt", "r") as f:
        shop = {
            segment.split("\n")[0].split(": ")[0].lower(): {
                " ".join(line.split()[:-3]).lower(): {
                    "cost": int(line.split()[-3]),
                    "damage": int(line.split()[-2]),
                    "armor": int(line.split()[-1]),
                }
                for line in segment.split("\n")[1:]
                if line.split()
            }
            for segment in f.read().split("\n\n") 
            if segment.split()
        }

    return (boss, shop)


def get_sumed_attr(items: list[dict], attr: str):
    return sum(item[attr] for item in items)


def generate_possible_players(shop: dict) -> list[Player]:
    possible_players = list()
    for weapon, weapon_info in shop["weapons"].items():
        for armor, armor_info in shop["armor"].items():
            for ring1, ring1_info in shop["rings"].items():
                for ring2, ring2_info in shop["rings"].items():
                    if ring1 == ring2:
                        continue
                    items = [
                        weapon_info, 
                        armor_info, 
                        ring1_info, 
                        ring2_info
                    ]
                    cost = get_sumed_attr(items, "cost")
                    possible_players.append((Player(
                        100,
                        get_sumed_attr(items, "damage"),
                        get_sumed_attr(items, "armor")
                    ), (weapon, armor, ring1, ring2), cost))

    return possible_players


def part1(_in):
    boss, shop = _in
    boss = boss.copy()

    possible_players = generate_possible_players(shop)
    possible_players.sort(key=lambda x: x[-1])

    for player_data in possible_players:
        player, items, cost = player_data
        if player.will_beat(boss):
            return player_data

    return None


def part2(_in):
    boss, shop = _in
    boss = boss.copy()

    possible_players = generate_possible_players(shop)
    possible_players.sort(key=lambda x: x[-1], reverse=True)

    for player_data in possible_players:
        player, items, cost = player_data
        if not player.will_beat(boss):
            return player_data

    return None


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
