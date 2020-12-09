#! /usr/bin/python3
import re
from functools import reduce

from common import getInput


numberRegex = re.compile(r"(-?[\d]+)")
def getNumbers(contents):
    for match in numberRegex.finditer(contents):
        yield int(match.group(1))
        

def main():
    numbers = getNumbers(getInput())
    result = reduce(lambda soFar, number: soFar + number, numbers)
    print("Result:", result)


if __name__ == "__main__":
    main()
