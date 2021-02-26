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
    using Directions = IEnumerable<string>;
    using Floor = Dictionary<Complex, bool>;

    static class Program
    {
        static Dictionary<string, Complex> DIRECTIONS = new Dictionary<string, Complex> {
            { "e",  new Complex( 1,  0) },
            { "se", new Complex( 0,  1) },
            { "sw", new Complex(-1,  1) },
            { "w",  new Complex(-1,  0) },
            { "ne", new Complex( 1, -1) },
            { "nw", new Complex( 0, -1) },
        };

        static Floor FlipInitiaTiles(IEnumerable<Directions> filePaths)
        {
            var floor = new Floor();
            foreach (var path in filePaths)
            {
                var current = Complex.Zero;
                foreach (var direction in path)
                    current += DIRECTIONS[direction];
                if (floor.ContainsKey(current))
                    floor[current] = !floor[current];
                else
                    floor[current] = true;
            }
            return floor;
        }

        static IEnumerable<Complex> GetNeighbors(Complex tile)
            => DIRECTIONS.Values.Select(direction => tile + direction);

        static int GetBlackCount(IEnumerable<Complex> neighbors, Floor floor)
            => neighbors.Count(neighbor => floor.ContainsKey(neighbor) && floor[neighbor]);

        static bool GetTileState(Complex tile, Floor floor)
            => floor.ContainsKey(tile) && floor[tile];

        static bool GetNewState(Complex tile, Floor floor)
        {
            var adjacentBlackCount = GetBlackCount(GetNeighbors(tile), floor);
            var tileState = GetTileState(tile, floor);
            if (tileState && adjacentBlackCount == 0 || adjacentBlackCount > 2)
                return false;
            return (!tileState && adjacentBlackCount == 2) || tileState;
        }

        static Floor RunDay(Floor floor)
        {
            var newFloor = new Floor();
            var edgesToTest = new List<Complex>();
            foreach (var tile in floor.Keys)
            {
                edgesToTest.AddRange(GetNeighbors(tile).Where(neighbor => !floor.ContainsKey(neighbor)));
                newFloor[tile] = GetNewState(tile, floor);
            }
            foreach (var tile in edgesToTest.ToHashSet())
                newFloor[tile] = GetNewState(tile, floor);
            return newFloor;
        }

        static int Part2(Floor floor)
        {
            foreach (var _ in Enumerable.Range(0, 100))
                floor = RunDay(floor);
            return floor.Values.Count(tile => tile);
        }

        static (int, int) Solve(IEnumerable<Directions> filePaths)
        {
            var floor = FlipInitiaTiles(filePaths);
            return (
                floor.Values.Count(tile => tile),
                Part2(floor)
            );
        }

        static Regex lineRegex = new Regex(@"e|se|sw|w|nw|ne", RegexOptions.Compiled);
        static IEnumerable<Directions> GetInput(string filePath)
            => !File.Exists(filePath) ? throw new FileNotFoundException(filePath)
            : File.ReadLines(filePath).Select(line => lineRegex.Matches(line).Select(match => match.Value));

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
