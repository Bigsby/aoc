import sys, os, re
from enum import Enum


ruleRegex = re.compile(r"(?P<number>^\d+):\s(?P<rule>.+)$")
letterRegex = re.compile(r"^\"(?P<letter>a|b)\"$")


class RuleType(Enum):
    Letter = 0
    Set = 1


class Rule():
    def __init__(self, number, definition):
        match = letterRegex.match(definition)
        self.number = int(number)
        self.solutions = []
        if match:
            self.type = RuleType.Letter
            self.letter = definition.strip("\"")
            self.solutions.append(self.letter)
        else:
            self.type = RuleType.Set
            self.sets = []
            for set in definition.split("|"):
                self.sets.append(list(map(lambda rule: int(rule), set.strip().split(" "))))
    def __str__(self):
        if self.type == RuleType.Set:
            return f"{self.number}: {self.type}: {self.sets}"
        else:
            return f"{self.number}: {self.type}: {self.solutions}"
    def __repr__(self):
        return self.__str__()

def generateRegex(rules, ruleNumber):
    rule = rules[ruleNumber]
    if rule.type == RuleType.Letter:
        return rule.letter
    elif len(rule.sets) == 1:
        return "".join(generateRegex(rules, innerNumber) for innerNumber in rule.sets[0])
    else:
        return "(?:" + "|".join("".join(generateRegex(rules, innerNumber) for innerNumber in ruleSet) for ruleSet in rule.sets) + ")"


def getInput():
    if len(sys.argv) != 2:
        print("Please, add input file path as parameter")
        sys.exit(1)

    filePath = sys.argv[1]
    if not os.path.isfile(filePath):
        print("File not found")
        sys.exit(1)

    with open(filePath, "r") as file:
        rules = {}
        messages = []
        for line in file.readlines():
            if line.strip() != "":
                match = ruleRegex.match(line)
                if match:
                    rules[int(match.group("number"))] = Rule(match.group("number"), match.group("rule"))
                else:
                    messages.append(line.strip())

        return rules, messages
