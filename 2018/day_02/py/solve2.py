#! /usr/bin/python3

from itertools import combinations

from common import getInput


def differenceCount(s1, s2):
    return [ i for i in range(len(s1)) if s1[i] != s2[i] ]


def main():
    ids = list(getInput())
    result = None
    for id1, id2 in combinations(ids, 2):
        differences = differenceCount(id1, id2)
        if len(differences) == 1:
            diferentIndex = differences[0]
            result = id1[:diferentIndex] + id1[diferentIndex + 1:]

    print("Result:", result)




if __name__ == "__main__":
    main()
