import sys, os, re

lineRegex = re.compile(r"^(?P<ingredients>[^\(]+)\s\(contains\s(?P<allergens>[^\)]+)\)$")

class Food():
    def __init__(self, ingredients, allergens):
        self.ingredients = ingredients
        self.allergens = allergens
    def __str__(self):
        return " ".join(self.ingredients) + " (contains " + ", ".join(self.allergens) + ")"


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
                yield Food(match.group("ingredients").split(" "), match.group("allergens").split(", "))
