#! /usr/bin/python3

import re
from functools import reduce

from common import getInput


hexaRegex = re.compile(r"\\x[0-9a-f]{2}")

def getStringDifference(string):
    initialLength = len(string)
    escaped = re.escape(string)
    escaped = escaped.replace("\"", "\\\"")
    return 2 + len(escaped) - initialLength


def main():
    difference = reduce(lambda soFar, s: soFar + getStringDifference(s), getInput(), 0)
    print("Difference is:", difference)


if __name__ == "__main__":
    main()
