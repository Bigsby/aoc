#! /usr/bin/python3

import re

from common import getInput, processReplacement


def main():
    replacements, molecule = getInput()
    newMolecules = []
    for replacement in replacements:
        for newMolecule in processReplacement(molecule, replacement):
            newMolecules.append(newMolecule)

    print("New molecules count:", len(list(set(newMolecules))))


if __name__ == "__main__":
    main()
