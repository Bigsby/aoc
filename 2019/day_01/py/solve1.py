#! /usr/bin/python3

from common import getInput


def main():
    masses = list(getInput())
    result = sum((mass // 3) - 2 for mass in masses)
    print("Result:", result)


if __name__ == "__main__":
    main()
