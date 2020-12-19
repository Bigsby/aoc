import sys, os, re
from enum import Enum


ruleRegex = re.compile(r"(?P<number>^\d):\s(?P<rule>.+)$")
letterRegex = re.compile(r"^\"(?P<letter>a|b)\"$")


class RuleType(Enum):
    Letter = 0
    Set = 1


class Rule():
    def __init__(self, definition):
        match = letterRegex.match(definition)
        if match:
            self.type = RuleType.Letter
            self.letter = match.group("letter")
        else:
            self.type = RuleType.Set
            self.sets = []
            for set in definition.split("|"):
                self.sets.append(list(map(lambda rule: int(rule), set.strip().split(" "))))
    def __str__(self):
        if self.type == RuleType.Set:
            return f"{self.type}: {self.sets}"
        else:
            return f"{self.type}: {self.letter}"


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
                    rules[match.group("number")] = Rule(match.group("rule"))
                else:
                    messages.append(line.strip())

        return rules, messages
