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


def validate_byr(value):
    byr, valid = intTryParse(value)
    return valid and byr >= 1920 and byr <= 2002
 

def validate_iyr(value):
    iyr, valid = intTryParse(value)
    return valid and iyr >= 2010 and iyr <= 2020


def validate_eyr(value):
    eyr, valid = intTryParse(value)
    return valid and eyr >= 2020 and eyr <= 2030


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
def validate_hcl(value):
    match = hclRegEx.match(value)
    if match:
        return True
    else:
        return False


ecls = [ "amb", "blu", "brn", "gry", "grn", "hzl", "oth" ]
def validate_ecl(value):
    return value in ecls


pidRegEx = re.compile("^[\d]{9}$")
def validate_pid(value):
    return pidRegEx.match(value)


validations = {
    'byr': validate_byr,
    'iyr': validate_iyr,
    'eyr': validate_eyr,
    'hgt': validate_hgt,
    'hcl': validate_hcl,
    'ecl': validate_ecl,
    'pid': validate_pid
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
