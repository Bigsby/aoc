using System;
using static System.Console;
using System.IO;
using System.Diagnostics;
using System.Linq;
using System.Collections.Generic;

namespace AoC
{
    record struct Edge(string nodeA, string nodeB);
    static class Program
    {
        static int FindPaths(IEnumerable<Edge> edges, bool repeat)
        {
            int completePathCount = 0;
            Queue<(string, string, bool)> queue = new Queue<(string, string, bool)>();
            queue.Enqueue(("start", "start", !repeat));
            while (queue.Any())
            {
                var (node, path, smallRepeat) = queue.Dequeue();
                if (node == "end")
                    completePathCount++;
                else
                    foreach (var edge in edges.Where(edge => edge.nodeA == node || edge.nodeB == node))
                    {
                        var other = edge.nodeA == node ? edge.nodeB : edge.nodeA;
                        if (!(other == "start" || (smallRepeat && other.ToLowerInvariant() == other && path.Contains(other))))
                            queue.Enqueue((other, $"{path},{other}", smallRepeat || (other == other.ToLowerInvariant() && path.Contains(other))));
                    }
            }
            return completePathCount;
        }

        static (int, int) Solve(IEnumerable<Edge> edges)
            => (FindPaths(edges, false), FindPaths(edges, true));

        static IEnumerable<Edge> GetInput(string filePath)
            => !File.Exists(filePath) ? throw new FileNotFoundException(filePath)
            : File.ReadAllLines(filePath).Select(line => {
                var split = line.Split("-");
                return new Edge(split[0], split[1]);
            });

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
