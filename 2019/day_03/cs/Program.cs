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
    using Wire = IEnumerable<Tuple<char, int>>;
    
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

        static int Part1(Tuple<Wire,Wire> wires)
        {
            var (wireA, wireB) = wires;
            var wireAPoints = new HashSet<Complex>(GetWirePositions(wireA));
            return (int)GetWirePositions(wireB)
                .Where(point => wireAPoints.Contains(point))
                .Min(point => Math.Abs(point.Real) + Math.Abs(point.Imaginary));
        }

        static int Part2(Tuple<Wire,Wire> wires)
        {
            var (wireA, wireB) = wires;
            var wireAPoints = new Dictionary<Complex, int>();
            foreach (var (position, steps) in GetWirePositions(wireA).Select((position, index) => (position, index)))
                if (!wireAPoints.ContainsKey(position)) 
                    wireAPoints[position] = steps + 1;
            return GetWirePositions(wireB)
                .Select((position, steps) => (position, steps))
                .Where(pair => wireAPoints.ContainsKey(pair.Item1))
                .Min(pair => wireAPoints[pair.Item1] + pair.Item2 + 1);
        }

        static Regex directionRegex = new Regex(@"(?<direction>R|U|L|D)(?<distance>\d+)", RegexOptions.Compiled);
        static Wire ParseLine(string line)
        {
            foreach (Match match in directionRegex.Matches(line))
                yield return Tuple.Create(match.Groups["direction"].Value[0], int.Parse(match.Groups["distance"].Value));

        }

        static Tuple<Wire,Wire> GetInput(string filePath)
        {
            if (!File.Exists(filePath)) throw new FileNotFoundException(filePath);
            var lines = File.ReadAllLines(filePath);
            return Tuple.Create(ParseLine(lines[0]), ParseLine(lines[1]));
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