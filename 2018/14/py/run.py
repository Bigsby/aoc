#! /usr/bin/python3

import sys, os, time
from typing import Tuple


def solve(target: int) -> Tuple[str,int]:
    scoreSequence = str(target)
    sequenceLength = len(scoreSequence)
    recipes = "37"
    elf1 = 0
    elf2 = 1
    part1Result = ""
    while recipes[-sequenceLength:] != scoreSequence and recipes[-sequenceLength - 1:-1] != scoreSequence:
        elf1Score = int(recipes[elf1])
        elf2Score = int(recipes[elf2])
        recipes += str(elf1Score + elf2Score)
        elf1 = (elf1 + elf1Score + 1) % len(recipes)
        elf2 = (elf2 + elf2Score + 1) % len(recipes)
        if not part1Result and len(recipes) > target + 10:
            part1Result = recipes[target:target + 10]
    return part1Result, recipes.index(scoreSequence)


def getInput(filePath: str) -> int:
    if not os.path.isfile(filePath):
        raise FileNotFoundError(filePath)
    
    with open(filePath, "r") as file:
        return int(file.read().strip())    


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