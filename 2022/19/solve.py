#!/usr/bin/env python3
from sys import argv
from datetime import datetime

from copy import deepcopy


class Resources:
    def __init__(self, ore=0, clay=0, obsidian=0, geode=0):
        self.ore = ore
        self.clay = clay
        self.obsidian = obsidian
        self.geode = geode
    
    def __repr__(self) -> str:
        return f"Resources(or={self.ore}, c={self.clay}, ob={self.obsidian}, g={self.geode})"

    def add(self, r) -> None:
        self.ore += r.ore
        self.clay += r.clay
        self.obsidian += r.obsidian
        self.geode += r.geode

    def is_sufficient(self, r) -> bool:
        return r.ore >= self.ore and r.clay >= self.clay and r.obsidian >= self.obsidian


class Blueprint:
    def __init__(self, rules_str: str):
        rules = [rule.split() for rule in rules_str.split(".")]

        self.ore_robot_cost = Resources(
            ore=int(rules[0][-2])
        )
        self.clay_robot_cost = Resources(
            ore=int(rules[1][-2])
        )
        self.obsidian_robot_cost = Resources(
            ore=int(rules[2][-5]),
            clay=int(rules[2][-2])
        )
        self.geode_robot_cost = Resources(
            ore=int(rules[3][-5]),
            obsidian=int(rules[3][-2])
        )

    def __repr__(self) -> str:
        return f"Blueprint(or_r={self.ore_robot_cost}, c_r={self.clay_robot_cost}, ob_r={self.obsidian_robot_cost}, g_r={self.geode_robot_cost})"



class Mine:
    def __init__(self, bp: Blueprint, res: Resources = Resources(), robots: Resources = Resources(ore=1)):
        self.bp = bp
        self.res = res
        self.robots = robots

    def __repr__(self) -> str:
        return f"Mine(bp={self.bp}, res={self.res}, robots={self.robots})"

    def get_possible_mines(self) -> list:
        possible_mines = [self]

        if self.bp.ore_robot_cost.is_sufficient(self.res):
            new_mine = deepcopy(self)
            new_mine.robots.ore += 1
            possible_mines.append(new_mine)

        if self.bp.clay_robot_cost.is_sufficient(self.res):
            new_mine = deepcopy(self)
            new_mine.robots.clay += 1
            possible_mines.append(new_mine)

        if self.bp.obsidian_robot_cost.is_sufficient(self.res):
            new_mine = deepcopy(self)
            new_mine.robots.obsidian += 1
            possible_mines.append(new_mine)

        if self.bp.geode_robot_cost.is_sufficient(self.res):
            new_mine = deepcopy(self)
            new_mine.robots.geode += 1
            possible_mines.append(new_mine)


        for mine in possible_mines:
            mine.res.add(self.robots)

        return possible_mines


def best_mine_search(mine: Mine, minutes: int) -> int:

    max_geodes = -1

    def wrapped(mine: Mine, minutes: int) -> int:

        nonlocal max_geodes

        if minutes <= 0:

            if mine.res.geode > max_geodes:
                max_geodes = mine.res.geode
            return
        
        possible_mines = mine.get_possible_mines()

        for possible_mine in possible_mines:
            wrapped(possible_mine, minutes-1)


    wrapped(mine, minutes)

    return max_geodes


def get_input(filename: str):
    with open(filename, "r") as f:
        lines = [line for line in f.read().split("\n") if line.split()]
        _in = {
            int(line.split(":")[0].split()[1]) : Blueprint(line.split(":")[1].strip())
            for line in lines
        }

    return _in


def part1(_in):
    mine = Mine(_in[1])
    max_geodes = best_mine_search(mine, 19)
    print(max_geodes)
    return max_geodes


def part2(_in):
    pass


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
