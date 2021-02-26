#! /usr/bin/python3

import sys, os, time
from typing import Tuple
import re


FORBIDDEN_LETTERS = [ ord("i"), ord("o"), ord("l") ]
pairsRegex = re.compile(r"^.*(.)\1{1}.*(.)\2{1}.*$")
def isPasswordValid(password: str) -> bool:
    if not pairsRegex.match(password):
        return False
    ords = list(map(lambda c: ord(c), password))
    for index in range(len(ords) - 2):
        if ords[index] == ords[index + 1] - 1 and ords[index] == ords[index + 2] - 2:
            return True
    return False
    

def getNextChar(c: int) -> str:
    c += 1
    while c in FORBIDDEN_LETTERS:
        c += 1
    return chr(c)


A_CHR = "a"
Z_ORD = ord("z")
def getNextPassword(currentPassword: str) -> str:
    result = list(currentPassword)
    for index in range(len(result) - 1, 0, -1):
        cOrd = ord(result[index])
        if cOrd == Z_ORD:
            result[index] = A_CHR
            continue
        result[index] = getNextChar(cOrd)
        break
    return "".join(result)


def getNextValidPassword(currentPassword: str) -> str:
    currentPassword = getNextPassword(currentPassword)
    while not isPasswordValid(currentPassword):
        currentPassword = getNextPassword(currentPassword)
    return currentPassword


def solve(currentPassword: str) -> Tuple[str,str]:
    part1 = getNextValidPassword(currentPassword)
    return (part1, getNextValidPassword(part1))


def getInput(filePath: str):
    if not os.path.isfile(filePath):
        raise FileNotFoundError(filePath)
    
    with open(filePath, "r") as file:
        return file.read().strip()


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