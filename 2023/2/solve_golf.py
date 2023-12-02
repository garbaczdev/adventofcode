with open("input.txt", "r") as f:
    rounds_per_game = [
        [
            {
                ball_str.split()[1]: int(ball_str.split()[0])
                for ball_str in round_str.split(", ")
            } for round_str in line.split(": ")[1].split("; ")
        ] for line in f.read().split("\n") if line.split()
    ]
print("Part 1:", sum(
    (index+1)*all(
        all(
            _round.get(color) is None or _round[color] <= max_count
            for color, max_count in [
                ("blue", 14), ("green", 13), ("red", 12)
            ]
        ) for _round in rounds
    ) for index, rounds in enumerate(rounds_per_game)
))
print("Part 2:", sum(
    min_colors["blue"]*min_colors["red"]*min_colors["green"]
    for min_colors in [
        {
            color: max(_round.get(color) or 0 for _round in rounds)
            for color in ["blue", "green", "red"]
        } for rounds in rounds_per_game
    ]
))

