#! /usr/bin/python3

import sys, os, time
from typing import Tuple, Dict, List
from collections import Counter, defaultdict

Input = [str, Dict[str,str]]


def count_insertions(puzzle_input: Input, steps: int) -> int:
    polymer, rules = puzzle_input
    pair_occurences = defaultdict(int)
    for index in range(len(polymer) - 1):
        pair_occurences[polymer[index:index + 2]] += 1
    for _ in range(steps):
        new_pair_occurences = defaultdict(int)
        for pair in pair_occurences:
            first, second = pair
            new_letter = rules[pair]
            this_pair_occurences = pair_occurences[pair]
            new_pair_occurences[first + new_letter] += this_pair_occurences
            new_pair_occurences[new_letter + second] += this_pair_occurences
        pair_occurences = new_pair_occurences
    distinct_occurences = defaultdict(int)
    for pair, occurences in pair_occurences.items():
        first, secode = pair
        distinct_occurences[first] += occurences
    distinct_occurences[polymer[-1]] += 1
    maximum = max(distinct_occurences, key=distinct_occurences.get)
    minimum = min(distinct_occurences, key=distinct_occurences.get)
    return distinct_occurences[maximum] - distinct_occurences[minimum]


def solve(puzzle_input: Input) -> Tuple[int,int]:
    return (count_insertions(puzzle_input, 10), count_insertions(puzzle_input, 40))


def get_input(file_path: str) -> Input:
    if not os.path.isfile(file_path):
        raise FileNotFoundError(file_path)
    
    with open(file_path) as file:
        polymer = ""
        rules = dict()
        for line in file.readlines():
            if not polymer:
                polymer = line.strip()
                continue
            if line == "\n":
                continue
            split = line.strip().split(" -> ")
            rules[split[0]] = split[1]
        return polymer, rules


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
