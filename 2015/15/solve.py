#!/usr/bin/env python3
from sys import argv
from datetime import datetime

from functools import reduce


def calculate_score(ingredients: list[dict], quanities: list[int]) -> int:
    properties = [
        sum(
            ingredient[key]*quanities[index]
            for index, ingredient in enumerate(ingredients)
        )
        for key, value in ingredients[0].items()
        if key != "calories"
    ]
    
    if any(property <= 0 for property in properties):
        return 0
    
    return reduce(lambda x,y: x*y, properties)


def get_possible_quanities(number_of_recipes: int, total_quanity: int) -> list[int]:
    quanities = list()

    def iterate_quanities(current_quanities: list[int]) -> None:

        max_sum = total_quanity - sum(current_quanities)

        if len(current_quanities) == number_of_recipes:
            if max_sum == 0:
                quanities.append(current_quanities[:])
            return

        for quanity in range(max_sum + 1):
            current_quanities.append(quanity)
            iterate_quanities(current_quanities)
            current_quanities.pop()
        
    iterate_quanities([])
    return quanities


def is_recipe_right(ingredients: list[dict], quanities: list[int], calories: int) -> int:
    return sum(
        ingredient["calories"]*quanities[index]
        for index, ingredient in enumerate(ingredients)
    ) == calories


def get_input(filename: str):
    with open(filename, "r") as f:
        _in = [line.split(": ")[1] for line in f.read().split("\n") if line.split()]
        _in = [
            {
                attr_str.split()[0].strip() : int(attr_str.split()[1])
                for attr_str in line.split(", ")
            }
            for line in _in
        ]
         

    return _in


def part1(_in):
    recipes = [
        (quanities, calculate_score(_in, quanities))
        for quanities in get_possible_quanities(len(_in), 100)
    ]
    return max(recipes, key=lambda x: x[1])


def part2(_in):
    recipes = [
        (quanities, calculate_score(_in, quanities))
        for quanities in get_possible_quanities(len(_in), 100)
        if is_recipe_right(_in, quanities, 500)
    ]
    return max(recipes, key=lambda x: x[1])


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
