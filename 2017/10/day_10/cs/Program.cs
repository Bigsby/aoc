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
        const int MARKS_COUNT = 256;

        static (int[] marks, int currentMark, int skip) RunLengths(int[] marks, IEnumerable<int> lengths, int currentMark, int skip)
        {
            foreach (var length in lengths)
            {
                var toReverse = new Stack<int>();
                var reverseMark = currentMark;
                foreach (var _ in Enumerable.Range(0, length))
                {
                    toReverse.Push(marks.ElementAt(reverseMark));
                    reverseMark = reverseMark < MARKS_COUNT - 1 ? reverseMark + 1 : 0;
                }
                reverseMark = currentMark;
                foreach (var _ in Enumerable.Range(0, length))
                {
                    marks[reverseMark] = toReverse.Pop();
                    reverseMark = reverseMark < MARKS_COUNT - 1 ? reverseMark + 1 : 0;
                }
                foreach (var _ in Enumerable.Range(0, length + skip))
                    currentMark = currentMark < MARKS_COUNT - 1 ? currentMark + 1 : 0;
                skip++;
            }
            return (marks, currentMark, skip);
        }

        static int Part1(string puzzleInput)
        {
            var lengths = puzzleInput.Split(',').Select(int.Parse);
            var marks = Enumerable.Range(0, MARKS_COUNT).ToArray();
            (marks, _, _) = RunLengths(marks, lengths, 0, 0);
            return marks[0] * marks[1];
        }

        static int[] SUFFIX = new [] { 17, 31, 73, 47, 23 };
        static string Part2(string puzzleInput)
        {
            var lengths = puzzleInput.Select(c => (int)c);
            lengths = lengths.Concat(SUFFIX);
            var marks = Enumerable.Range(0, MARKS_COUNT).ToArray();
            var currentMark = 0;
            var skip = 0;
            foreach (var _ in Enumerable.Range(0, 64))
                (marks, currentMark, skip) = RunLengths(marks, lengths, currentMark, skip);
            var denseHash = Enumerable.Range(0, 16).Select(index => marks[new Range(index * 16, (index + 1) * 16)].Aggregate((soFar, mark) => soFar ^ mark));
            return string.Join("", denseHash.Select(knot => knot.ToString("x2")));
        }

        static string GetInput(string filePath)
        {
            if (!File.Exists(filePath)) throw new FileNotFoundException(filePath);
            return File.ReadAllText(filePath).Trim();
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