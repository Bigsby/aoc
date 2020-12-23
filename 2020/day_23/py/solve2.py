#! /usr/bin/python3

from common import getInput, playGame


def main():
    cups = list(getInput())
    for cup in range(10, 10**6 + 1):
        cups.append(cup)

    oneNode = playGame(cups, 10**7)
    result = oneNode.next.value * oneNode.next.next.value

    print("Result:", result)


if __name__ == "__main__":
    main()
