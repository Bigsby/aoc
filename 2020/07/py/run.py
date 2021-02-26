#! /usr/bin/python3

import sys, os, time
import re
from typing import Dict, Iterable, List, Tuple

Rule = Tuple[str,int]
Rules = Dict[str,List[Rule]]
REQUIRED_COLOR = "shiny gold"


def getRulesContaining(color: str, rules: Rules) -> Iterable[str]:
    for ruleColor, innerRules in rules.items():
        if any(map(lambda innerRule: innerRule[0] == color, innerRules)):
            yield ruleColor 
            yield from getRulesContaining(ruleColor, rules)


def getQuantityFromColor(color: str, rules: Rules) -> int:
    return sum(map(lambda innerRule: innerRule[1] * ( 1 + getQuantityFromColor(innerRule[0], rules)), rules[color]))


def solve(rules: Rules) -> Tuple[int,int]:
    return (
        len(set(getRulesContaining(REQUIRED_COLOR, rules))),
        getQuantityFromColor(REQUIRED_COLOR, rules)
    )


innerBagsRegex = re.compile(r"^(\d+)\s(.*)\sbags?$")
def processInnerRule(text: str) -> Rule:
    match = innerBagsRegex.match(text.strip())
    if match:
        return (match.group(2), int(match.group(1)))
    raise Exception("Bad format", text)


def processInnerRules(text: str) -> List[Rule] :
    if text == "no other bags":
        return []
    return [ processInnerRule(innerText) for innerText in text.split(", ") ]


bagsRegex = re.compile(r"^(.*)\sbags contain\s(.*)$")
def processLine(line: str) -> Tuple[str,List[Rule]]:
    match = bagsRegex.match(line)
    if match:
        return (match.group(1), processInnerRules(match.group(2).rstrip(".")))
    raise Exception("Bad format", line)


def getInput(filePath: str) -> Rules:
    if not os.path.isfile(filePath):
        raise FileNotFoundError(filePath)
    
    with open(filePath, "r") as file:
        return { color: innerRules for color, innerRules in [ processLine(line) for line in file.readlines() ] }


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