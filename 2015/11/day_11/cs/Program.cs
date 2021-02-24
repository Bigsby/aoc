using System;
using static System.Console;
using System.IO;
using System.Diagnostics;
using System.Linq;
using System.Text.RegularExpressions;

namespace AoC
{
    class Program
    {
        static Regex pairsRegex = new Regex(@"^.*(.)\1{1}.*(.)\2{1}.*$", RegexOptions.Compiled);
        static bool IsPasswordValid(string password)
        {
            var ords = password.Select(c => (int)c).ToArray();
            return pairsRegex.Match(password).Success 
                && Enumerable.Range(0, password.Length - 2)
                    .Any(index => ords[index] == ords[index + 1] - 1 && ords[index] == ords[index + 2] - 2);
        }

        static int[] FORBIDDEN_LETTERS = new [] { (int)'i', (int)'o', (int)'l' };
        static char GetNextChar(int c)
        {
            while (FORBIDDEN_LETTERS.Contains(++c));
            return (char)c;
        }

        const char A_CHR = 'a';
        const int Z_ORD = 'z';
        static string GetNextPassword(string currentPassword)
        {
            var result = currentPassword.ToArray();
            for (var index = currentPassword.Length - 1; index > 0; index--)
            {
                var cOrd = (int)result[index];
                if (cOrd == Z_ORD)
                {
                    result[index] = A_CHR;
                    continue;
                }
                result[index] = GetNextChar(cOrd);
                break;
            }
            return new string(result);
        }

        static string GetNextValidPassword(string currentPassword)
        {
            while (!IsPasswordValid(currentPassword = GetNextPassword(currentPassword)));
            return currentPassword;
        }

        static string Part1(string currentPassword) => GetNextValidPassword(currentPassword);

        static string Part2(string currentPassword) => GetNextValidPassword(GetNextValidPassword(currentPassword));

        static string GetInput(string filePath)
        {
            if (!File.Exists(filePath)) throw new FileNotFoundException(filePath);
            return File.ReadAllText(filePath).Trim();
        }

        static void Main(string[] args)
        {
            if (args.Length != 1) throw new Exception("Please, add input file path as parameter");

            var puzzleInput = GetInput(args[0]);
            var watch = Stopwatch.StartNew();
            var part1Result = Part1(puzzleInput);
            watch.Stop();
            var middle = watch.ElapsedTicks;
            watch = Stopwatch.StartNew();
            var part2Result = Part2(puzzleInput);
            watch.Stop();
            WriteLine($"P1: {part1Result}");
            WriteLine($"P2: {part2Result}");
            WriteLine();
            WriteLine($"P1 time: {(double)middle / 100 / TimeSpan.TicksPerSecond:f7}");
            WriteLine($"P2 time: {(double)watch.ElapsedTicks / 100 / TimeSpan.TicksPerSecond:f7}");
        }
    }
}