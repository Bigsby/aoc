#! /usr/bin/python3

from common import getInput


def main():
    expressions = list(getInput())
    result = sum(expressions)
    print("Sum of expression results:", result)


if __name__ == "__main__":
    main()
