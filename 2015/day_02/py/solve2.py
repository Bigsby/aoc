#! /usr/bin/python3

from common import getInput


def main():
    totalRibbon = 0
    for dimension in getInput():
        w, l, h = dimension
        sidesList = [w, l, h]
        sidesList.remove(max(sidesList))
        totalRibbon = totalRibbon + 2 * sidesList[0] + 2 * sidesList[1] + w * l * h

    print("Total ribbon lenght:", totalRibbon)


if __name__ == "__main__":
    main()
