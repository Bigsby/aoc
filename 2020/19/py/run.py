#! /usr/bin/python3

import sys
import os
import time
import re
from enum import Enum
from typing import Dict, List, Tuple


class RuleType(Enum):
    Letter = 0
    Set = 1


letterRegex = re.compile(r"^\"(?P<letter>a|b)\"$")


class Rule():
    def __init__(self, number: str, definition: str):
        match = letterRegex.match(definition)
        self.number = int(number)
        if match:
            self.type = RuleType.Letter
            self.letter = match.group("letter")
        else:
            self.type = RuleType.Set
            self.sets: List[List[int]] = []
            for set in definition.split("|"):
                self.sets.append(
                    list(map(lambda rule: int(rule), set.strip().split(" "))))


def generateRegex(rules: Dict[int, Rule], ruleNumber: int) -> str:
    rule = rules[ruleNumber]
    if rule.type == RuleType.Letter:
        return rule.letter
    else:
        return "(?:" + "|".join("".join(generateRegex(rules, innerNumber) for innerNumber in ruleSet) for ruleSet in rule.sets) + ")"


def isInnerMatch(rule: str, message: str, position: int) -> Tuple[bool, int]:
    match = re.match(rule, message[position:])
    if match:
        return True, position + match.end()
    return False, position


def isMatch(firstRule: str, secondRule: str, message: str) -> bool:
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


def solve(puzzleInput: Tuple[Dict[int, Rule], List[str]]) -> Tuple[int, int]:
    rules, messages = puzzleInput
    rule0 = generateRegex(rules, 0)
    rule42 = generateRegex(rules, 42)
    rule31 = generateRegex(rules, 31)
    return (
        sum(1 for message in messages if re.fullmatch(rule0, message)),
        sum(1 for message in messages if isMatch(rule42, rule31, message))
    )


ruleRegex = re.compile(r"(?P<number>^\d+):\s(?P<rule>.+)$")


def getInput(filePath: str) -> Tuple[Dict[int, Rule], List[str]]:
    if not os.path.isfile(filePath):
        raise FileNotFoundError(filePath)

    with open(filePath, "r") as file:
        rules: Dict[int, Rule] = {}
        messages: List[str] = []
        for line in file.readlines():
            if line.strip() != "":
                match = ruleRegex.match(line)
                if match:
                    rules[int(match.group("number"))] = Rule(
                        match.group("number"), match.group("rule"))
                else:
                    messages.append(line.strip())
        return rules, messages


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
