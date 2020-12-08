#! /usr/bin/python3

from common import getInput


def main():
    grid = getInput()
    for step in range(100):
        grid.calculateNextStep()
        
    print()
    print("Lights on:", grid.lightsOnCount())


if __name__ == "__main__":
    main()
