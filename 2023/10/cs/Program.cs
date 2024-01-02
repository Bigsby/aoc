using System;
using static System.Console;
using System.IO;
using System.Diagnostics;
using System.Linq;
using System.Collections.Generic;
using System.Numerics;

namespace AoC
{
    using Input = Tuple<Complex, Dictionary<Complex, TileType>>; 
    
    [Flags]
    enum Direction 
    {
        North  = 1 << 0,
        East = 1 << 1,
        South = 1 << 2,
        West = 1 << 3
    }

    enum TileType 
    {
        None = 0,
        NorthEast = Direction.North | Direction.East,
        NorthSouth = Direction.North | Direction.South,
        NorthWest = Direction.North | Direction.West,
        EastWest = Direction.East | Direction.West,
        SouthEast = Direction.South | Direction.East,
        SouthWest = Direction.South | Direction.West
    }


    static class Program
    {
        static Complex NORTH = -Complex.ImaginaryOne;
        static Complex SOUTH = Complex.ImaginaryOne;
        static Complex WEST = -Complex.One;
        static Complex EAST = Complex.One;


        static (Complex, Complex) GetDirections(TileType type)
        {
            return type switch {
                TileType.NorthEast => (Complex.One, -Complex.ImaginaryOne),
                TileType.NorthSouth => (Complex.ImaginaryOne, -Complex.ImaginaryOne),
                TileType.NorthWest => (-Complex.One, -Complex.ImaginaryOne),
                TileType.EastWest => (-Complex.One, Complex.One),
                TileType.SouthEast => (Complex.One, Complex.ImaginaryOne),
                TileType.SouthWest => (-Complex.One, Complex.ImaginaryOne),
                _ => throw new Exception($"{type} tile type should not be exist.")
            };
        }

        static IEnumerable<(Complex, Direction, Direction)> NEIGHBOR_TESTS = new []
        {
            (EAST, Direction.West, Direction.East),
            (WEST, Direction.East, Direction.West),
            (SOUTH, Direction.North, Direction.South),
            (NORTH, Direction.South, Direction.North)
        };
        
        static TileType GetStartTile(Complex start, Dictionary<Complex, TileType> tiles)
        {
            var type = 0;
            foreach (var (direction, neighborTest, startDirection) in NEIGHBOR_TESTS)
                if (tiles.TryGetValue(start + direction, out var neighborType) && neighborType.HasFlag((TileType)neighborTest))
                    type |= (int)startDirection;
            return (TileType)type;
        }

        static Complex GetNextDirection(Complex previous, TileType type)
        {
            var (nextOne, nextTwo) = GetDirections(type);
            if (previous == NORTH)
                return nextOne == SOUTH ? nextTwo : nextOne;
            if (previous == SOUTH)
                return nextOne == NORTH ? nextTwo : nextOne;
            if (previous == EAST)
                return nextOne == WEST ? nextTwo : nextOne;
            if (previous == WEST)
                return nextOne == EAST ? nextTwo : nextOne;
            throw new Exception($"Directions {previous} not expected.");
        }

        static (int, IEnumerable<Complex>) Part1(Input puzzleInput)
        { 
            var (start, tiles) = puzzleInput;
            var startTile = GetStartTile(start, tiles);
            var current = start;
            var (_, nextDirection) = GetDirections(startTile);
            var steps = 0;
            var loop = new List<Complex>();
            do {
                loop.Add(current);
                current += nextDirection;
                steps++;
                nextDirection = GetNextDirection(nextDirection, tiles[current]);
            } while (current != start);
            return (steps / 2 + (steps % 2 == 1 ? 1 : 0), loop);
        }

        static bool IsInside(IEnumerable<Complex> loop, Complex coordinate)
        {
            var inside = false;
            int i, j;
            var loopArray = loop.ToArray();
            for (i = 0, j = loopArray.Length - 1; i < loopArray.Length; j = i++)
            {
                var ith = loopArray[i];
                var jth = loopArray[j];
                if(ith.Imaginary > coordinate.Imaginary ^ jth.Imaginary > coordinate.Imaginary
                    && 
                    (coordinate.Real < (jth.Real - ith.Real) * (coordinate.Imaginary - ith.Imaginary) / (jth.Imaginary - ith.Imaginary) + ith.Real))
                    inside = !inside;
            }
            return inside;
        }

        static int Part2(IEnumerable<Complex> loop, Dictionary<Complex, TileType> tiles)
        {
            var (maxX, maxY) = (loop.Max(c => c.Real) + 1, loop.Max(c => c.Imaginary) + 1);
            var enclosed = 0;
            for (var y = 0; y < maxY; y++)
            {
                for (var x = 0; x < maxX; x++)
                {
                    var coordinate = new Complex(x, y);
                    if (loop.Contains(coordinate))
                        continue;
                    enclosed += IsInside(loop, coordinate) ? 1 : 0;
                }
            }
            return enclosed;
        }

        static (int, int) Solve(Input puzzleInput)
        {
            var (start, tiles) = puzzleInput;
            tiles[start] = GetStartTile(start, tiles);
            var (furthest, loop) = Part1(puzzleInput);
            return (furthest, Part2(loop, tiles));
        }

        static Input GetInput(string filePath)
        {

            if (!File.Exists(filePath)) 
                throw new FileNotFoundException(filePath);
            var tiles = new Dictionary<Complex, TileType>();
            var start = Complex.NaN;

            var y = 0;
            foreach (var line in File.ReadAllLines(filePath))
            {
                var x = 0;
                foreach (var c in line.Trim())
                {
                    switch (c)
                    {
                        case '.':
                            break;
                        case 'S':
                            start = new Complex(x, y);
                            break;
                        default:
                            tiles[new Complex(x, y)] = c switch 
                            {
                                '|' => TileType.NorthSouth,
                                '-' => TileType.EastWest,
                                'L' => TileType.NorthEast,
                                'J' => TileType.NorthWest,
                                '7' => TileType.SouthWest,
                                'F' => TileType.SouthEast,
                                _ => throw new Exception($"{c} tile unknown!")
                            };
                            break;
                    }
                    x++;
                }
                y++;
            }

            return start != Complex.NaN ? Tuple.Create(start, tiles) : throw new Exception("Start not found!");
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
