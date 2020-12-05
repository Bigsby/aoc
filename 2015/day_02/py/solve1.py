#! /usr/bin/python3

from common import getInput


def main():
    totalPaper = 0
    for dimension in getInput():
        w, l, h = dimension
        wl = w * l
        wh = w * h
        hl = h * l
        smallest = min(wl, wh, hl)
        totalPaper = totalPaper + (2 * wl) + (2 * wh) + (2 * hl) + smallest

    print("Total paper", totalPaper)

if __name__ == "__main__":
    main()
