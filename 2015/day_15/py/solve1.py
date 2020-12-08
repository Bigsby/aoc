#! /usr/bin/python3

from functools import reduce
from itertools import combinations_with_replacement
import json

from common import getInput


def findValueForSolution(solution, entries, properties):
    values = {}
    for prop in properties:
        values[prop] = reduce(lambda soFar, entry: soFar + getattr(entry, prop) * solution[entry.name], entries, 0)
    return reduce(lambda soFar, key: soFar * (values[key] if values[key] > 0 else 1), values, 1)


def createSolutionFromCombination(combination, ingredients):
    return { ingredient: combination.count(ingredient) for ingredient in ingredients }
    



def main():
    entries = list(getInput())
    totalSpoons = 100
    ingredients = list(map(lambda entry: entry.name, entries))
    properties = [ "capacity", "durability", "flavor", "texture" ]
    possibleCombinations = combinations_with_replacement(ingredients, totalSpoons)
    maxValue = 0
    for combination in possibleCombinations:
        solution = createSolutionFromCombination(combination, ingredients)
        solutionResult = findValueForSolution(solution, entries, properties)
        maxValue = max(maxValue, solutionResult)

    print("Highest score:", maxValue)


if __name__ == "__main__":
    main()
