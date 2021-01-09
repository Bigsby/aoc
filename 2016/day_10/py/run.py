#! /usr/bin/python3

import sys, os, time
from typing import Dict, List, Tuple
import re
from functools import reduce


LOW_VALUE = 17
HIGH_VALUE = 61
TARGET_OUTPUTS = [ 0, 1, 2 ]
def isComplete(test: int, bot: int, lowChip: int, highChip: int, outputs: Dict[int,int]):
    if test == 1:
        if lowChip == LOW_VALUE and highChip == HIGH_VALUE:
            return True, bot
        return False, -1
    else:
        if all(output in outputs for output in TARGET_OUTPUTS):
            return True, reduce(lambda soFar, output: soFar * outputs[output], TARGET_OUTPUTS, 1)
        return False, -1


def run(instructions: Tuple[List[Tuple[int,int]],Dict[int,Tuple[str,int,str,int]]], test: int) -> int:
    valueInstructions, compareInstructions = instructions
    bots: Dict[int, List[int]] = {}
    for bot, value in valueInstructions:
        if bot not in bots:
            bots[bot] = []
        bots[bot].append(value)
    outputs: Dict[int,int] = {}
    while True:
        bot = next(bot for bot, chips in bots.items() if len(chips) == 2)
        lowChip = min(bots[bot])
        highChip = max(bots[bot])
        lowTarget, low, highTarget, high = compareInstructions[bot]
        if lowTarget == "bot":
            if low not in bots:
                bots[low] = []
            bots[low].append(lowChip)
        else:
            outputs[low] = lowChip        
        if highTarget == "bot":
            if high not in bots:
                bots[high] = []
            bots[high].append(highChip)
        else:
            outputs[high] = highChip
        bots[bot].remove(lowChip)
        bots[bot].remove(highChip)

        complete, result = isComplete(test, bot, lowChip, highChip, outputs)
        if complete:
            return result


def part1(instructions: Tuple[List[Tuple[int,int]],Dict[int,Tuple[str,int,str,int]]]) -> int:
    return run(instructions, 1)


def part2(instructions: Tuple[List[Tuple[int,int]],Dict[int,Tuple[str,int,str,int]]]) -> int:
    return run(instructions, 2)


valueRegex = re.compile(r"^value\s(?P<value>\d+)\sgoes to bot\s(?P<bot>\d+)$")
compareRegex = re.compile(r"^bot\s(?P<bot>\d+)\sgives low to\s(?P<lowTarget>bot|output)\s(?P<low>\d+)\sand high to\s(?P<highTarget>bot|output)\s(?P<high>\d+)$")
def getInput(filePath: str) -> Tuple[List[Tuple[int,int]],Dict[int,Tuple[str,int,str,int]]]:
    if not os.path.isfile(filePath):
        raise FileNotFoundError(filePath)
    
    with open(filePath, "r") as file:
        valueInstructions: List[Tuple[int,int]] = []
        compareInstructions: Dict[int,Tuple[str,int,str,int]] = {}
        for line in file.readlines():
            valueMatch = valueRegex.match(line)
            if valueMatch:
                valueInstructions.append((int(valueMatch.group("bot")), int(valueMatch.group("value"))))
            compareMatch = compareRegex.match(line)
            if compareMatch:
                compareInstructions[int(compareMatch.group("bot"))] = \
                    (compareMatch.group("lowTarget"), \
                    int(compareMatch.group("low")), \
                    compareMatch.group("highTarget"), \
                    int(compareMatch.group("high")))
        return valueInstructions, compareInstructions


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