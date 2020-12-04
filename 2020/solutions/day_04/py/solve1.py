#! /usr/bin/python3

from functools import reduce

from common import getInput


passportMandatoryFields = [ 
    'byr', 
    'iyr', 
    'eyr', 
    'hgt', 
    'hcl', 
    'ecl', 
    'pid', 
   # 'cid' 
    ]
    

def isPassportValid(passport):
    for field in passportMandatoryFields:
        if not (field in passport):
            return False
    return True
    

def main():
    passports = getInput()
    validPassportCount = reduce(lambda currentCount, passport: currentCount + isPassportValid(passport), passports, 0)

    print("Valid passports count:", validPassportCount)


if __name__ == "__main__":
    main()
