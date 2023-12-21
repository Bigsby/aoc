using System;
using static System.Console;
using System.IO;
using System.Diagnostics;
using System.Linq;
using System.Collections.Generic;
using System.Numerics;

namespace AoC
{
    using Input = Tuple<string, Dictionary<string, Tuple<string, string>>>;

    static class Program
    {
        static int Part1(Input puzzleInput)
        { 
            var (directions, nodes) = puzzleInput;
            var current = "AAA";
            var steps = 0;
            while (current != "ZZZ")
            {
                var direction = directions[steps % directions.Length];
                var next = nodes[current];
                current = direction == 'L' ? next.Item1 : next.Item2;
                steps++;
            }
            return steps;
        }

        static BigInteger GetSteps(Input puzzleInput, string start)
        {
            var (directions, nodes) = puzzleInput;
            var current = start;
            var steps = 0;
            while (!current.EndsWith("Z"))
            {
                var direction = directions[steps % directions.Length];
                var next = nodes[current];
                current = direction == 'L' ? next.Item1 : next.Item2;
                steps++;
            }
            return steps;
        }

        static BigInteger GreatestCommonFactor(BigInteger a, BigInteger b)
        {
            while (b != 0)
            {
                BigInteger temp = b;
                b = a % b;
                a = temp;
            }
            return a;
        }

        static BigInteger LeastCommonMultiple(BigInteger a, BigInteger b)
            => (a / GreatestCommonFactor(a, b)) * b;

        static BigInteger Part2(Input puzzleInput)
        {
            var (directions, nodes) = puzzleInput;
            return nodes.Keys.Where(node => node.EndsWith("A"))
                .Select(node => GetSteps(puzzleInput, node))
                .Aggregate(new BigInteger(1), (soFar, next) => LeastCommonMultiple(soFar, next));
        }

        static (int, BigInteger) Solve(Input puzzleInput)
            => (Part1(puzzleInput), Part2(puzzleInput));

        static Input GetInput(string filePath)
        {
            if (!File.Exists(filePath)) 
                throw new FileNotFoundException(filePath);
            var lines = File.ReadAllLines(filePath);
            var nodes = new Dictionary<string, Tuple<string, string>>();
            foreach (var line in lines.Skip(2))
            {
                var split = line.Split(" = ");
                var next = split[1].Trim(new [] { '(', ')' }).Split(", ");
                nodes[split[0]] = Tuple.Create(next[0], next[1]);
            }
            return Tuple.Create(lines[0], nodes);
        }

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
