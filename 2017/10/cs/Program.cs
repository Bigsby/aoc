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
                    reverseMark = (reverseMark + 1) % MARKS_COUNT;
                }
                reverseMark = currentMark;
                foreach (var _ in Enumerable.Range(0, length))
                {
                    marks[reverseMark] = toReverse.Pop();
                    reverseMark = (reverseMark + 1) % MARKS_COUNT;
                }
                currentMark = (currentMark + length + skip) % MARKS_COUNT;
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

        static int[] SUFFIX = new[] { 17, 31, 73, 47, 23 };
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

        static (int, string) Solve(string puzzleInput)
            => (
                Part1(puzzleInput),
                Part2(puzzleInput)
            );

        static string GetInput(string filePath)
            => !File.Exists(filePath) ? throw new FileNotFoundException(filePath)
            : File.ReadAllText(filePath).Trim();

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