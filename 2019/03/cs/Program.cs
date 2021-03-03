using System;
using static System.Console;
using System.IO;
using System.Diagnostics;
using System.Linq;
using System.Collections.Generic;
using System.Text.RegularExpressions;
using System.Numerics;

namespace AoC
{
    using Wire = IEnumerable<(char, int)>;

    class Program
    {
        static Dictionary<char, Complex> STEPS = new Dictionary<char, Complex> {
            { 'R', 1 },
            { 'U', -Complex.ImaginaryOne },
            { 'L', -1 },
            { 'D', Complex.ImaginaryOne }
        };
        static IEnumerable<Complex> GetWirePositions(Wire wire)
        {
            Complex position = 0;
            foreach (var (direction, distance) in wire)
                foreach (var _ in Enumerable.Range(0, distance))
                {
                    position += STEPS[direction];
                    yield return position;
                }
        }

        static int Part1((Wire, Wire) wires)
        {
            var (wireA, wireB) = wires;
            var wireAPoints = new HashSet<Complex>(GetWirePositions(wireA));
            return (int)GetWirePositions(wireB)
                .Where(point => wireAPoints.Contains(point))
                .Min(point => Math.Abs(point.Real) + Math.Abs(point.Imaginary));
        }

        static int Part2((Wire, Wire) wires)
        {
            var (wireA, wireB) = wires;
            var wireAPoints = new Dictionary<Complex, int>();
            foreach (var (position, steps) in GetWirePositions(wireA).Select((position, index) => (position, index)))
                if (!wireAPoints.ContainsKey(position))
                    wireAPoints[position] = steps + 1;
            return GetWirePositions(wireB)
                .Select((position, steps) => (position, steps))
                .Where(pair => wireAPoints.ContainsKey(pair.position))
                .Min(pair => wireAPoints[pair.position] + pair.steps + 1);
        }

        static (int, int) Solve((Wire, Wire) wires)
            => (
                Part1(wires),
                Part2(wires)
            );

        static Regex directionRegex = new Regex(@"(?<direction>R|U|L|D)(?<distance>\d+)", RegexOptions.Compiled);
        static Wire ParseLine(string line)
            => directionRegex.Matches(line)
                .Select(match =>
                (
                    match.Groups["direction"].Value[0],
                    int.Parse(match.Groups["distance"].Value
                )));

        static (Wire, Wire) GetInput(string filePath)
        {
            if (!File.Exists(filePath)) throw new FileNotFoundException(filePath);
            var lines = File.ReadAllLines(filePath);
            return (ParseLine(lines[0]), ParseLine(lines[1]));
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