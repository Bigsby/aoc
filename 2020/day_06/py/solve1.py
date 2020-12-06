#! /usr/bin/python3

from functools import reduce

from common import getInput


def countGroupAnswers(group):
    return reduce(lambda currentCount, letter: currentCount + (group["answers"][letter] != 0), group["answers"].keys(), 0)


def main():
    answersCount = reduce(lambda currentCount, group: currentCount + countGroupAnswers(group), getInput(), 0)
    print("Total yes anwsers:", answersCount)


if __name__ == "__main__":
    main()
