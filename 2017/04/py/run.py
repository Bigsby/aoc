#! /usr/bin/python3

import sys, os, time
from typing import Callable, List


def runTests(passphrases: List[List[str]], validationFunc: Callable[[List[str]],bool]) -> int:
    return sum(map(lambda passphrase: validationFunc(passphrase), passphrases))


def part1(passphrases: List[List[str]]) -> int:
    return runTests(passphrases, lambda passphrase: 
        not any(map(lambda word: passphrase.count(word) > 1, passphrase)))


def isAnagram(word1: str, word2: str) -> bool:
    return len(word1) == len(word2) and \
        all(map(lambda c: word1.count(c) == word2.count(c), word1))


def hasNoAnagram(passphrase: List[str]) -> bool:
    for index, word in enumerate(passphrase):
        for otherWord in passphrase[:index] + passphrase[index + 1:]:
            if isAnagram(word, otherWord):
                return False
    return True


def part2(passphrases: List[List[str]]) -> int:
    return runTests(passphrases, hasNoAnagram)


def getInput(filePath: str) -> List[List[str]]:
    if not os.path.isfile(filePath):
        raise FileNotFoundError(filePath)
    
    with open(filePath, "r") as file:
        return [ line.strip().split(" ") for line in file.readlines() ]


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