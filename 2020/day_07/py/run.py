#! /usr/bin/python3

import sys, os, time
import re


requiredColor = "shiny gold"


def getRulesContaining(color, rules):
    for ruleColor, innerRules in rules.items():
        if any(map(lambda innerRule: innerRule[0] == color, innerRules)):
            yield ruleColor 
            yield from getRulesContaining(ruleColor, rules)


def part1(puzzleInput):
    return len(set(getRulesContaining(requiredColor, puzzleInput)))
    

def getQuantityFromColor(color, rules):
    return sum(map(lambda innerRule: innerRule[1] * ( 1 + getQuantityFromColor(innerRule[0], rules)), rules[color]))


def part2(puzzleInput):
    return getQuantityFromColor(requiredColor, puzzleInput)


innerBagsRegex = re.compile("^(\d+)\s(.*)\sbags?$")
def processInnerRule(text):
    match = innerBagsRegex.match(text.strip())
    return (match.group(2), int(match.group(1)))


def processInnerRules(text):
    if text == "no other bags":
        return []
    return [ processInnerRule(innerText) for innerText in text.split(", ") ]


bagsRegex = re.compile("^(.*)\sbags contain\s(.*)$")
def processLine(line):
    match = bagsRegex.match(line)
    return (match.group(1), processInnerRules(match.group(2).rstrip(".")))


def getInput(filePath):
    if not os.path.isfile(filePath):
        raise FileNotFoundError(filePath)
    
    with open(filePath, "r") as file:
        return { color: innerRules for color, innerRules in [ processLine(line) for line in file.readlines() ] }


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