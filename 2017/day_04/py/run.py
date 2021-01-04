#! /usr/bin/python3

import sys, os, time


def hasRepeatedWords(passphrase):
    for word in passphrase:
        if passphrase.count(word) > 1:
            return True
    return False


def part1(passphrases):
    return sum([ not hasRepeatedWords(passphrase) for passphrase in passphrases ])


def isAnagram(word1, word2):
    if len(word1) != len(word2):
        return False
    for c in word1:
        if word1.count(c) != word2.count(c):
            return False
    return True


def hasAnagram(passphrase):
    for index, word in enumerate(passphrase):
        for otherWord in passphrase[:index] + passphrase[index + 1:]:
            if isAnagram(word, otherWord):
                return True
    return False


def part2(passphrases):
    return sum([ not hasAnagram(passphrase) for passphrase in passphrases ])


def getInput(filePath):
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
    print(f"P1 time: {middle - start:.8f}")
    print(f"P2 time: {end - middle:.8f}")


if __name__ == "__main__":
    main()