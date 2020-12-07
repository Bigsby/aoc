import sys, os, re


bagsRegex = re.compile("^(.*)\sbags contain\s(.*)$")
NO_BAGS = "no other bags."
innerBagsRegex = re.compile("^(\d+)\s(.*)\sbags?$")


class InnerBagRule():
    def __init__(self, color, quantity):
        self.color = color
        self.quantity = int(quantity)
    def __str__(self):
        return f"{self.quantity} {self.color}"
    def __repr__(self):
        return self.__str__()


class BagRule():
    def __init__(self, color, innerRules):
        self.color = color
        self.innerRules = list(innerRules)
    def __str__(self):
        return f"{self.color} -> {self.innerRules}"


def processInnerRules(text):
    if text == NO_BAGS:
        raise StopIteration
    rules = text.split(", ")
    for rule in rules:
        match = innerBagsRegex.match(rule)
        if match:
            yield InnerBagRule(match.group(2), match.group(1))


def processLine(line):
    match = bagsRegex.match(line)
    if match:
        return BagRule(match.group(1), processInnerRules(match.group(2).rstrip(".")))
    else:
        raise Exception("Bad format line:", line)


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
            yield processLine(line)
