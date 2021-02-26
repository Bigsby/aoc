using System;
using static System.Console;
using System.IO;
using System.Diagnostics;
using System.Linq;
using System.Collections.Generic;

namespace AoC
{
    record Node(IEnumerable<Node> children, IEnumerable<int> metadata);

    class Program
    {
        static Node ReadNode(Queue<int> data)
        {
            var childrenCount = data.Dequeue();
            var metadataCount = data.Dequeue();
            var children = new List<Node>();
            var metadata = new List<int>();
            foreach (var _ in Enumerable.Range(0, childrenCount))
                children.Add(ReadNode(data));
            foreach (var _ in Enumerable.Range(0, metadataCount))
                metadata.Add(data.Dequeue());
            return new Node(children, metadata);
        }

        static int GetMetadataSum(Node node) => node.metadata.Sum() + node.children.Sum(GetMetadataSum);

        static int GetValue(Node node)
        {
            if (!node.children.Any())
                return node.metadata.Sum();
            var childrenCount = node.children.Count();
            return node.metadata.Where(index => 
                index > 0 && index <= childrenCount).Sum(index => GetValue(node.children.ElementAt(index - 1)));
        }

        static (int, int) Solve(IEnumerable<int> data)
        {
            var root = ReadNode(new Queue<int>(data));
            return (
                GetMetadataSum(root),
                GetValue(root)
            );
        }

        static IEnumerable<int> GetInput(string filePath)
            => !File.Exists(filePath) ? throw new FileNotFoundException(filePath)
            : File.ReadAllText(filePath).Trim().Split(" ").Select(int.Parse);

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