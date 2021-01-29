#! /usr/bin/python3

import sys, os, time
from typing import List, Tuple

Shuffle = Tuple[int,int]
NEW_STACK, CUT, INCREMENT = 0, 1, 2


def doShuffles(cards: List[int], shuffles: List[Shuffle]) -> List[int]:
    cardsCount = len(cards)
    replacement = [ 0 ] * cardsCount
    for shuffle, count in shuffles:
        if shuffle == NEW_STACK:
            cards = cards[::-1]
        elif shuffle == CUT:
            cards = cards[count:] + cards[:count]
        else:
            for index in range(cardsCount):
                replacement[(index * count) % cardsCount] = cards.pop(0)
            cards = replacement
    return cards


CARDS1 = 10007
POSITION1 = 2019
def part1(shuffles: List[Shuffle]) -> int:
    cards = doShuffles([ card for card in range(CARDS1) ], shuffles)
    return cards.index(POSITION1)


def inv(a: int, n:int): 
    return pow(a, n-2, n)


CARDS2 = 119315717514047
RUNS = 101741582076661
POSITION2 = 2020
def part2(shuffles: List[Shuffle]) -> int:    
    la = lb = 0
    a, b = 1, 0
    for shuffle, count in shuffles:
        if shuffle == NEW_STACK:
            la, lb = -1, -1
        elif shuffle == INCREMENT:
            la, lb = count, 0
        else:
            la, lb = 1, -count
        a = (la * a) % CARDS2
        b = (la * b + lb) % CARDS2

    Ma = pow(a, RUNS, CARDS2)
    Mb = (b * (Ma - 1) * inv(a-1, CARDS2)) % CARDS2
    return ((POSITION2 - Mb) * inv(Ma, CARDS2)) % CARDS2


def parseLine(line:str) -> Shuffle:
    if line.startswith("deal into"):
        return NEW_STACK, 0
    if line.startswith("cut"):
        return CUT, int(line.split(" ")[1])
    if line.startswith("deal with"):
        return INCREMENT, int(line.split(" ")[-1])
    raise Exception("Unknow shuffle", line)


def getInput(filePath: str):
    if not os.path.isfile(filePath):
        raise FileNotFoundError(filePath)
    
    with open(filePath, "r") as file:
        return [ parseLine(line) for line in file.readlines() ]


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