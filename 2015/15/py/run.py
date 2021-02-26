#! /usr/bin/python3

import sys, os, time
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


def getValueForProperty(solution: Dict[str,int], entries: List[Entry], property: str) -> int:
    return reduce(lambda soFar, entry: soFar + getattr(entry, property) * solution[entry.name], entries, 0)


VALUE_PROPERTIES = [ "capacity", "durability", "flavor", "texture" ]
def findValueForSolution(solution: Dict[str,int], entries: List[Entry]) -> Tuple[int,int]:
    values: Dict[str,int] = {}
    for property in VALUE_PROPERTIES:
        values[property] = getValueForProperty(solution, entries, property)
    totalScore = reduce(lambda soFar, key: soFar * (values[key] if values[key] > 0 else 0), values, 1)
    calories = getValueForProperty(solution, entries, "calories")
    return totalScore, calories


def getPossibleCombinations(ingredients: List[str], totalSpoons: int) -> Iterable[Tuple[str,...]]:
    return combinations_with_replacement(ingredients, totalSpoons)


def createSolutionFromCombination(combination: Tuple[str,...], ingredients: List[str]) -> Dict[str,int]:
    return { ingredient: combination.count(ingredient) for ingredient in ingredients }


def getIngredientCombinations(entries: List[Entry], totalSpoons: int) -> Tuple[List[str],Iterable[Tuple[str,...]]]:
    ingredients = list(map(lambda entry: entry.name, entries))
    return ingredients, getPossibleCombinations(ingredients, totalSpoons)


def solve(entries: List[Entry]) -> Tuple[int,int]:
    ingredients, possibleCombinations = getIngredientCombinations(entries, 100)
    part1 = 0
    part2 = 0
    for combination in possibleCombinations:
        solution = createSolutionFromCombination(combination, ingredients)
        solutionResult, calories = findValueForSolution(solution, entries)
        part1 = max(part1, solutionResult)
        if calories == 500:
            part2 = max(part2, solutionResult)
    return part1, part2


lineRegex = re.compile(r"^(\w+):\scapacity\s(-?\d+),\sdurability\s(-?\d+),\sflavor\s(-?\d+),\stexture\s(-?\d+),\scalories\s(-?\d+)$")
def parseLine(line: str) -> Entry:
    match = lineRegex.match(line)
    if match:
        return Entry(*match.group(1, 2, 3, 4, 5, 6))
    raise Exception("Bad format", line)


def getInput(filePath: str) -> List[Entry]:
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