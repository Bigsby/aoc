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
        const int TARGET_TOTAL = 150;

        static IEnumerable<T[]> Combinations<T>(IEnumerable<T> source, int length)
        {
            T[] result = new T[length];
            Stack<int> stack = new Stack<int>();
            var data = source.ToArray();
            stack.Push(0);
            while (stack.Count > 0)
            {
                int resultIndex = stack.Count - 1;
                int dataIndex = stack.Pop();
                while (dataIndex < data.Length) 
                {
                    result[resultIndex++] = data[dataIndex];
                    stack.Push(++dataIndex);
                    if (resultIndex == length) 
                    {
                        yield return result;
                        break;
                    }
                }
            }
        }

        static IEnumerable<IEnumerable<int>> GetValidCombinations(IEnumerable<int> containers)
        {
            var validCombinations = new List<IEnumerable<int>>();
            for (var containerCount = 2; containerCount < containers.Count(); containerCount++)
                foreach (var combination in Combinations(containers, containerCount))
                    if (combination.Sum() == TARGET_TOTAL)
                        validCombinations.Add(combination);
            return validCombinations;
        }

        static int Part1(IEnumerable<int> containers) => GetValidCombinations(containers).Count();

        static int Part2(IEnumerable<int> containers)
        {
            var validCombinations = GetValidCombinations(containers);
            var minCount = validCombinations.Min(combination => combination.Count());
            return validCombinations.Count(combination => combination.Count() == minCount);
        }

        static IEnumerable<int> GetInput(string filePath)
        {
            if (!File.Exists(filePath)) throw new FileNotFoundException(filePath);
            return File.ReadLines(filePath).Select(int.Parse);
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
