#! /usr/bin/python3

import sys, os, time
from typing import Callable, List, Tuple


def runTests(passphrases: List[List[str]], validationFunc: Callable[[List[str]],bool]) -> int:
    return sum(map(lambda passphrase: validationFunc(passphrase), passphrases))


def isAnagram(word1: str, word2: str) -> bool:
    return len(word1) == len(word2) and \
        all(map(lambda c: word1.count(c) == word2.count(c), word1))


def hasNoAnagram(passphrase: List[str]) -> bool:
    for index, word in enumerate(passphrase):
        for otherWord in passphrase[:index] + passphrase[index + 1:]:
            if isAnagram(word, otherWord):
                return False
    return True


def solve(passphrases: List[List[str]]) -> Tuple[int,int]:
    return (
        runTests(passphrases, lambda passphrase: 
            not any(map(lambda word: passphrase.count(word) > 1, passphrase))),
        runTests(passphrases, hasNoAnagram)
    )


def getInput(filePath: str) -> List[List[str]]:
    if not os.path.isfile(filePath):
        raise FileNotFoundError(filePath)
    
    with open(filePath, "r") as file:
        return [ line.strip().split(" ") for line in file.readlines() ]


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