#! /usr/bin/python3

import sys, os, time


def part1(target: int):
    recipes = "37"
    elf1 = 0
    elf2 = 1
    while len(recipes) < target + 10:
        elf1Score = int(recipes[elf1])
        elf2Score = int(recipes[elf2])
        recipes += str(elf1Score + elf2Score)
        elf1 = (elf1 + elf1Score + 1) % len(recipes)
        elf2 = (elf2 + elf2Score + 1) % len(recipes)

    return recipes[target:target + 10]


def part2(target:int):
    scoreSequence = str(target)
    sequenceLength = len(scoreSequence)
    recipes = "37"
    elf1 = 0
    elf2 = 1
    while recipes[-sequenceLength:] != scoreSequence and recipes[-sequenceLength -1:-1] != scoreSequence:
        elf1Score = int(recipes[elf1])
        elf2Score = int(recipes[elf2])
        recipes += str(elf1Score + elf2Score)
        elf1 = (elf1 + elf1Score + 1) % len(recipes)
        elf2 = (elf2 + elf2Score + 1) % len(recipes)

    return recipes.index(scoreSequence)


def getInput(filePath: str) -> int:
    if not os.path.isfile(filePath):
        raise FileNotFoundError(filePath)
    
    with open(filePath, "r") as file:
        return int(file.read().strip())
            


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