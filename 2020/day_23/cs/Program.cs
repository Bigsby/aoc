using System;
using static System.Console;
using System.IO;
using System.Diagnostics;
using System.Linq;
using System.Collections.Generic;

namespace AoC
{
    class Node
    {
        public long Value { get; init; }
        public Node Next { get; set; }
        public Node(long value)
        {
            Value = value;
            Next = this;
        }
    }

    static class Program
    {
        static (Node, Node[]) BuildLinkedList(IEnumerable<long> cups)
        {
            Node start, previous, last;
            start = previous = last = new Node(cups.First());
            var values = Enumerable.Range(0, cups.Count()).Select(_ => start).ToArray();
            values[start.Value - 1] = start;
            foreach (var cup in cups.Skip(1))
            {
                last = new Node(cup);
                previous.Next = last;
                values[last.Value - 1] = last;
                previous = last;
            }
            last.Next = start;
            return (start, values);
        }

        static Node PlayGame(IEnumerable<long> cups, int moves)
        {
            var (start, values) = BuildLinkedList(cups);
            var maxValue = cups.Max();
            var current = start;
            while (moves > 0)
            {
                moves--;
                var firstRemoved = current.Next;
                var lastRemoved = firstRemoved.Next.Next;
                var removedValues = new [] { firstRemoved.Value, firstRemoved.Next.Value, lastRemoved.Value };
                current.Next = lastRemoved.Next;
                var destinationValue = current.Value - 1;
                while (removedValues.Contains(destinationValue) || destinationValue < 1)
                {
                    destinationValue--;
                    if (destinationValue < 0)
                        destinationValue = maxValue;
                }
                var destinationLink = values[destinationValue - 1];
                lastRemoved.Next = destinationLink.Next;
                destinationLink.Next = firstRemoved;
                current = current.Next;
            }
            return values[0];
        }

        static string Part1(IEnumerable<long> cups)
        {
            var oneNode = PlayGame(cups, 100);
            var result = new List<long>();
            var currentNode = oneNode.Next;
            while (currentNode.Value != 1)
            {
                result.Add(currentNode.Value);
                currentNode = currentNode.Next;
            }
            return string.Join("", result);
        }

        static long Part2(IEnumerable<long> cups)
        {
            cups = cups.Concat(Enumerable.Range(10, 1_000_000 - 9).Select(c => (long)c));
            var oneNode = PlayGame(cups, 10_000_000);
            return oneNode.Next.Value * oneNode.Next.Next.Value; 
        }

        static IEnumerable<long> GetInput(string filePath)
        {
            if (!File.Exists(filePath)) throw new FileNotFoundException(filePath);
            return File.ReadAllText(filePath).Trim().Select(c => long.Parse(c.ToString()));
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
