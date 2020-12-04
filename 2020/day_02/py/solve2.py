#! /usr/bin/python3

from typing import Tuple
from functools import reduce

from common import getLines


def isLineValid(line: Tuple[int,int,str,str]) -> bool:
    first, second, letter, password = line 
    return (password[first - 1] == letter) ^ (password[second - 1] == letter)

    
def main():
    validPasswordCount = reduce(lambda currentCount, line: currentCount + isLineValid(line), getLines(), 0)

    print("Valid password count is", validPasswordCount)


if __name__ == "__main__":
    main()
