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

        static int Part1(string[][] passphrases) => RunTests(passphrases, 
            passphrase => !passphrase.Any(word => passphrase.Count(p => p == word) > 1));

        static bool IsAnagram(string word1, string word2)
        {
            return word1.Length == word2.Length &&
                word1.All(c => word1.Count(t => t == c) == word2.Count(t => t == c));
        }

        static bool HasNoAnagram(string[] passphrase)
        {
            foreach (var (word, index) in passphrase.Select((word, index) => (word, index)))
                foreach (var otherWord in passphrase[Range.EndAt(index)].Concat(passphrase[Range.StartAt(index + 1)]))
                    if (IsAnagram(word, otherWord))
                        return false;
            return true;
        }

        static int Part2(string[][] passphrases) => RunTests(passphrases, HasNoAnagram);

        static string[][] GetInput(string filePath)
        {
            if (!File.Exists(filePath)) throw new FileNotFoundException(filePath);
            return File.ReadAllLines(filePath).Select(line => line.Split(' ', StringSplitOptions.RemoveEmptyEntries)).ToArray();
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