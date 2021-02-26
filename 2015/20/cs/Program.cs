using System;
using static System.Console;
using System.IO;
using System.Diagnostics;
using System.Linq;
using System.Collections.Generic;

namespace AoC
{
    static class Program
    {
        static IEnumerable<int> GetDivisors(int number)
        {
            var largeDivisors = new List<int>();
            var top = (int)Math.Sqrt(number) + 1;
            for (var i = 1; i < top; i++)
                if (number % i == 0)
                {
                    yield return i;
                    if (i * i != number)
                        largeDivisors.Add(number / i);
                }
            largeDivisors.Reverse();
            foreach (var divisor in largeDivisors)
                yield return divisor;
        }

        static int GetPresentCountForHouse(int number)
            => GetDivisors(number).Sum();

        static int Part1(int puzzleInput)
        {
            var houseNumber = 0;
            var presentsReceived = 0;
            var step = 2 * 3 * 5 * 7 * 11;
            var targetPresents = puzzleInput / 10;
            while (presentsReceived <= targetPresents)
            {
                houseNumber += step;
                presentsReceived = GetPresentCountForHouse(houseNumber);
            }
            return houseNumber;
        }

        static int GetPresentCountForHouse2(int number)
            => GetDivisors(number).Where(divisor => number / divisor < 50).Select(divisor => divisor * 11).Sum();

        static int Part2(int puzzleInput, int houseNumber)
        {
            var step = 1;
            var presentsReceived = 0;
            while (presentsReceived <= puzzleInput)
            {
                houseNumber += step;
                presentsReceived = GetPresentCountForHouse2(houseNumber);
            }
            return houseNumber;
        }

        static (int, int) Solve(int puzzleInput)
        {
            var part1Result = Part1(puzzleInput);
            return (
                part1Result,
                Part2(puzzleInput, part1Result)
            );
        }

        static int GetInput(string filePath)
            => !File.Exists(filePath) ? throw new FileNotFoundException(filePath)
            : int.Parse(File.ReadAllText(filePath));

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
