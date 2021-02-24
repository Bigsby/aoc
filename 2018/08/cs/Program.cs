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

        static Node GetRoot(IEnumerable<int> data)
        {
            data = new List<int>(data);
            return ReadNode(new Queue<int>(data));
        }

        static int Part1(IEnumerable<int> data) => GetMetadataSum(GetRoot(data));

        static int GetValue(Node node)
        {
            if (!node.children.Any())
                return node.metadata.Sum();
            var childrenCount = node.children.Count();
            return node.metadata.Where(index => index > 0 && index <= childrenCount).Sum(index => GetValue(node.children.ElementAt(index - 1)));
        }

        static int Part2(IEnumerable<int> data) => GetValue(GetRoot(data));

        static IEnumerable<int> GetInput(string filePath)
        {
            if (!File.Exists(filePath)) throw new FileNotFoundException(filePath);
            return File.ReadAllText(filePath).Trim().Split(" ").Select(int.Parse);
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