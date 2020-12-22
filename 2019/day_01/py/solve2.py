#! /usr/bin/python3

from common import getInput


def getFuel(mass):
    total = 0
    currentMass = mass
    while True:
        fuel = currentMass // 3 - 2
        if fuel <= 0:
            break
        total += fuel
        currentMass = fuel

    return total


def main():
    masses = list(getInput())
    result = sum(getFuel(mass) for mass in masses)
    print("Result:", result)


if __name__ == "__main__":
    main()
