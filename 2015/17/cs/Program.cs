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

        static (int, int) Solve(IEnumerable<int> containers)
        {
            var validCombinations = GetValidCombinations(containers);
            var minCount = validCombinations.Min(combination => combination.Count());
            return (
                validCombinations.Count(),
                validCombinations.Count(combination => combination.Count() == minCount)
            );
        }

        static IEnumerable<int> GetInput(string filePath)
            => !File.Exists(filePath) ? throw new FileNotFoundException(filePath)
            : File.ReadLines(filePath).Select(int.Parse);

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
