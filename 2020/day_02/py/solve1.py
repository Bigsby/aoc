#! /usr/bin/python3

from typing import Tuple
from functools import reduce

from common import getLines


def countOccurences(password: str, letter: str) -> int:
    return reduce(lambda currentCount, c: currentCount + (c == letter), password, 0)


def isLineValid(line: Tuple[int,int,str,str]) -> bool:
    minimum, maximum, letter, password = line
    occurenceCount = countOccurences(password, letter) 
    return occurenceCount >= minimum and occurenceCount <= maximum


def main():
    validPasswordCount = reduce(lambda currentCount, line: currentCount + isLineValid(line), getLines(), 0)

    print("Valid password count is", validPasswordCount)


if __name__ == "__main__":
    main()
