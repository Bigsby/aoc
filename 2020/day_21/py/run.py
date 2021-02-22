#! /usr/bin/python3

import sys, os, time
from typing import Dict, List, Set
import re
from functools import reduce


class Food():
    def __init__(self, ingredients: List[str], allergens: List[str]):
        self.ingredients = ingredients
        self.allergens = allergens

    def __str__(self):
        return " ".join(self.ingredients) + " (contains " + ", ".join(self.allergens) + ")"


def getAllergens(foods: List[Food]) -> Set[str]:
    allergens = set()
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


def part1(foods: List[Food]) -> int:
    allergenGraph = buildAllergenGraph(foods)
    foundIngredients = reduce(lambda soFar, ingredientsForAllergen: \
        soFar | ingredientsForAllergen, (graph for _, graph in allergenGraph.items()))
    count = 0
    for food in foods:
        for ingredient in food.ingredients:
            count += ingredient not in foundIngredients
    return count


def part2(foods: List[Food]) -> str:
    allergenGraph = buildAllergenGraph(foods)
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

    puzzleInput = getInput(sys.argv[1])
    start = time.perf_counter()
    part1Result = part1(puzzleInput)
    middle = time.perf_counter()
    part2Result = part2(puzzleInput)
    end = time.perf_counter()
    print("P1:", part1Result)
    print("P2:", part2Result)
    print()
    print(f"P1 time: {middle - start:.7f}")
    print(f"P2 time: {end - middle:.7f}")


if __name__ == "__main__":
    main()