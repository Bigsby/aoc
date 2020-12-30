#! /usr/bin/python3

import sys, os, time
import re
from functools import reduce
from itertools import combinations_with_replacement


class Entry():
    def __init__(self, name, capacity, durability, flavor, texture, calories):
        self.name = name
        self.capacity = int(capacity)
        self.durability = int(durability)
        self.flavor = int(flavor)
        self.texture = int(texture)
        self.calories = int(calories)

    def __str__(self):
        return f"{self.name}: cap:{self.capacity} dur:{self.durability} fla:{self.flavor} tex:{self.texture} cal:{self.calories}"
    def __repr__(self):
        return self.__str__()


def getValueForProperty(solution, entries, property):
    return reduce(lambda soFar, entry: soFar + getattr(entry, property) * solution[entry.name], entries, 0)


valueProperties = [ "capacity", "durability", "flavor", "texture" ]
def findValueForSolution(solution, entries):
    values = {}
    for property in valueProperties:
        values[property] = getValueForProperty(solution, entries, property)
    totalScore = reduce(lambda soFar, key: soFar * (values[key] if values[key] > 0 else 1), values, 1)
    calories = getValueForProperty(solution, entries, "calories")
    return totalScore, calories


def getPossibleCombinations(ingredients, totalSpoons):
    return combinations_with_replacement(ingredients, totalSpoons)


def createSolutionFromCombination(combination, ingredients):
    return { ingredient: combination.count(ingredient) for ingredient in ingredients }


def getIngredientCombinations(entries, totalSpoons):
    totalSpoons = 100
    ingredients = list(map(lambda entry: entry.name, entries))
    return ingredients, getPossibleCombinations(ingredients, totalSpoons)


def getMaxValue(entries, requireCalories = False):
    ingredients, possibleCombinations = getIngredientCombinations(entries, 100)
    maxValue = 0
    for combination in possibleCombinations:
        solution = createSolutionFromCombination(combination, ingredients)
        solutionResult, calories = findValueForSolution(solution, entries)
        if not requireCalories or calories == 500:
            maxValue = max(maxValue, solutionResult)

    return maxValue


def part1(puzzleInput):
    return getMaxValue(puzzleInput)


def part2(puzzleInput):
    return getMaxValue(puzzleInput, True)


lineRegex = re.compile(r"^(\w+):\scapacity\s(-?\d+),\sdurability\s(-?\d+),\sflavor\s(-?\d+),\stexture\s(-?\d+),\scalories\s(-?\d+)$")
def parseLine(line):
    return Entry(*lineRegex.match(line).group(1, 2, 3, 4, 5, 6))


def getInput(filePath):
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
    print(f"P1 time: {middle - start:.8f}")
    print(f"P2 time: {end - middle:.8f}")


if __name__ == "__main__":
    main()