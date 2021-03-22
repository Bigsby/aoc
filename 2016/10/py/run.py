#! /usr/bin/python3

import sys
import os
import time
from typing import Dict, List, Tuple
import re
from functools import reduce

ValueInstruction = Tuple[int, int]
CompareInstruction = Tuple[str, int, str, int]
Instructions = Tuple[List[ValueInstruction], Dict[int, CompareInstruction]]


LOW_VALUE = 17
HIGH_VALUE = 61
TARGET_OUTPUTS = [0, 1, 2]


def solve(instructions: Instructions) -> Tuple[int, int]:
    value_instructions, compare_instructions = instructions
    bots: Dict[int, List[int]] = {}
    for bot, value in value_instructions:
        if bot not in bots:
            bots[bot] = []
        bots[bot].append(value)
    outputs: Dict[int, int] = {}
    part1_result: int = 0
    part2_result = 0
    while part1_result == 0 or part2_result == 0:
        bot: int = next(bot for bot, chips in bots.items() if len(chips) == 2)
        low_chip = min(bots[bot])
        high_chip = max(bots[bot])
        low_target, low, high_target, high = compare_instructions[bot]
        if low_target == "bot":
            if low not in bots:
                bots[low] = []
            bots[low].append(low_chip)
        else:
            outputs[low] = low_chip
        if high_target == "bot":
            if high not in bots:
                bots[high] = []
            bots[high].append(high_chip)
        else:
            outputs[high] = high_chip
        del bots[bot]
        if part1_result == 0 and low_chip == LOW_VALUE and high_chip == HIGH_VALUE:
            part1_result = bot
        if part2_result == 0 and all(output in outputs for output in TARGET_OUTPUTS):
            part2_result = reduce(
                lambda soFar, output: soFar * outputs[output], TARGET_OUTPUTS, 1)
    return (
        part1_result,
        part2_result
    )


value_regex = re.compile(r"^value\s(?P<value>\d+)\sgoes to bot\s(?P<bot>\d+)$")
compare_regex = re.compile(
    r"^bot\s(?P<bot>\d+)\sgives low to\s(?P<lowTarget>bot|output)\s(?P<low>\d+)\sand high to\s(?P<highTarget>bot|output)\s(?P<high>\d+)$")


def get_input(file_path: str) -> Instructions:
    if not os.path.isfile(file_path):
        raise FileNotFoundError(file_path)

    with open(file_path, "r") as file:
        value_instructions: List[ValueInstruction] = []
        compare_instructions: Dict[int, CompareInstruction] = {}
        for line in file.readlines():
            value_match = value_regex.match(line)
            if value_match:
                value_instructions.append(
                    (int(value_match.group("bot")), int(value_match.group("value"))))
            compare_match = compare_regex.match(line)
            if compare_match:
                compare_instructions[int(compare_match.group("bot"))] = \
                    (compare_match.group("lowTarget"),
                     int(compare_match.group("low")),
                     compare_match.group("highTarget"),
                     int(compare_match.group("high")))
        return value_instructions, compare_instructions


def main():
    if len(sys.argv) != 2:
        raise Exception("Please, add input file path as parameter")

    start = time.perf_counter()
    part1_result, part2_result = solve(get_input(sys.argv[1]))
    end = time.perf_counter()
    print("P1:", part1_result)
    print("P2:", part2_result)
    print()
    print(f"Time: {end - start:.7f}")


if __name__ == "__main__":
    main()
