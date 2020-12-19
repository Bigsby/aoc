#! /usr/bin/python3
import re
from functools import reduce

from common import getInput, generateRegex


def main():
    rules, messages = getInput()

    zeroRegeex = generateRegex(rules, 0)
    count = 0
    for message in messages:
        if re.fullmatch(zeroRegeex, message):
            count += 1
    print("Zero rule matches:", count)


if __name__ == "__main__":
    main()
