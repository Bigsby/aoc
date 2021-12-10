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
        static IDictionary<char, char> MATCHES = new Dictionary<char, char> {
            { '(', ')' },
            { '[', ']' },
            { '{', '}' },
            { '<', '>' }
        };
        static IDictionary<char, int> ILLEGAL_CLOSING = new Dictionary<char, int> {
            { ')', 3 },
            { ']', 57 },
            { '}', 1197 },
            { '>', 25137 }
        };
        static IDictionary<char, ulong> CLOSING = new Dictionary<char, ulong> {
            { ')', 1 },
            { ']', 2 },
            { '}', 3 },
            { '>', 4 }
        };

        static (int, ulong) Solve(IEnumerable<string> lines)
        {
            var incompletePoints = new List<ulong>();
            var illegalPoints = 0;
            foreach (var line in lines)
            {
                var expectedClosing = new Stack<char>();
                var illegal = false;
                foreach (var c in line)
                {
                    if (c == '(' || c == '[' || c == '{' || c == '<')
                        expectedClosing.Push(MATCHES[c]);
                    else if (c != expectedClosing.Pop())
                    {
                        illegal = true;
                        illegalPoints += ILLEGAL_CLOSING[c];
                        break;
                    }
                }
                if (!illegal)
                {
                    var points = 0UL;
                    foreach (var c in expectedClosing)
                        points = points * 5 + CLOSING[c];
                    incompletePoints.Add(points);
                }
            }
            incompletePoints = incompletePoints.OrderBy(points => points).ToList();
            return (illegalPoints, incompletePoints[(int)(incompletePoints.Count() / 2)]);
        }

        static IEnumerable<string> GetInput(string filePath)
            => !File.Exists(filePath) ? throw new FileNotFoundException(filePath)
            : File.ReadAllLines(filePath);

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
