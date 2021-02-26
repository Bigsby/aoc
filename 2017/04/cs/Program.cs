using System;
using static System.Console;
using System.IO;
using System.Diagnostics;
using System.Linq;

namespace AoC
{
    class Program
    {
        static int RunTests(string[][] passphrases, Func<string[], bool> validationFunc)
            => passphrases.Count(passphrase => validationFunc(passphrase));

        static bool IsAnagram(string word1, string word2)
            => word1.Length == word2.Length &&
                word1.All(c => word1.Count(t => t == c) == word2.Count(t => t == c));

        static bool HasNoAnagram(string[] passphrase)
        {
            foreach (var (word, index) in passphrase.Select((word, index) => (word, index)))
                foreach (var otherWord in passphrase.Take(index).Concat(passphrase.Skip(index + 1)))
                    if (IsAnagram(word, otherWord))
                        return false;
            return true;
        }

        static (int, int) Solve(string[][] passphrases)
            => (
                RunTests(passphrases, 
                    passphrase => !passphrase.Any(word => passphrase.Count(p => p == word) > 1)),
                RunTests(passphrases, HasNoAnagram)
            );

        static string[][] GetInput(string filePath)
            => !File.Exists(filePath) ? throw new FileNotFoundException(filePath)
            : File.ReadAllLines(filePath).Select(line => line.Split(' ', StringSplitOptions.RemoveEmptyEntries)).ToArray();

        static void Main(string[] args)
        {
            if (args.Length != 1) throw new Exception("Please, add input file path as parameter");

            var watch = Stopwatch.StartNew();
            var (part1Result, part2Result) = Solve(GetInput(args[0]));
            watch.Stop();
            WriteLine($"P1: {part1Result}");
            WriteLine($"P2: {part2Result}");
            WriteLine();
            WriteLine($"Time: {(double)watch.ElapsedTicks / 100 / TimeSpan.TicksPerSecond:f7}");
        }
    }
}