#! /usr/bin/python3

import re

from common import getInput

def processReplacement(molecule, replacement):
    for match in re.finditer(replacement.source, molecule):
        mBefore = molecule[0 : match.start()]
        mAfter = molecule[match.end() : ]
        yield mBefore + replacement.target + mAfter
        

def main():
    replacements, molecule = getInput()
    newMolecules = []
    for replacement in replacements:
        for newMolecule in processReplacement(molecule, replacement):
            newMolecules.append(newMolecule)

    print("New molecules count:", len(list(set(newMolecules))))


if __name__ == "__main__":
    main()
