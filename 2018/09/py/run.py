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


def solve(puzzleInput: Tuple[int,int]) -> Tuple[int,int]:
    playerCount, lastMarble = puzzleInput
    scores = { player + 1: 0 for player in range(playerCount) }
    players = cycle(scores.keys())
    currentPlayer = next(players)
    currentMarble = Marble(0, None, None)
    nextNumber = 0
    part1Result = 0
    while nextNumber <= lastMarble * 100:
        nextNumber += 1
        if nextNumber == lastMarble:
            part1Result = max(scores.values())
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
    return part1Result, max(scores.values())


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

    start = time.perf_counter()
    part1Result, part2Result = solve(getInput(sys.argv[1]))
    end = time.perf_counter()
    print("P1:", part1Result)
    print("P2:", part2Result)
    print()
    print(f"Time: {end - start:.7f}")


if __name__ == "__main__":
    main()