using System;
using static System.Console;
using System.IO;
using System.Diagnostics;
using System.Linq;
using System.Collections.Generic;
using System.Numerics;
using System.Text.RegularExpressions;

namespace AoC
{
    using FileSystem = Dictionary<Complex,(int size, int used)>;

    static class Program
    {
        static (Complex empty, IEnumerable<Complex> nonViable) GetEmptyAndNonViableNodes(FileSystem fileSystem)
        {
            var nodeNames = fileSystem.Keys;
            var empty = Complex.Zero;
            var nonViableNodes = new HashSet<Complex>();
            foreach (var thisNode in nodeNames)
            {
                var thisUsed = fileSystem[thisNode].used;
                if (thisUsed == 0)
                {
                    empty = thisNode;
                    continue;
                }
                foreach (var otherNode in nodeNames)
                {
                    if (otherNode == thisNode)
                        continue;
                    if (thisUsed > fileSystem[otherNode].size)
                        nonViableNodes.Add(thisNode);
                }
            }
            return (empty, nonViableNodes);
        }

        static int Part1(FileSystem fileSystem)
            => fileSystem.Count - GetEmptyAndNonViableNodes(fileSystem).nonViable.Count() - 1;

        static Complex[] DIRECTIONS = new [] { -Complex.ImaginaryOne, -1, 1, Complex.ImaginaryOne };
        static int GetStepsToTarget(IEnumerable<Complex> nodes, IEnumerable<Complex> nonViable, Complex start, Complex destination)
        {
            var visited = new HashSet<Complex>();
            visited.Add(start);
            var queue = new Queue<(Complex, int)>();
            queue.Enqueue((start, 0));
            while (queue.Any())
            {
                var (currentNode, length) = queue.Dequeue();
                foreach (var newNode in DIRECTIONS.Select(direction => currentNode + direction))
                    if (newNode == destination)
                        return length + 1;
                    else if (nodes.Contains(newNode) && !visited.Contains(newNode) && !nonViable.Contains(newNode))
                    {
                        visited.Add(newNode);
                        queue.Enqueue((newNode, length + 1));
                    }
            }
            throw new Exception("Path not found");
        }

        static int Part2(FileSystem fileSystem)
        {
            var (empty, nonViable) = GetEmptyAndNonViableNodes(fileSystem);
            var nodes = fileSystem.Keys.ToList();
            var emptyDestination = (int)nodes.Max(n => n.Real);
            return GetStepsToTarget(nodes, nonViable, empty, emptyDestination) + (emptyDestination - 1) * 5;
        }

        static Regex lineRegex = new Regex(@"^/dev/grid/node-x(?<x>\d+)-y(?<y>\d+)\s+(?<size>\d+)T\s+(?<used>\d+)", RegexOptions.Compiled);
        static FileSystem GetInput(string filePath)
        {
            if (!File.Exists(filePath)) throw new FileNotFoundException(filePath);
            var fileSystem = new FileSystem();
            foreach (var line in File.ReadLines(filePath))
            {
                var match = lineRegex.Match(line);
                if (match.Success)
                    fileSystem[new Complex(int.Parse(match.Groups["x"].Value), int.Parse(match.Groups["y"].Value))] =
                        (int.Parse(match.Groups["size"].Value), int.Parse(match.Groups["used"].Value));
            }
            return fileSystem;
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
