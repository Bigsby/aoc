#! /usr/bin/python3

import sys, os, time
import re
from enum import Enum


class RuleType(Enum):
    Letter = 0
    Set = 1


letterRegex = re.compile(r"^\"(?P<letter>a|b)\"$")
class Rule():
    def __init__(self, number, definition):
        match = letterRegex.match(definition)
        self.number = int(number)
        if match:
            self.type = RuleType.Letter
            self.letter = match.group("letter")
        else:
            self.type = RuleType.Set
            self.sets = []
            for set in definition.split("|"):
                self.sets.append(list(map(lambda rule: int(rule), set.strip().split(" "))))


def generateRegex(rules, ruleNumber):
    rule = rules[ruleNumber]
    if rule.type == RuleType.Letter:
        return rule.letter
    elif len(rule.sets) == 1:
        return "".join(generateRegex(rules, innerNumber) for innerNumber in rule.sets[0])
    else:
        return "(?:" + "|".join("".join(generateRegex(rules, innerNumber) for innerNumber in ruleSet) for ruleSet in rule.sets) + ")"


def part1(puzzleInput):
    rules, messages = puzzleInput
    zeroRegex = generateRegex(rules, 0)
    return sum(1 for message in messages if re.fullmatch(zeroRegex, message))


def isInnerMatch(rule, message, position):
    match = re.match(rule, message[position:])
    if match:
        return True, position + match.end()
    return False, position

  
def isMatch(firstRule, secondRule, message):
    count = 0
    matched, position = isInnerMatch(firstRule, message, 0)
    while matched and position <= len(message):
        lastPosition = position
        for _ in range(count):
            matched, position = isInnerMatch(secondRule, message, position)
            if not matched:  
                position = lastPosition
                break
            elif position == len(message):  
                return True

        count += 1
        matched, position = isInnerMatch(firstRule, message, position)
    return False


def part2(puzzleInput):
    rules, messages = puzzleInput
    rule42 = generateRegex(rules, 42)
    rule31 = generateRegex(rules, 31)
    return sum([ 1 for message in messages if isMatch(rule42, rule31, message) ])


ruleRegex = re.compile(r"(?P<number>^\d+):\s(?P<rule>.+)$")
def getInput(filePath):
    if not os.path.isfile(filePath):
        raise FileNotFoundError(filePath)
    
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