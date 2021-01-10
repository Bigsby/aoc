#! /usr/bin/python3

import sys, os, time
from typing import Any, Dict, List, Union
import re
import json
from functools import reduce

JSONType = Union[str, int, float, bool, None, Dict[str, Any], List[Any]]


numberRegex = re.compile(r"(-?[\d]+)")
def part1(puzzleInput: str):
    return reduce(lambda soFar, match: soFar + int(match.group(1)), numberRegex.finditer(puzzleInput), 0)


def getTotal(obj: JSONType) -> int:
    if isinstance(obj, dict):
        if any(filter(lambda value: value == "red", obj.values())):
            return 0
        return reduce(lambda total, value: total + getTotal(value), obj.values(), 0)
    if isinstance(obj, int):
        return int(obj)
    if isinstance(obj, list):
        return reduce(lambda total, item: total + getTotal(item), obj, 0)
    return 0


def part2(puzzleInput: str):
    report = json.loads(puzzleInput)
    return getTotal(report)


def getInput(filePath: str) -> str:
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