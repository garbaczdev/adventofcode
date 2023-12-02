#!/usr/bin/env python3
from sys import argv
from datetime import datetime


def get_input(filename: str):
    with open(filename, "r") as f:
        _in = [line for line in f.read().split("\n") if line.split()]
        _in = [
            line.split(": ")[1]
            for line in _in
        ]

    return _in


def part1(_in):
    games = []
    for line in _in:
        valid_game = True
        for game in line.split("; "):
            balls = {
                ball.split()[1]: int(ball.split()[0]) for ball in game.split(", ")
            }
            if any([
                balls.get("blue") is not None and balls["blue"] > 14,
                balls.get("red") is not None and balls["red"] > 12,
                balls.get("green") is not None and balls["green"] > 13
            ]):
                valid_game = False
                break

        games.append(valid_game)
    
    return sum(
        index+1 for index, game in enumerate(games) if game
    )
                  
    return games
            


def part2(_in):
    score = 0
    for line in _in:
        game_balls = []
        for game in line.split("; "):
            balls = {
                ball.split()[1]: int(ball.split()[0]) for ball in game.split(", ")
            }
            game_balls.append(balls)
        min_game_balls = {
            color: max(
                game_ball.get(color) if game_ball.get(color) is not None else 0 for game_ball in game_balls
            )
            for color in ["red", "green", "blue"]
        }
        score += min_game_balls["blue"] * min_game_balls["red"] * min_game_balls["green"]

    
    return score

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
