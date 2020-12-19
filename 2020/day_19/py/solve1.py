#! /usr/bin/python3
import re
from functools import reduce

from common import getInput, generateRegex


def main():
    rules, messages = getInput()

    zeroRegex = generateRegex(rules, 0)
    count = reduce(lambda soFar, message: soFar + (1 if re.fullmatch(zeroRegex, message) else 0), messages, 0)
    print("Zero rule matches:", count)


if __name__ == "__main__":
    main()
