#! /usr/bin/python3

from itertools import permutations

from common import getInput


def main():
    lines = list(getInput())
    total = 0
    for line in lines:
        pairs = permutations(line, 2)
        for pair in pairs:
            if pair[0] > pair[1] and pair[0] % pair[1] == 0:
                total += pair[0] // pair[1]

    print("Result:", total)
                


if __name__ == "__main__":
    main()
