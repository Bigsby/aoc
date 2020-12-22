#! /usr/bin/python3

from common import getInput


def main():
    lines = list(getInput())
    total = 0
    for line in lines:
        maximum = max(line)
        minimum = min(line)
        total += maximum - minimum

    print("Result:", total)


if __name__ == "__main__":
    main()
