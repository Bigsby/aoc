using System;
using static System.Console;
using System.IO;
using System.Diagnostics;
using System.Linq;
using System.Collections.Generic;

namespace AoC
{
    using Grid = Dictionary<Coordinate, State>;

    struct Coordinate
    {
        public int X { get; }
        public int Y { get; }

        public Coordinate(int x, int y)
        {
            X = x;
            Y = y;
        }

        public override bool Equals(object obj)
            => obj is Coordinate a && a.X == X && a.Y == Y;
        public override int GetHashCode()
            => base.GetHashCode();
        public static bool operator ==(Coordinate a, Coordinate b)
            => a.Equals(b);
        public static bool operator !=(Coordinate a, Coordinate b)
            => !a.Equals(b);
        public static Coordinate operator +(Coordinate a, Coordinate b)
            => new Coordinate(a.X + b.X, a.Y + b.Y);
        public static Coordinate operator -(Coordinate a, Coordinate b)
            => new Coordinate(a.X - b.X, a.Y - b.Y);
        public static Coordinate operator *(Coordinate a, Coordinate b)
            => new Coordinate(a.X * b.Y - a.X * b.Y, a.Y * b.X + a.X * b.Y);
        public static implicit operator Coordinate(int i)
            => new Coordinate(i, 0);
        public static Coordinate YOne = new Coordinate(0, 1);

        public void Deconstruct(out int x, out int y)
        {
            x = X;
            y = Y;
        }
        public Coordinate RotateLeft(int turns = 1)
            => this * new Coordinate(0, turns);
        public Coordinate RotateRight(int turns = 1)
            => this * new Coordinate(0, -turns);
        public override string ToString()
            => $"({X}, {Y})";
    }

    enum State
    {
        Open,
        Tree,
        Lumberyard
    }

    static class Program
    {
        static Dictionary<char, State> RESOURCES = new Dictionary<char, State> {
            { '.', State.Open},
            { '|', State.Tree},
            { '#', State.Lumberyard }
        };

        static Coordinate[] NEIGHBOR_DIRECTIONS = new Coordinate[] {
            new Coordinate(-1, -1),
            new Coordinate( 0, -1),
            new Coordinate( 1, -1),
            new Coordinate(-1,  0),
            new Coordinate( 1,  0),
            new Coordinate(-1,  1),
            new Coordinate( 0,  1),
            new Coordinate( 1,  1),
        };
        static int GetCountAround(Coordinate position, Grid grid, State state)
            => NEIGHBOR_DIRECTIONS.Count(direction =>
                grid.ContainsKey(position + direction)
                &&
                grid[position + direction] == state);

        static Grid GetNextMinute(Grid grid)
        {
            var newState = new Grid();
            foreach (var (position, state) in grid.Select(pair => (pair.Key, pair.Value)))
                switch (state)
                {
                    case State.Open:
                        newState[position] = GetCountAround(position, grid, State.Tree) > 2 ? State.Tree : State.Open;
                        break;
                    case State.Tree:
                        newState[position] = GetCountAround(position, grid, State.Lumberyard) > 2
                            ? State.Lumberyard : State.Tree;
                        break;
                    case State.Lumberyard:
                        newState[position] = GetCountAround(position, grid, State.Lumberyard) > 0
                            && GetCountAround(position, grid, State.Tree) > 0
                            ? State.Lumberyard : State.Open;
                        break;
                }
            return newState;
        }

        static int GetResourceValue(Grid grid)
            => grid.Values.Count(v => v == State.Tree) * grid.Values.Count(v => v == State.Lumberyard);

        static bool TryFindRepeat(IEnumerable<Grid> previousGrids, Grid current, out int repeatIndex)
        {
            foreach (var (previous, index) in previousGrids.Select((previous, index) => (previous, index)))
                if (previous.All(pair => current[pair.Key] == pair.Value))
                {
                    repeatIndex = index;
                    return true;
                }
            repeatIndex = 0;
            return false;
        }

        static (int, int) Solve(Grid grid)
        {
            var previousGrids = new List<Grid>();
            previousGrids.Add(grid);
            var total = 1_000_000_000;
            var minute = 0;
            var part1Result = 0;
            var repeatFound = false;
            while (minute < total)
            {
                if (minute == 10)
                    part1Result = GetResourceValue(grid);
                minute++;
                grid = GetNextMinute(grid);
                if (!repeatFound && TryFindRepeat(previousGrids, grid, out var repeatIndex))
                {
                    repeatFound = true;
                    var period = minute - repeatIndex;
                    minute += ((total - minute) / period) * period;
                }
                previousGrids.Add(grid);
            }
            return (part1Result, GetResourceValue(grid));
        }

        static Grid GetInput(string filePath)
        {
            if (!File.Exists(filePath)) throw new FileNotFoundException(filePath);
            var grid = new Grid();
            foreach (var (line, y) in File.ReadLines(filePath).Select((line, y) => (line, y)))
                foreach (var (c, x) in line.Select((c, x) => (c, x)))
                    grid[new Coordinate(x, y)] = RESOURCES[c];
            return grid;
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
