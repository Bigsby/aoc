#! /usr/bin/python3

import sys, os, time
import re
from enum import Enum
from typing import Dict, List, Tuple


class Direction(Enum):
    Increment = "inc"
    Decrement = "dec"


class Operator(Enum):
    Equal = "=="
    NotEqual = "!="
    LessThan = "<"
    GreaterThan = ">"
    LessOrEqual = "<="
    GreatherOrEqual = ">="


Instruction = Tuple[str,str,Direction,int,Operator,int]


def isConditionValid(source: int, operator: Operator, value: int) -> bool:
    if operator == Operator.Equal:
        return source == value
    if operator == Operator.NotEqual:
        return source != value
    if operator == Operator.LessThan:
        return source < value
    if operator == Operator.GreaterThan:
        return source > value
    if operator == Operator.LessOrEqual:
        return source <= value
    if operator == Operator.GreatherOrEqual:
        return source >= value
    raise Exception("Unknown operator", operator)


def runInstructions(instructions: List[Instruction], returnFinal: bool) -> int:
    memory: Dict[str,int] = {}
    maxValue = 0
    for target, source, direction, amount, operator, value in instructions:
        sourceValue = memory[source] if source in memory else 0
        if not isConditionValid(sourceValue, operator, value):
            continue
        if target not in memory:
            memory[target] = 0
        memory[target] += amount * (1 if direction == Direction.Increment else -1)
        maxValue = max(maxValue, memory[target])
    return maxValue if returnFinal else max(memory.values())


def part1(instructions: List[Instruction]) -> int:
    return runInstructions(instructions, False)


def part2(instructions: List[Instruction]) -> int:
    return runInstructions(instructions, True)


lineRegex = re.compile(r"^(?P<target>[a-z]+)\s(?P<direction>inc|dec)\s(?P<amount>-?\d+)\sif\s(?P<source>[a-z]+)\s(?P<operator>==|!=|>=|<=|>|<)\s(?P<value>-?\d+)$")
def parseLine(line: str)  -> Instruction:
    match = lineRegex.match(line)
    if match:
        return match.group("target"), match.group("source"), Direction(match.group("direction")), int(match.group("amount")), Operator(match.group("operator")), int(match.group("value"))
    raise Exception("Bad format", line)


def getInput(filePath: str) -> List[Instruction]:
    if not os.path.isfile(filePath):
        raise FileNotFoundError(filePath)
    
    with open(filePath, "r") as file:
        return [ parseLine(line) for line in file.readlines() ]


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
    print(f"P1 time: {middle - start:.7f}")
    print(f"P2 time: {end - middle:.7f}")


if __name__ == "__main__":
    main()