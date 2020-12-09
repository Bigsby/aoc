#! /usr/bin/python3

from common import getInput


def main():
    grid = getInput()
    limit = len(grid.lights) - 1
    alwaysOn = [
        (0, 0),
        (0, limit),
        (limit, 0),
        (limit, limit)
    ]

    for step in range(100):
        grid.calculateNextStep(alwaysOn)

        
    print()
    print("Lights on:", grid.lightsOnCount())


if __name__ == "__main__":
    main()
