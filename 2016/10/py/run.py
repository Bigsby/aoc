#! /usr/bin/python3

import sys, os, time
from typing import Dict, List, Tuple
import re
from functools import reduce

ValueInstruction = Tuple[int,int]
CompareInstruction = Tuple[str,int,str,int]
Instructions = Tuple[List[ValueInstruction],Dict[int,CompareInstruction]]


LOW_VALUE = 17
HIGH_VALUE = 61
TARGET_OUTPUTS = [ 0, 1, 2 ]
def solve(instructions: Instructions) -> Tuple[int,int]:
    valueInstructions, compareInstructions = instructions
    bots: Dict[int, List[int]] = {}
    for bot, value in valueInstructions:
        if bot not in bots:
            bots[bot] = []
        bots[bot].append(value)
    outputs: Dict[int,int] = {}
    part1Result = 0
    part2Result = 0
    while part1Result == 0 or part2Result == 0:
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
        if part1Result == 0 and lowChip == LOW_VALUE and highChip == HIGH_VALUE:
            part1Result = bot
        if part2Result == 0 and all(output in outputs for output in TARGET_OUTPUTS):
            part2Result = reduce(lambda soFar, output: soFar * outputs[output], TARGET_OUTPUTS, 1)
    return (
        part1Result, 
        part2Result
    )


valueRegex = re.compile(r"^value\s(?P<value>\d+)\sgoes to bot\s(?P<bot>\d+)$")
compareRegex = re.compile(r"^bot\s(?P<bot>\d+)\sgives low to\s(?P<lowTarget>bot|output)\s(?P<low>\d+)\sand high to\s(?P<highTarget>bot|output)\s(?P<high>\d+)$")
def getInput(filePath: str) -> Instructions:
    if not os.path.isfile(filePath):
        raise FileNotFoundError(filePath)
    
    with open(filePath, "r") as file:
        valueInstructions: List[ValueInstruction] = []
        compareInstructions: Dict[int,CompareInstruction] = {}
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

    start = time.perf_counter()
    part1Result, part2Result = solve(getInput(sys.argv[1]))
    end = time.perf_counter()
    print("P1:", part1Result)
    print("P2:", part2Result)
    print()
    print(f"Time: {end - start:.7f}")


if __name__ == "__main__":
    main()