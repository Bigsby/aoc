import sys, os, re


entryRegEx = re.compile('([a-z]{3})\:([^\s]+)')

def getInput():
    if len(sys.argv) != 2:
        print("Please, add input file path as parameter")
        sys.exit(1)

    filePath = sys.argv[1]
    if not os.path.isfile(filePath):
        print("File not found")
        sys.exit(1)

    passports = []

    with open(filePath) as file:
        contents = file.read()
        entries = contents.split("\n\n")
        for entry in entries:
            matches = entryRegEx.findall(entry)
            passports.append(dict(matches))
            
    return passports
