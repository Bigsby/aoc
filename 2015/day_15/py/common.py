import sys, os, re
from functools import reduce
from itertools import combinations_with_replacement


lineRegex = re.compile(r"^(\w+):\scapacity\s(-?\d+),\sdurability\s(-?\d+),\sflavor\s(-?\d+),\stexture\s(-?\d+),\scalories\s(-?\d+)$")
valueProperties = [ "capacity", "durability", "flavor", "texture" ]


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
 

def getInput():
    if len(sys.argv) != 2:
        print("Please, add input file path as parameter")
        sys.exit(1)

    filePath = sys.argv[1]
    if not os.path.isfile(filePath):
        print("File not found")
        sys.exit(1)

    with open(filePath, "r") as file:
        for line in file.readlines():
            match = lineRegex.match(line)
            if match:
                yield Entry(*match.group(1, 2, 3, 4, 5, 6))
