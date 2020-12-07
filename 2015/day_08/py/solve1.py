#! /usr/bin/python3

import re
from functools import reduce

from common import getInput


hexaRegex = re.compile(r"\\x[0-9a-f]{2}")

def getStringDifference(string):
    totalLength = len(string)
    stripped = string.replace(r"\\", "r")
    stripped = stripped.replace(r"\"", "r")
    stripped = hexaRegex.sub("r", stripped)
    stripped = stripped.strip(r"\"")
    return totalLength - len(stripped) 


def main():
    difference = reduce(lambda soFar, s: soFar + getStringDifference(s), getInput(), 0)
    print("Difference is:", difference)


if __name__ == "__main__":
    main()
