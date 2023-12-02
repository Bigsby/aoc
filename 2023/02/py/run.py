#! /usr/bin/python3

import sys, os, time
from typing import Tuple, List, Dict


Draw = Tuple[int,int,int]
Game = Tuple[int,List[Draw]]

Input = List[Game]

MAX_BALLS: Draw = (12, 13, 14)

def is_game_possible(game: Game) -> bool:
    for draw in game[1]:
        for index in range(3):
            if draw[index] > MAX_BALLS[index]:
                return False
    return True


def part1(games: Input) -> int:
    sum = 0
    for game in games:
        if is_game_possible(game):
            sum += game[0]
    return sum


def get_powers(game: Game) -> int:
    mins = [0] * 3
    for  draw in game[1]:
        for index in range(3):
            mins[index] = max(mins[index], draw[index])
    return mins[0] * mins[1] * mins[2]



def part2(games: Input) -> int:
    return sum(get_powers(game) for game in games)


def solve(puzzle_input: Input) -> Tuple[int,int]:
    return (part1(puzzle_input), part2(puzzle_input))


def parse_draw(text: str) -> Draw:
    colours: Dict[str,int] = {
        "blue": 0,
        "red": 0,
        "green": 0
    }
    for draw in text.split(","):
        count, colour = draw.strip().split(" ")
        colours[colour] = int(count)
    return colours["red"], colours["green"], colours["blue"]


def parse_game(line: str) -> Game:
    separator_index = line.find(":")
    heading, draws_text = line[:separator_index], line[separator_index + 2:]
    return int(heading.split(" ")[1]), [ parse_draw(draw_text) for draw_text in draws_text.split(";") ]


def get_input(file_path: str) -> Input:
    if not os.path.isfile(file_path):
        raise FileNotFoundError(file_path)
    
    with open(file_path) as file:
        return [ parse_game(line.strip()) for line in file.readlines()]


def main():
    if len(sys.argv) != 2:
        raise Exception("Please, add input file path as parameter")

    start = time.perf_counter()
    part1_result, part2_result = solve(get_input(sys.argv[1]))
    end = time.perf_counter()
    print("P1:", part1_result)
    print("P2:", part2_result)
    print()
    print(f"Time: {end - start:.7f}")


if __name__ == "__main__":
    main()
