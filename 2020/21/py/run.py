#! /usr/bin/python3

import sys
import os
import time
from typing import Dict, List, Set, Tuple
import re
from functools import reduce


class Food():
    def __init__(self, ingredients: List[str], allergens: List[str]):
        self.ingredients = ingredients
        self.allergens = allergens

    def __str__(self):
        return " ".join(self.ingredients) + " (contains " + ", ".join(self.allergens) + ")"


def get_allergens(foods: List[Food]) -> Set[str]:
    allergens: Set[str] = set()
    for food in foods:
        for allergen in food.allergens:
            allergens.add(allergen)
    return allergens


def build_allergen_graph(foods: List[Food]) -> Dict[str, Set[str]]:
    allergens = get_allergens(foods)
    return {
        allergen: reduce(lambda so_far, food_allergens: so_far & food_allergens,
                         (set(food.ingredients) for food in foods if allergen in food.allergens))
        for allergen in allergens
    }


def part1(foods: List[Food], allergen_graph: Dict[str, Set[str]]) -> int:
    found_ingredients = reduce(lambda so_far, ingredients_for_allergen:
                               so_far | ingredients_for_allergen, allergen_graph.values())
    count = 0
    for food in foods:
        for ingredient in food.ingredients:
            count += ingredient not in found_ingredients
    return count


def part2(allergen_graph: Dict[str, Set[str]]) -> str:
    while any(len(ingredients) != 1 for ingredients in allergen_graph.values()):
        single_ingredient_allergens = [
            (allergen, next(iter(allergen_graph[allergen])))
            for allergen in allergen_graph if len(allergen_graph[allergen]) == 1
        ]
        for single_allergen, ingredient in single_ingredient_allergens:
            for allergen in allergen_graph:
                if allergen != single_allergen and ingredient in allergen_graph[allergen]:
                    allergen_graph[allergen].remove(ingredient)
    return ",".join(map(lambda k: next(iter(allergen_graph[k])), sorted(allergen_graph)))


def solve(foods: List[Food]) -> Tuple[int, str]:
    allergen_graph = build_allergen_graph(foods)
    return (
        part1(foods, allergen_graph),
        part2(allergen_graph)
    )


line_regex = re.compile(
    r"^(?P<ingredients>[^\(]+)\s\(contains\s(?P<allergens>[^\)]+)\)$")


def parse_line(line: str) -> Food:
    match = line_regex.match(line)
    if match:
        return Food(match.group("ingredients").split(" "), match.group("allergens").split(", "))
    raise Exception("Bad format", line)


def get_input(file_path: str) -> List[Food]:
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
