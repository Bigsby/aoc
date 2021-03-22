#! /usr/bin/python3

import sys
import os
import time
import re
from typing import Dict, Iterable, List, Tuple
from functools import reduce
from itertools import combinations_with_replacement


class Entry():
    def __init__(self, name: str, capacity: str, durability: str, flavor: str, texture: str, calories: str):
        self.name = name
        self.capacity = int(capacity)
        self.durability = int(durability)
        self.flavor = int(flavor)
        self.texture = int(texture)
        self.calories = int(calories)


def get_value_for_property(solution: Dict[str, int], entries: List[Entry], property: str) -> int:
    return reduce(lambda soFar, entry: soFar + getattr(entry, property) * solution[entry.name], entries, 0)


VALUE_PROPERTIES = ["capacity", "durability", "flavor", "texture"]


def find_value_for_solution(solution: Dict[str, int], entries: List[Entry]) -> Tuple[int, int]:
    values: List[int] = []
    for property in VALUE_PROPERTIES:
        values.append(get_value_for_property(solution, entries, property))
    total_score = reduce(lambda soFar, value: soFar *
                         (value if value > 0 else 0), values, 1)
    calories = get_value_for_property(solution, entries, "calories")
    return total_score, calories


def get_possible_combinations(ingredients: List[str], total_spoons: int) -> Iterable[Tuple[str, ...]]:
    return combinations_with_replacement(ingredients, total_spoons)


def create_solution_from_combination(combination: Tuple[str, ...], ingredients: List[str]) -> Dict[str, int]:
    return {ingredient: combination.count(ingredient) for ingredient in ingredients}


def get_ingredient_combinations(entries: List[Entry], totalSpoons: int) -> Tuple[List[str], Iterable[Tuple[str, ...]]]:
    ingredients = list(map(lambda entry: entry.name, entries))
    return ingredients, get_possible_combinations(ingredients, totalSpoons)


def solve(entries: List[Entry]) -> Tuple[int, int]:
    ingredients, possible_combinations = get_ingredient_combinations(
        entries, 100)
    part1 = 0
    part2 = 0
    for combination in possible_combinations:
        solution = create_solution_from_combination(combination, ingredients)
        solution_result, calories = find_value_for_solution(solution, entries)
        part1 = max(part1, solution_result)
        if calories == 500:
            part2 = max(part2, solution_result)
    return part1, part2


line_regex = re.compile(
    r"^(\w+):\scapacity\s(-?\d+),\sdurability\s(-?\d+),\sflavor\s(-?\d+),\stexture\s(-?\d+),\scalories\s(-?\d+)$")


def parse_line(line: str) -> Entry:
    match = line_regex.match(line)
    if match:
        return Entry(*match.group(1, 2, 3, 4, 5, 6))
    raise Exception("Bad format", line)


def get_input(file_path: str) -> List[Entry]:
    if not os.path.isfile(file_path):
        raise FileNotFoundError(file_path)

    with open(file_path, "r") as file:
        return [parse_line(line) for line in file.readlines()]


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
