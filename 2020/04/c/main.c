#include <stdio.h>
#include <stdlib.h>
#include <sys/time.h>
#include <regex.h>
#include <string.h>

#define FIELD_COUNT 7

typedef struct
{
    char *fields[FIELD_COUNT];
} Passport;
typedef struct
{
    Passport *passports;
    int count, size;
} Input;
typedef struct
{
    int part1;
    int part2;
} Results;

char *MANDATORY_FIELDS[] = {
    "byr",
    "iyr",
    "eyr",
    "hgt",
    "hcl",
    "ecl",
    "pid"};
int getFieldIndex(char *field)
{
    for (int index = 0; index < FIELD_COUNT; index++)
        if (strcmp(field, MANDATORY_FIELDS[index]) == 0)
            return index;
    return -1;
}

int countValidPasswords(Input input, int (*validationFunc)(Passport))
{
    int count = 0;
    while (input.count--)
        count += validationFunc(*(input.passports++));
    return count;
}

int part1(Passport passport)
{
    for (int index = 0; index < FIELD_COUNT; index++)
        if (passport.fields[index] == NULL)
            return 0;
    return 1;
}

int validateInt(char *value, int min, int max)
{
    int parsedValue;
    if (sscanf(value, "%d", &parsedValue))
        return parsedValue >= min && parsedValue <= max;
    return 0;
}

int validateBYR(char *value)
{
    return validateInt(value, 1920, 2002);
}

int validateIYR(char *value)
{
    return validateInt(value, 2010, 2020);
}

int validateEYR(char *value)
{
    return validateInt(value, 2020, 2030);
}

regex_t hgtRegex;
regex_t hclRegex;
regex_t pidRegex;

int validateHGT(char *value)
{
#define HGT_GROUP_COUNT 4
    regmatch_t groupArray[HGT_GROUP_COUNT];
    int group, groupLength, height;
    char unit[5];
    if (!regexec(&hgtRegex, value, HGT_GROUP_COUNT, groupArray, 0))
    {
        for (group = 0; group <= HGT_GROUP_COUNT && groupArray[group].rm_so != -1; group++)
        {
            groupLength = strlen(value) + 1;
            char cursorCopy[groupLength];
            strcpy(cursorCopy, value);
            cursorCopy[groupArray[group].rm_eo] = 0;
            switch (group)
            {
            case 1:
                height = atoi(cursorCopy + groupArray[group].rm_so);
                break;
            case 2:
                strcpy(unit, cursorCopy + groupArray[group].rm_so);
                break;
            }
        }
    }
    else
        return 0;
    return strcmp(unit, "cm") == 0 ? height >= 150 && height <= 193
                                   : height >= 59 && height <= 76;
}

int validateHCL(char *value)
{
    return !regexec(&hclRegex, value, 0, NULL, 0);
}

char *ECLS[] = {"amb", "blu", "brn", "gry", "grn", "hzl", "oth"};
const int ECLS_COUNT = 7;
int validateECL(char *value)
{
    for (int index = 0; index < ECLS_COUNT; index++)
        if (strcmp(value, ECLS[index]) == 0)
            return 1;
    return 0;
}

int validatePID(char *value)
{
    return !regexec(&pidRegex, value, 0, NULL, 0);
}

int (*VALIDATIONS[])(char *) = {
    &validateBYR,
    &validateIYR,
    &validateEYR,
    &validateHGT,
    &validateHCL,
    &validateECL,
    &validatePID,
};

int part2(Passport passport)
{
    for (int index = 0; index < FIELD_COUNT; index++)
        if (passport.fields[index] == NULL || !VALIDATIONS[index](passport.fields[index]))
            return 0;
    return 1;
}

Results solve(Input input)
{
    if (regcomp(&hgtRegex, "^([0-9]{2,3})(cm|in)$", REG_EXTENDED))
    {
        perror("Error compiling hgt regex.");
        exit(1);
    }
    if (regcomp(&hclRegex, "^#[0-9a-f]{6}$", REG_EXTENDED))
    {
        perror("Error compiling hcl regex.");
        exit(1);
    }
    if (regcomp(&pidRegex, "^[0-9]{9}$", REG_EXTENDED))
    {
        perror("Error compiling hgt regex.");
        exit(1);
    }
    return (Results){countValidPasswords(input, &part1), countValidPasswords(input, &part2)};
}

Passport initializePassport()
{
    Passport passport;
    for (int index = 0; index < FIELD_COUNT; index++)
        passport.fields[index] = NULL;
    return passport;
}

#define INPUT_INCREMENT 10
void addToInput(Input *input, Passport passport)
{
    if (input->count == input->size)
    {
        Passport *oldPassports = input->passports;
        Passport *newPassports = realloc(oldPassports, (input->size + INPUT_INCREMENT) * sizeof(Passport));
        input->passports = newPassports;
        input->size += INPUT_INCREMENT;
    }
    input->passports[input->count++] = passport;
}

Input getInput(char *filePath)
{
    FILE *file;
    if ((file = fopen(filePath, "r")) == NULL)
    {
        perror("Error reading input file!\n");
        exit(1);
    }
#define INPUT_GROUP_COUNT 3
    regmatch_t groupArray[INPUT_GROUP_COUNT];
    regex_t regexCompiled;
    if (regcomp(&regexCompiled, "(byr|iyr|eyr|hgt|hcl|ecl|pid):([^ \n]+)", REG_EXTENDED))
    {
        perror("Error compiling regex.");
        exit(1);
    }
    char *line = NULL, *cursor = NULL, *field, *value;
    size_t lineLength;
    Input input = {
        calloc(10, sizeof(Passport)),
        0,
        10};
    int group, groupLength;
    Passport passport = initializePassport();
    while (getline(&line, &lineLength, file) != EOF)
    {
        if (line[0] == '\n')
        {
            addToInput(&input, passport);
            passport = initializePassport();
            continue;
        }
        cursor = line;
        while (!regexec(&regexCompiled, cursor, INPUT_GROUP_COUNT, groupArray, 0))
        {
            for (group = 0; group <= INPUT_GROUP_COUNT && groupArray[group].rm_so != -1; group++)
            {
                groupLength = strlen(cursor) + 1;
                char cursorCopy[groupLength];
                strcpy(cursorCopy, cursor);
                cursorCopy[groupArray[group].rm_eo] = 0;
                switch (group)
                {
                case 1:
                    field = malloc(groupLength);
                    strcpy(field, cursorCopy + groupArray[group].rm_so);
                    break;
                case 2:
                    value = malloc(groupLength);
                    strcpy(value, cursorCopy + groupArray[group].rm_so);
                    break;
                }
            }
            cursor += groupArray[0].rm_eo;
            passport.fields[getFieldIndex(field)] = value;
        }
    }
    addToInput(&input, passport);
    fclose(file);
    return input;
}

void freeInput(Input input)
{
}

int main(int argc, char **argv)
{
    if (argc != 2)
    {
        perror("Please, add input file path as parameter");
        exit(1);
    }
    struct timeval starts, ends;
    gettimeofday(&starts, NULL);
    Input input = getInput(argv[1]);
    Results results = solve(input);
    gettimeofday(&ends, NULL);
    freeInput(input);
    printf("P1: %d\n", results.part1);
    printf("P2: %d\n\n", results.part2);
    printf("Time: %.7f\n", (double)((ends.tv_sec - starts.tv_sec) * 1000000 + ends.tv_usec - starts.tv_usec) / 1000000);
    return 0;
}