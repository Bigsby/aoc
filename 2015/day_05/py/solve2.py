#! /usr/bin/python3

import re
from functools import reduce

from common import getInput


def hasRepeatingPair(word):
    for pairStart in range(0, len(word) - 2):
        pairToTest = word[pairStart : pairStart + 2]
        startOfWord = word[0 : pairStart] 
        endOfWord = word[pairStart + 2 : len(word)]
        if pairToTest in startOfWord or pairToTest in endOfWord:
            return True
    return False


def hasRepeatingLetter(word):
    for index in range(0, len(word) - 2):
        if word[index] == word[index + 2]:
            return True
    return False


def isWordNice(word):
    return hasRepeatingPair(word) and hasRepeatingLetter(word)


def main():
    niceWordCount = reduce(lambda currentCount, word: currentCount + isWordNice(word), getInput(), 0)
    print("Nice words:", niceWordCount)


if __name__ == "__main__":
    main()
