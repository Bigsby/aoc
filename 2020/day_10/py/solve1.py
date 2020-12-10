#! /usr/bin/python3

from common import getInput


def main():
    numbers = sorted(list(getInput()))
    diff1 = 0
    diff3 = 1
    currentJoltage = 0
    
    while len(numbers):
        newJoltage = numbers.pop(0)
        diff = newJoltage - currentJoltage
        if diff == 1:
            diff1 += 1
        elif diff == 3:
            diff3 += 1
        else:
            print("Diff:", diff)
        currentJoltage = newJoltage

    print("Diff 1:", diff1)
    print("Diff 3:", diff3)
    print("Result:", diff1 * diff3)


if __name__ == "__main__":
    main()
