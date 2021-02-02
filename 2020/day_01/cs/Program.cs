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

        static int GetCombination(int[] numbers, int length)
        {
            foreach (var combination in Combinations(numbers, length)) {
                if (combination.Sum() == 2020)
                {
                    return combination.Aggregate(1, (soFar, number) => soFar * number);
                }
            }
            throw new Exception("Numbers not found");
        }

        static int Part1(int[] numbers)
        {
            return GetCombination(numbers, 2);
        }

        static object Part2(int[] numbers)
        {
            return GetCombination(numbers, 3);
        }

        static int[] GetInput(string filePath)
        {
            if (!File.Exists(filePath)) throw new FileNotFoundException(filePath);
            return File.ReadAllLines(filePath).Select(int.Parse).ToArray();
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