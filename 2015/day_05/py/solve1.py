#! /usr/bin/python3

import re
from functools import reduce

from common import getInput


forbidenPairs = [ "ab", "cd", "pq", "xy" ]
vowelRegex = re.compile("[aeiou]")
repeatRegex = re.compile("(.)\\1{1,}")

def isWordNice(word):
    for pair in forbidenPairs:
        if pair in word:
            return False
    return len(vowelRegex.findall(word)) > 2 and len(repeatRegex.findall(word)) != 0


def main():
    niceWordCount = reduce(lambda currentCount, word: currentCount + isWordNice(word), getInput(), 0)
    print("Nice words:", niceWordCount)


if __name__ == "__main__":
    main()
