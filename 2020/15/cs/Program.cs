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
        static int GetNthTurn(IEnumerable<int> numbers, int turns)
        {
            var turn = 0;
            var occurrences = new Dictionary<int, (int lastOccurrence, int secondLastOccurence)>();
            foreach (var number in numbers)
                occurrences[number] = (++turn, 0);
            var lastNumber = numbers.Last();
            while (turn < turns)
            {
                turn++;
                var (lastOccurrence, secondLastOccurence) = occurrences[lastNumber];
                if (secondLastOccurence == 0)
                    lastNumber = 0;
                else
                    lastNumber = lastOccurrence - secondLastOccurence;
                if (occurrences.ContainsKey(lastNumber))
                    occurrences[lastNumber] = (turn, occurrences[lastNumber].lastOccurrence);
                else
                    occurrences[lastNumber] = (turn, 0);
            }
            return lastNumber;
        }

        static int Part1(IEnumerable<int> numbers) => GetNthTurn(numbers, 2020);

        static int Part2(IEnumerable<int> numbers) => GetNthTurn(numbers, 30_000_000);

        static IEnumerable<int> GetInput(string filePath)
        {
            if (!File.Exists(filePath)) throw new FileNotFoundException(filePath);
            return File.ReadAllText(filePath).Split(',').Select(int.Parse);
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