#! /usr/bin/python3

import sys, os, time
import re
from functools import reduce


forbidenPairs = [ "ab", "cd", "pq", "xy" ]
vowelRegex = re.compile("[aeiou]")
repeatRegex = re.compile("(.)\\1{1,}")
def isWordNice(word):
    for pair in forbidenPairs:
        if pair in word:
            return False
    return len(vowelRegex.findall(word)) > 2 and len(repeatRegex.findall(word)) != 0


def part1(puzzleInput):
    return reduce(lambda currentCount, word: currentCount + isWordNice(word), puzzleInput, 0)


def hasRepeatingPair(word):
    for pairStart in range(0, len(word) - 2):
        pairToTest = word[pairStart : pairStart + 2]
        startOfWord = word[0 : pairStart] 
        endOfWord = word[pairStart + 2 : len(word)]
        if pairToTest in startOfWord or pairToTest in endOfWord:
            return True
    return False


def hasRepeatingLetter(word):
    for index in range(0, len(word) - 2):
        if word[index] == word[index + 2]:
            return True
    return False


def part2(puzzleInput):
    return reduce(lambda currentCount, word: currentCount + (hasRepeatingPair(word) and hasRepeatingLetter(word)), puzzleInput, 0)


def getInput(filePath):
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
    print(f"P1 time: {middle - start:.8f}")
    print(f"P2 time: {end - middle:.8f}")


if __name__ == "__main__":
    main()