using System;
using static System.Console;
using System.IO;
using System.Diagnostics;
using System.Linq;
using System.Collections.Generic;
using System.Text.RegularExpressions;

namespace AoC
{
    readonly struct Edge
    {
        public Edge(string nodeA, string nodeB, int distance)
        {
            NodeA = nodeA;
            NodeB = nodeB;
            Distance = distance;
        }
        public string NodeA { get; }
        public string NodeB { get; }
        public int Distance { get; }
    }

    class Program
    {
        static IEnumerable<string> GetSingleNodes(IEnumerable<Edge> edges)
        {
            var nodes = new HashSet<string>();
            foreach (var path in edges)
            {
                nodes.Add(path.NodeA);
                nodes.Add(path.NodeB);
            }
            return nodes;
        }

        static int GetBestPath(IEnumerable<Edge> edges, IEnumerable<string> singleNodes, bool longest)
        {
            var length = singleNodes.Count();
            var stack = new Stack<(List<string> path, string current, int distance)>(singleNodes.Select(node => (new List<string>(new[] { node }), node, 0)));
            var bestDistance = longest ? 0 : int.MaxValue;
            while (stack.Any())
            {
                var (path, current, distance) = stack.Pop();
                foreach (var edge in edges.Where(edge => edge.NodeA == current || edge.NodeB == current))
                {
                    var nextNode = current == edge.NodeA ? edge.NodeB : edge.NodeA;
                    if (path.Contains(nextNode))
                        continue;
                    var newDistance = distance + edge.Distance;
                    if (!longest && newDistance > bestDistance)
                        continue;
                    var newPath = path.ToList();
                    newPath.Add(nextNode);
                    if (newPath.Count == length)
                        bestDistance = longest ? Math.Max(bestDistance, newDistance) : Math.Min(bestDistance, newDistance);
                    else
                        stack.Push((newPath, nextNode, newDistance));
                }
            }
            return bestDistance;
        }

        static (int, int) Solve(IEnumerable<Edge> edges)
        {
            var singleNodes = GetSingleNodes(edges);
            return (GetBestPath(edges, singleNodes, false), GetBestPath(edges, singleNodes, true));
        }


        static Regex lineRegex = new Regex(@"^(.*)\sto\s(.*)\s=\s(\d+)$", RegexOptions.Compiled);
        static IEnumerable<Edge> GetInput(string filePath)
            => !File.Exists(filePath) ? throw new FileNotFoundException(filePath)
            : File.ReadAllLines(filePath).Select(line =>
            {
                var match = lineRegex.Match(line);
                if (match.Success)
                    return new Edge(match.Groups[1].Value, match.Groups[2].Value, int.Parse(match.Groups[3].Value));
                throw new Exception($"Bad format '{line}'");
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