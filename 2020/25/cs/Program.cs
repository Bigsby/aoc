using System;
using static System.Console;
using System.IO;
using System.Diagnostics;

namespace AoC
{
    static class Program
    {
        const int BASE_SUBJECT_NUMBER = 7;
        const int DIVIDER = 20201227;

        static long GetNextValue(long value, long subjectNumber = BASE_SUBJECT_NUMBER)
            => (value * subjectNumber) % DIVIDER;

        static long GetLoopSize(long target)
        {
            var value = 1L;
            var cycle = 0;
            while (value != target)
            {
                cycle++;
                value = GetNextValue(value);
            }
            return cycle;
        }

        static long Transform(long subjectNumber, long cycles)
        {
            var value = 1L;
            while (cycles > 0)
            {
                cycles--;
                value = GetNextValue(value, subjectNumber);
            }
            return value;
        }

        static (long, object) Solve((long card, long door) puzzleInput)
            => (Transform(puzzleInput.card, GetLoopSize(puzzleInput.door)), null);

        static (long, long) GetInput(string filePath)
        {
            if (!File.Exists(filePath)) throw new FileNotFoundException(filePath);
            var lines = File.ReadAllLines(filePath);
            return (long.Parse(lines[0]), long.Parse(lines[1]));
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
