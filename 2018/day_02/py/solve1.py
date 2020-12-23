#! /usr/bin/python3

from common import getInput


def main():
    ids = list(getInput())

    twiceCount = 0
    thriceCount = 0

    for id in ids:
        idCounts = { id.count(c) for c in id }
        twiceCount += 2 in idCounts
        thriceCount += 3 in idCounts

    result = twiceCount * thriceCount
    print("Result:", result)


if __name__ == "__main__":
    main()