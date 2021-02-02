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
        static int Part1(string[] ids)
        {
            var twiceCount = 0;
            var thriceCount = 0;
            foreach (var id in ids)
            {
                var idCounts = id.Select(c => id.Count(c0 => c0 == c));
                twiceCount += idCounts.Contains(2) ? 1 : 0;
                thriceCount += idCounts.Contains(3) ? 1 : 0;
            }
            return twiceCount * thriceCount;
        }

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

        static string Part2(string[] ids)
        {
            foreach (var combination in Combinations(ids, 2))
            {
                var id1 = combination[0];
                var id2 = combination[1];
                var differences = Enumerable.Range(0, id1.Count()).Where(index => id1[index] != id2[index]);
                if (differences.Count() == 1)
                {
                    var differenceIndex = differences.First();
                    return id1[Range.EndAt(differenceIndex)] + id1[Range.StartAt(differenceIndex + 1)];
                }
            }
            throw new Exception("Ids differencing 1 not found");
        }

        static string[] GetInput(string filePath)
        {
            if (!File.Exists(filePath)) throw new FileNotFoundException(filePath);
            return File.ReadAllLines(filePath).Select(line => line.Trim()).ToArray();
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