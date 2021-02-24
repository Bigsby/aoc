#! /usr/bin/python3

import sys, os, time
from typing import List
import re


FORBIDEN_PAIRS = [ "ab", "cd", "pq", "xy" ]
vowelRegex = re.compile("[aeiou]")
repeatRegex = re.compile("(.)\\1{1,}")
def isWordNice(word: str) -> bool:
    return all(map(lambda pair: pair not in word, FORBIDEN_PAIRS)) \
        and len(vowelRegex.findall(word)) > 2 \
        and len(repeatRegex.findall(word)) != 0


def part1(words: List[str]) -> int:
    return len(list(filter(isWordNice, words)))


def hasRepeatingPair(word: str) -> bool:
    for pairStart in range(len(word) - 2):
        pairToTest = word[pairStart : pairStart + 2]
        if pairToTest in word[:pairStart] or pairToTest in word[pairStart + 2:]:
            return True
    return False


def hasRepeatingLetter(word: str) -> bool:
    for index in range(len(word) - 2):
        if word[index] == word[index + 2]:
            return True
    return False


def part2(words: List[str]) -> int:
    return len(list(filter(lambda word: hasRepeatingPair(word) and hasRepeatingLetter(word), words)))


def getInput(filePath: str) -> List[str]:
    if not os.path.isfile(filePath):
        raise FileNotFoundError(filePath)
    
    with open(filePath, "r") as file:
        return [ line.strip() for line in file.readlines() ]


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