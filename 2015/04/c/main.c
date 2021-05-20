#include <stdio.h>
#include <stdlib.h>
#include <sys/time.h>
#include <math.h>
#include <string.h>

typedef char *Input;
typedef struct
{
    int part1;
    int part2;
} Results;

typedef union uwb
{
    unsigned w;
    unsigned char b[4];
} WBunion;

typedef unsigned Digest[4];

unsigned f0(unsigned abcd[])
{
    return (abcd[1] & abcd[2]) | (~abcd[1] & abcd[3]);
}

unsigned f1(unsigned abcd[])
{
    return (abcd[3] & abcd[1]) | (~abcd[3] & abcd[2]);
}

unsigned f2(unsigned abcd[])
{
    return abcd[1] ^ abcd[2] ^ abcd[3];
}

unsigned f3(unsigned abcd[])
{
    return abcd[2] ^ (abcd[1] | ~abcd[3]);
}

typedef unsigned (*DgstFctn)(unsigned a[]);

unsigned *calcKs(unsigned *k)
{
    double s, pwr;
    int i;
    pwr = pow(2, 32);
    for (i = 0; i < 64; i++)
    {
        s = fabs(sin(1 + i));
        k[i] = (unsigned)(s * pwr);
    }
    return k;
}

unsigned rol(unsigned v, short amt)
{
    unsigned msk1 = (1 << amt) - 1;
    return ((v >> (32 - amt)) & msk1) | ((v << amt) & ~msk1);
}

unsigned *md5(const char *msg, int mlen)
{
    static Digest h0 = {0x67452301, 0xEFCDAB89, 0x98BADCFE, 0x10325476};
    static DgstFctn ff[] = {&f0, &f1, &f2, &f3};
    static short M[] = {1, 5, 3, 7};
    static short O[] = {0, 1, 5, 0};
    static short rot0[] = {7, 12, 17, 22};
    static short rot1[] = {5, 9, 14, 20};
    static short rot2[] = {4, 11, 16, 23};
    static short rot3[] = {6, 10, 15, 21};
    static short *rots[] = {rot0, rot1, rot2, rot3};
    static unsigned kspace[64];
    static unsigned *k;
    static Digest h;
    Digest abcd;
    DgstFctn fctn;
    short m, o, g;
    unsigned f;
    short *rotn;
    union
    {
        unsigned w[16];
        char b[64];
    } mm;
    int os = 0;
    int grp, grps, q, p;
    unsigned char *msg2;
    if (k == NULL)
        k = calcKs(kspace);
    for (q = 0; q < 4; q++)
        h[q] = h0[q];
    {
        grps = 1 + (mlen + 8) / 64;
        msg2 = malloc(64 * grps);
        memcpy(msg2, msg, mlen);
        msg2[mlen] = (unsigned char)0x80;
        q = mlen + 1;
        while (q < 64 * grps)
        {
            msg2[q] = 0;
            q++;
        }
        {
            WBunion u;
            u.w = 8 * mlen;
            q -= 8;
            memcpy(msg2 + q, &u.w, 4);
        }
    }
    for (grp = 0; grp < grps; grp++)
    {
        memcpy(mm.b, msg2 + os, 64);
        for (q = 0; q < 4; q++)
            abcd[q] = h[q];
        for (p = 0; p < 4; p++)
        {
            fctn = ff[p];
            rotn = rots[p];
            m = M[p];
            o = O[p];
            for (q = 0; q < 16; q++)
            {
                g = (m * q + o) % 16;
                f = abcd[1] + rol(abcd[0] + fctn(abcd) + k[q + 16 * p] + mm.w[g], rotn[q % 4]);

                abcd[0] = abcd[3];
                abcd[3] = abcd[2];
                abcd[2] = abcd[1];
                abcd[1] = f;
            }
        }
        for (p = 0; p < 4; p++)
            h[p] += abcd[p];
        os += 64;
    }
    if (msg2)
        free(msg2);

    return h;
}

void md5HexDigest(const char *msg, char *result)
{
    int j, k;
    unsigned *d = md5(msg, strlen(msg));
    WBunion u;
    char *cursor = result;
    for (j = 0; j < 4; j++)
    {
        u.w = d[j];
        for (k = 0; k < 4; k++)
        {
            sprintf(cursor, "%02x", u.b[k]);
            cursor += 2;
        }
    }
}

const char *DIGITS = "0123456789abcdef";
char* itoa(int val, int base){
	static char buf[32] = {0};
	int i = 30;
	for(; val && i ; --i, val /= base)
		buf[i] = DIGITS[val % base];	
	return &buf[i+1];
	
}

int startsWith(const char *str, char digit, int count)
{
    while (count--)
        if (*(str++) != digit)
            return 0;
    return 1;
}

int findHash(char *secretKey, int prefixCount, int guess)
{
    char hash[32];
    char test[32];
    char guessString[32 - strlen(secretKey)];
    while (1)
    {
        strcpy(test, secretKey);
        strcat(test, itoa(guess, 10));
        md5HexDigest(test, hash);
        if (startsWith(hash, '0', prefixCount))
            return guess;
        guess++;
    }
}

Results solve(Input input)
{
    int part1Result = findHash(input, 5, 1);
    return (Results){part1Result, findHash(input, 6, part1Result)};
}

char *rtrim(char *str, const char *seps)
{
    int i;
    if (seps == NULL)
    {
        seps = "\t\n\v\f\r ";
    }
    i = strlen(str) - 1;
    while (i >= 0 && strchr(seps, str[i]) != NULL)
    {
        str[i] = '\0';
        i--;
    }
    return str;
}

Input getInput(char *filePath)
{
    FILE *file;
    if ((file = fopen(filePath, "r")) == NULL)
    {
        perror("Error reading input file!\n");
        exit(1);
    }
    fseek(file, 0, SEEK_END);
    long length = ftell(file);
    rewind(file);
    char *key = calloc(length, length + 1);
    fread(key, length, 1, file);
    fclose(file);
    return rtrim(key, NULL);
}

void freeInput(Input input)
{
    free(input);
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