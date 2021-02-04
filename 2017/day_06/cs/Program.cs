using System;
using static System.Console;
using System.IO;
using System.Diagnostics;
using System.Linq;
using System.Collections.Generic;

namespace AoC
{
    class Program
    {
        static Tuple<int, int> RunCycles(IEnumerable<int> numbers)
        {
            var numbersLength = numbers.Count();
            var previousLists = new List<string>();
            var cycles = 0;
            var currentList = numbers.ToList();
            while (true)
            {
                var currentListString = string.Join(",", currentList);
                if (previousLists.Contains(currentListString))
                    return Tuple.Create(cycles, previousLists.IndexOf(currentListString));
                cycles++;
                previousLists.Add(currentListString);
                var updateIndex = -1;
                var maxNumber = 0;
                foreach (var (number, index) in currentList.Select((number, index) => (number, index)))
                    if (number > maxNumber)
                    {
                        maxNumber = number;
                        updateIndex = index;
                    }
                currentList[updateIndex] = 0;
                while (maxNumber > 0)
                {
                    updateIndex = updateIndex < numbersLength - 1 ? updateIndex + 1 : 0;
                    currentList[updateIndex]++;
                    maxNumber--;
                }
            }
        }

        static int Part1(IEnumerable<int> numbers) => RunCycles(numbers).Item1;

        static int Part2(IEnumerable<int> numbers)
        {
            var (cycles, first) = RunCycles(numbers);
            return cycles - first;
        }

        static IEnumerable<int> GetInput(string filePath)
        {
            if (!File.Exists(filePath)) throw new FileNotFoundException(filePath);
            return File.ReadAllText(filePath).Split("\t").Select(int.Parse);
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