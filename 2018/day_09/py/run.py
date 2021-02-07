#! /usr/bin/python3

import sys, os, time
from typing import Tuple, Union
import re
from itertools import cycle


class Marble():
    def __init__(self, number: int, previous: Union['Marble',None], next: Union['Marble',None]):
        self.number = number
        self.previous = previous if previous else self
        self.previous.next = self
        self.next = next if next else self
        self.next.previous = self
        

def playerGame(playerCount: int, lastMarble:int) -> int:
    scores = { player + 1: 0 for player in range(playerCount) }
    players = cycle(scores.keys())
    currentPlayer = next(players)
    currentMarble = Marble(0, None, None)
    nextNumber = 0
    while nextNumber <= lastMarble:
        nextNumber += 1
        currentPlayer = next(players)
        if nextNumber % 23:
            currentMarble = Marble(nextNumber, currentMarble.next, currentMarble.next.next)
        else:
            backCount = 6
            while backCount:
                currentMarble = currentMarble.previous
                backCount -= 1
            marbleToRemove = currentMarble.previous
            scores[currentPlayer] += nextNumber + marbleToRemove.number
            marbleToRemove.previous.next = currentMarble
            currentMarble.previous = marbleToRemove.previous
    
    return max(scores.values())


def part1(puzzleInput: Tuple[int,int]) -> int:
    return playerGame(*puzzleInput)


def part2(puzzleInput: Tuple[int,int]) -> int:
    playerCount, lastMarble = puzzleInput
    return playerGame(playerCount, lastMarble * 100)


inputRegex = re.compile(r"^(?P<players>\d+) players; last marble is worth (?P<last>\d+)")
def getInput(filePath: str) -> Tuple[int,int]:
    if not os.path.isfile(filePath):
        raise FileNotFoundError(filePath)
    
    with open(filePath, "r") as file:
        match = inputRegex.match(file.read())
        if match:
            return int(match.group("players")), int(match.group("last"))
        raise Exception("Bad input")


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