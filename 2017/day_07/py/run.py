#! /usr/bin/python3

import sys, os, time
from typing import Counter, Dict, List, Tuple
import re
from functools import reduce


def part1(records: Dict[str, Tuple[ int, List[str]]]) -> str:
    allChildren: List[str] = list(reduce(lambda soFar, children: [ *soFar, *children[1] ], records.values(), []))
    for name in records.keys():
        if name not in allChildren:
            return name
    raise Exception("Top not found")


def part2(records: Dict[str, Tuple[ int, List[str]]]):
    combinedWeights: Dict[str, int] = {}
    while len(combinedWeights) != len(records):
        for name, (weight, children) in records.items():
            if name in combinedWeights:
                continue
            if not children:
                combinedWeights[name] = weight
                continue
            if all(child in combinedWeights for child in children):
                combinedWeights[name] = reduce(lambda soFar, child: soFar + combinedWeights[child], children, weight)
    
    currentTower = records[part1(records)]
    weightDifference = 0
    while True:
        weight, children = currentTower
        weightCounts = Counter([ combinedWeights[child] for child in children ])
        if len(weightCounts) == 1:
            return weight + weightDifference
        singleWeight: int = next(k for k, v in weightCounts.items() if v == 1)
        weightDifference = next(k for k, v in weightCounts.items() if v > 1) - singleWeight
        currentTower = records[next(child for child in currentTower[1] if combinedWeights[child] == singleWeight)]


lineRegex = re.compile(r"^(?P<name>[a-z]+)\s\((?P<weight>\d+)\)(?P<children>.*)")
def parseLine(line: str) -> Tuple[str, int, List[str]]:
    match = lineRegex.match(line.strip())
    if match:
        chilren = [ child for child in match.group("children").replace("->", "").strip().split(", ")  if child ]
        return match.group("name"), int(match.group("weight")), chilren
    else:
        raise Exception("Bad format", line)
    
    
def getInput(filePath: str) -> Dict[str, Tuple[ int, List[str]]]:
    if not os.path.isfile(filePath):
        raise FileNotFoundError(filePath)
    
    with open(filePath, "r") as file:
        return { name: (weight, children) for name, weight, children in map(parseLine, file.readlines()) }
            

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