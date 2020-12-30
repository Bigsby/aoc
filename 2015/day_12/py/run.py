#! /usr/bin/python3

import sys, os, time
import re
import json
from functools import reduce


numberRegex = re.compile(r"(-?[\d]+)")
def part1(puzzleInput):
    return reduce(lambda soFar, match: soFar + int(match.group(1)), numberRegex.finditer(puzzleInput), 0)


def getTotal(obj):
    if isinstance(obj, dict):
        if any(filter(lambda key: obj[key] == "red", obj.keys())):
            return 0
        return reduce(lambda total, key: total + getTotal(obj[key]), obj.keys(), 0)
    if isinstance(obj, int):
        return int(obj)
    if isinstance(obj, list):
        return reduce(lambda total, item: total + getTotal(item), obj, 0)
    return 0


def part2(puzzleInput):
    report = json.loads(puzzleInput)
    return getTotal(report)


def getInput(filePath):
    if not os.path.isfile(filePath):
        raise FileNotFoundError(filePath)
    
    with open(filePath, "r") as file:
        return file.read().strip()


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