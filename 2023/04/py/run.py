#! /usr/bin/python3

import sys, os, time
from typing import Tuple, List

Card = Tuple[int,List[int],List[int]]
Input = List[Card]


def solve(cards: Input) -> Tuple[int,int]:
    part1 = 0
    won: List[int] = [1] * len(cards)
    for index, card in enumerate(cards):
        matches = sum(1 if number in card[1] else 0 for number in card[2])
        if matches:
            part1 += 2 ** (matches - 1)
        for offset in range(matches):
            won[index + offset + 1] += won[index]
    return (part1, sum(won))


def parse_card(line: str) -> Card:
    header, numbers = line.split(":")
    winning, own = numbers.strip().split("|")
    return int(header.split()[-1]), [ int(value.strip()) for value in winning.split() ], [ int(value.strip()) for value in own.split() ]


def get_input(file_path: str) -> Input:
    if not os.path.isfile(file_path):
        raise FileNotFoundError(file_path)
    
    with open(file_path) as file:
        return [ parse_card(line.strip()) for line in file.readlines() ]


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
