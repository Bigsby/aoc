#! /usr/bin/python3

import sys, os, time
from typing import Dict, List, Set, Tuple
import re
from functools import reduce


class Food():
    def __init__(self, ingredients: List[str], allergens: List[str]):
        self.ingredients = ingredients
        self.allergens = allergens

    def __str__(self):
        return " ".join(self.ingredients) + " (contains " + ", ".join(self.allergens) + ")"


def getAllergens(foods: List[Food]) -> Set[str]:
    allergens: Set[str] = set()
    for food in foods:
        for allergen in food.allergens:
            allergens.add(allergen)
    return allergens


def buildAllergenGraph(foods: List[Food]) -> Dict[str,Set[str]]:
    allergens = getAllergens(foods)
    return {
        allergen: reduce(lambda soFar, foodAllergens: soFar & foodAllergens, \
            (set(food.ingredients) for food in foods if allergen in food.allergens)) \
            for allergen in allergens
    }


def part1(foods: List[Food], allergenGraph: Dict[str,Set[str]]) -> int:
    foundIngredients = reduce(lambda soFar, ingredientsForAllergen: \
        soFar | ingredientsForAllergen, (graph for _, graph in allergenGraph.items()))
    count = 0
    for food in foods:
        for ingredient in food.ingredients:
            count += ingredient not in foundIngredients
    return count


def part2(allergenGraph: Dict[str,Set[str]]) -> str:
    while any(len(ingredients) != 1 for ingredients in allergenGraph.values()):
        singleIngredientAllergens = [  
            (allergen, next(iter(allergenGraph[allergen]))) \
            for allergen in allergenGraph if len(allergenGraph[allergen]) == 1 
        ]
        for singleAllergen, ingredient in singleIngredientAllergens:
            for allergen in allergenGraph:
                if allergen != singleAllergen and ingredient in allergenGraph[allergen]:
                    allergenGraph[allergen].remove(ingredient)
    return ",".join(map(lambda k: next(iter(allergenGraph[k])), sorted(allergenGraph)))


def solve(foods: List[Food]) -> Tuple[int,str]:
    allergenGraph = buildAllergenGraph(foods)
    return (
        part1(foods, allergenGraph),
        part2(allergenGraph)
    )


lineRegex = re.compile(r"^(?P<ingredients>[^\(]+)\s\(contains\s(?P<allergens>[^\)]+)\)$")
def parseLine(line: str) -> Food:
    match = lineRegex.match(line)
    if match:
        return Food(match.group("ingredients").split(" "), match.group("allergens").split(", "))
    raise Exception("Bad format", line)


def getInput(filePath: str) -> List[Food]:
    if not os.path.isfile(filePath):
        raise FileNotFoundError(filePath)
    
    with open(filePath, "r") as file:
        return [ parseLine(line) for line in file.readlines() ]


def main():
    if len(sys.argv) != 2:
        raise Exception("Please, add input file path as parameter")

    start = time.perf_counter()
    part1Result, part2Result = solve(getInput(sys.argv[1]))
    end = time.perf_counter()
    print("P1:", part1Result)
    print("P2:", part2Result)
    print()
    print(f"Time: {end - start:.7f}")


if __name__ == "__main__":
    main()