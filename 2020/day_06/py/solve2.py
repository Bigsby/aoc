#! /usr/bin/python3

from functools import reduce

from common import getInput


def getGroupCommonAnswers(group):
    return reduce(lambda currentCount, letter: currentCount + (group["answers"][letter] == group["peopleCount"]), group["answers"].keys(), 0)


def main():
    commonAnswersCount = reduce(lambda currentCount, group: currentCount + getGroupCommonAnswers(group), getInput(), 0)
    print("Total common answers:", commonAnswersCount)


if __name__ == "__main__":
    main()
