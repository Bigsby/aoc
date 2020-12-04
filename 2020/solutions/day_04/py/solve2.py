#! /usr/bin/python3

from functools import reduce
import re

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

   
def intTryParse(value):
    try:
        return int(value), True
    except:
        return value, False


def validate_int(value, min, max):
    parsed, valid = intTryParse(value)
    return valid and parsed >= min and parsed <= max


hgtRegEx = re.compile('^(\d{2,3})(cm|in)$')
def validate_hgt(value):
    match = hgtRegEx.match(value)
    if match:
        height = int(match.group(1))
        if match.group(2) == "cm":
            return height >= 150 and height <= 193
        else:
            return height >= 59 and height <= 76
    return False


hclRegEx = re.compile('^#[0-9a-f]{6}$')
ecls = [ "amb", "blu", "brn", "gry", "grn", "hzl", "oth" ]
pidRegEx = re.compile("^[\d]{9}$")


validations = {
    'byr': lambda value: validate_int(value, 1920, 2002),
    'iyr': lambda value: validate_int(value, 2010, 2020),
    'eyr': lambda value: validate_int(value, 2020, 2030),
    'hgt': validate_hgt,
    'hcl': lambda value: hclRegEx.match(value),
    'ecl': lambda value: value in ecls,
    'pid': lambda value: pidRegEx.match(value)
}


def isPassportValid(passport):
    for field in passportMandatoryFields:
        if not (field in passport) or not validations[field](passport[field]):            
            return False
    return True
    

def main():
    passports = getInput()
    validPassportCount = reduce(lambda currentCount, passport: currentCount + isPassportValid(passport), passports, 0)

    print("Valid passports count:", validPassportCount)


if __name__ == "__main__":
    main()
