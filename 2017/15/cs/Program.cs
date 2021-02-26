using System;
using static System.Console;
using System.IO;
using System.Diagnostics;
using System.Collections.Generic;
using System.Text.RegularExpressions;

namespace AoC
{
    class Program
    {
        const long MODULUS = 2147483647;
        static IEnumerator<long> BuildGenerator(long number, long factor, long divisor)
        {
            while (true)
            {
                number = (number * factor) % MODULUS;
                if (number % divisor == 0)
                    yield return number & 0xffff;
            }
        }

        const int FACTOR_A = 16807;
        const int FACTOR_B = 48271;
        static int RunSequences(Tuple<long, long> generators, long divisorA, long divisorB, long millionCycles)
        {
            var (generatorA, generatorB) = generators;
            var sequenceA = BuildGenerator(generatorA, FACTOR_A, divisorA);
            var sequenceB = BuildGenerator(generatorB, FACTOR_B, divisorB);
            var matches = 0;
            for (var i = 0; i < millionCycles * 1_000_000; i++)
            {
                sequenceA.MoveNext();
                sequenceB.MoveNext();
                if (sequenceA.Current == sequenceB.Current)
                    matches++;
            }
            return matches;
        }

        const int DIVISOR_A = 4;
        const int DIVISOR_B = 8;
        static (int, int) Solve(Tuple<long, long> generators)
            => (
                RunSequences(generators, 1, 1, 40),
                RunSequences(generators, DIVISOR_A, DIVISOR_B, 5)
            );

        static Tuple<long, long> GetInput(string filePath)
        {
            if (!File.Exists(filePath)) throw new FileNotFoundException(filePath);
            var matches = Regex.Matches(File.ReadAllText(filePath), @"\d+", RegexOptions.Multiline);
            return Tuple.Create(
                long.Parse(matches[0].Groups[0].Value),
                long.Parse(matches[1].Groups[0].Value));
        }

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