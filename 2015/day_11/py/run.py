#! /usr/bin/python3

import sys, os, time
import re


forbiddenLetters = [ ord("i"), ord("o"), ord("l") ]
pairsRegex = re.compile(r"^.*(.)\1{1}.*(.)\2{1}.*$")
def isPasswordValid(password):
    ords = list(map(lambda c: ord(c), password))
    # for testOrd in forbiddenLetters:
    #     if testOrd in ords:
    #         return False

    if not pairsRegex.match(password):
        return False

    for index in range(0, len(ords) - 2):
        if ords[index] == ords[index + 1] - 1 and ords[index] == ords[index + 2] - 2:
            return True

    return False
    

def getNextChar(c):
    c += 1
    while c in forbiddenLetters:
        c += 1
    return chr(c)


aOrd = ord("a")
zOrd = ord("z")
def getNextPassword(current):
    result = list(current)
    for index in range(len(result) - 1, 0, -1):
        cOrd = ord(result[index])
        if cOrd == zOrd:
            result[index] = chr(aOrd)
            continue
        result[index] = getNextChar(cOrd)
        break
    return "".join(result)


def getNextValidPassword(currentPassword):
    currentPassword = getNextPassword(currentPassword)
    while not isPasswordValid(currentPassword):
        currentPassword = getNextPassword(currentPassword)

    return currentPassword


def part1(puzzleInput):
    return getNextValidPassword(puzzleInput)


def part2(puzzleInput):
    return getNextValidPassword(getNextValidPassword(puzzleInput))


def getInput(filePath):
    if not os.path.isfile(filePath):
        raise FileNotFoundError(filePath)
    
    with open(filePath, "r") as file:
        return file.read().strip()


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