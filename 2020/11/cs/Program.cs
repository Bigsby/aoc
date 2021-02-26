using System;
using static System.Console;
using System.IO;
using System.Diagnostics;
using System.Linq;
using System.Collections.Generic;
using System.Numerics;

namespace AoC
{
    using Grid = Dictionary<Complex, State>;
    enum State
    {
        Occupied,
        Empty,
        Floor
    }

    class Program
    {
        static Complex I = Complex.ImaginaryOne;
        static Complex[] NEIGHBOR_DIRECTIONS = new [] {
            - 1 - 1 * I,
                - 1 * I,
            + 1 - 1 * I,
            - 1,
            + 1,
            - 1 + 1 * I,
                + 1 * I,
            + 1 + 1 * I
        };

        static int GetOccupiedCount(Grid grid, Complex position, Func<Grid, Complex, Complex, Complex> getNeighborFunc)
        {
            var total = 0;
            foreach (var neighbor in NEIGHBOR_DIRECTIONS
                        .Select(direction => getNeighborFunc(grid, position, direction)))
                if (grid.ContainsKey(neighbor) && grid[neighbor] == State.Occupied)
                    total++;
            return total;
        }

        static (bool changed, State newPositionState) GetPositionNewState(Grid grid, Complex position, int tolerance, Func<Grid, Complex, Complex, Complex> getNeighborFunc)
        {
            var currentState = grid[position];
            if (currentState == State.Floor)
                return (false, State.Floor);
            var occupiedCount = GetOccupiedCount(grid, position, getNeighborFunc);
            if (currentState == State.Empty && occupiedCount == 0)
                return (true, State.Occupied);
            if (currentState == State.Occupied && occupiedCount > tolerance)
                return (true, State.Empty);
            return (false, currentState);
        }

        static (int changedCount, Grid newState) GetNextState(Grid grid, int tolerance, Func<Grid, Complex, Complex, Complex> getNeighborFunc)
        {
            var newState = new Grid(grid);
            var changedCount = 0;
            foreach (var position in grid.Keys)
            {
                var (changed, newPositionState) = GetPositionNewState(grid, position, tolerance, getNeighborFunc);
                if (changed)
                    changedCount++;
                newState[position] = newPositionState;
            }
            return (changedCount, newState);
        }

        static int RunGrid(Grid grid, int tolerance, Func<Grid, Complex, Complex, Complex> getNeighborFunc)
        {
            var proccessGrid = new Grid(grid);
            var changed = 1;
            while (changed != 0)
                (changed, proccessGrid) = GetNextState(proccessGrid, tolerance, getNeighborFunc);
            return proccessGrid.Values.Count(state => state == State.Occupied);
        }

        static Complex GetDirectionalNeighbor(Grid grid, Complex position, Complex direction)
        {
            position += direction;
            while (grid.ContainsKey(position) && grid[position] == State.Floor)
                position += direction;
            return position;
        }
        
        static (int, int) Solve(Grid grid)
            => (
                RunGrid(grid, 3, (_, position, direction) => position + direction),
                RunGrid(grid, 4, GetDirectionalNeighbor)
            );

        static Dictionary<char, State> CHAR_STATES = new Dictionary<char, State> {
            { '.', State.Floor },
            { 'L', State.Empty },
            { '#', State.Occupied }
        };
        static Grid GetInput(string filePath)
        {
            if (!File.Exists(filePath)) throw new FileNotFoundException(filePath);
            var grid = new Grid();
            foreach (var (line, y) in File.ReadAllLines(filePath).Select((line, index) => (line, index)))
                foreach (var (c, x) in line.Select((c, index) => (c, index)))
                    grid[x + y * I] = CHAR_STATES[c];
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