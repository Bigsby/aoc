using System;
using static System.Console;
using System.IO;
using System.Diagnostics;
using System.Linq;
using System.Collections.Generic;
using System.Collections;

namespace AoC
{
    using Universe = Dictionary<Coordinate, bool>;
    class Coordinate : IEnumerable<int>
    {
        public Coordinate(params int[] coordinates) => _coordinates = coordinates;

        public int this[int index] 
        {
            get => _coordinates[index];
            set => _coordinates[index] = value;
        }

        public int Count => _coordinates.Length;

        public override bool Equals(object obj)
        {
            if (obj is Coordinate other)
            {
                for (var i = 0; i < _coordinates.Length; i++)
                    if (_coordinates[i] != other._coordinates[i])
                        return false;
                return true;
            }
            return false;
        }
        public override int GetHashCode() => string.Join(",", _coordinates).GetHashCode();
        public override string ToString() => "() " + string.Join(",", _coordinates) + " )";
        public IEnumerator<int> GetEnumerator() => (IEnumerator<int>)_coordinates.ToList().GetEnumerator();
        IEnumerator IEnumerable.GetEnumerator() => _coordinates.GetEnumerator();
        public static implicit operator Coordinate(int[] values) => new Coordinate(values);
        public static implicit operator Coordinate(List<int> values) => new Coordinate(values.ToArray());
        
        public static Coordinate operator +(Coordinate a, int i)
            => Enumerable.Range(0, a.Count).Select(index => a[index] + i).ToArray();
        public static Coordinate operator -(Coordinate a, int i)
            => Enumerable.Range(0, a.Count).Select(index => a[index] - i).ToArray();
        public static bool operator ==(Coordinate a, Coordinate b) => a.Equals(b);
        public static bool operator !=(Coordinate a, Coordinate b) => !a.Equals(b);
        public static Coordinate operator *(Coordinate a, int i)
        {
            var coordinatesList = a._coordinates.ToList();
            for (var count = 0; count < i; count++)
                coordinatesList.Insert(0, 0);
            return new Coordinate(coordinatesList.ToArray());
        }
        public static Coordinate operator ++(Coordinate a)
        {
            for (var index = 0; index < a.Count; index++)
                a[index]++;
            return a;
        }
        public static Coordinate operator --(Coordinate a)
        {
            for (var index = 0; index < a.Count; index++)
                a[index]--;
            return a;
        }
        private int[] _coordinates;
    }

    static class Program
    {
        static Coordinate NextCoordinateValue(Coordinate current, Coordinate lowerLimits, Coordinate upperLimits)
        {
            var result = current.ToArray();
            for (var index = current.Count - 1; index >= 0; index--)
                if (current[index] < upperLimits[index])
                {
                    result[index]++;
                    for (var overflow = index + 1; overflow < current.Count; overflow++)
                        result[overflow] = lowerLimits[overflow];
                    break;
                }
            return result;
        }

        static (Coordinate, Coordinate) GetLimits(Universe universe)
            => (
                Enumerable.Range(0, universe.Keys.First().Count).Select(index => universe.Keys.Min(coordinate => coordinate[index])).ToArray(),
                Enumerable.Range(0, universe.Keys.First().Count).Select(index => universe.Keys.Max(coordinate => coordinate[index])).ToArray()
            );
        
        static char[] OUTER_DIMENSIONS = new [] { 'z', 'w' };
        static void PrintUniverse(Universe universe)
        {
            var dimensionCount = universe.Keys.First().Count;
            var (lowerLimits, upperLimits) = GetLimits(universe);
            foreach (var coordinate in CycleCoordinates(lowerLimits, upperLimits))
            {
                if (coordinate[^1] == lowerLimits[^1] && coordinate[^2] == lowerLimits[^2])
                    Write("\n" + string.Join(", ", Enumerable.Range(0, dimensionCount - 2).Select(index => OUTER_DIMENSIONS[index] + "=" + coordinate[index])));
                if (coordinate[^1] == lowerLimits[^1])
                    WriteLine();
                Write(universe[coordinate] ? '#': '.');
            }
            WriteLine();
            ReadLine();
        }

        static IEnumerable<Coordinate> CycleCoordinates(Coordinate lowerLimit, Coordinate upperLimit)
        {
            var current = (Coordinate)lowerLimit.ToArray();
            current[^1]--;
            while (current != upperLimit)
            {
                current = NextCoordinateValue(current, lowerLimit, upperLimit);
                yield return current;
            }
        }

        static IEnumerable<Coordinate> GetNeighbors(Coordinate coordinate)
        {
            var lowerLimit = coordinate - 1;
            var upperLimit = coordinate + 1;
            var current = (Coordinate)lowerLimit.ToArray();
            current[^1]--;
            while (current != upperLimit)
            {
                current = NextCoordinateValue(current, lowerLimit, upperLimit);
                if (current != coordinate)
                    yield return current;
            }
        }

        static int GetActiveNeighborCount(Universe universe, Coordinate coordinate)
            => CycleCoordinates(coordinate - 1, coordinate + 1).Count(neighbor => 
                neighbor != coordinate
                && universe.ContainsKey(neighbor)
                && universe[neighbor]
            );

        static Universe NextCycle(Universe universe)
        {
            var newState = new Universe();
            var (lowerLimits, upperLimits) = GetLimits(universe);
            foreach (var coordinate in CycleCoordinates(--lowerLimits, ++upperLimits))
            {
                var activeNeighborCount = GetActiveNeighborCount(universe, coordinate);
                var newValue = false;
                if (universe.ContainsKey(coordinate) && universe[coordinate])
                    newValue = activeNeighborCount == 2 || activeNeighborCount == 3;
                else
                    newValue = activeNeighborCount == 3;
                newState[coordinate] = newValue;
            }
            return newState;
        }

        static int RunCycles(Universe universe)
        {
            foreach (var _ in Enumerable.Range(0, 6))
                universe = NextCycle(universe);
            return universe.Values.Count(v => v);
        }

        static int Part1(Universe universe) => RunCycles(universe);

        static int Part2(Dictionary<Coordinate, bool> universe)
            => RunCycles(universe.ToDictionary(pair => pair.Key * 1, pair => pair.Value));

        static Dictionary<Coordinate, bool> GetInput(string filePath)
        {
            if (!File.Exists(filePath)) throw new FileNotFoundException(filePath);
            var universe = new Dictionary<Coordinate, bool>();
            foreach (var (line, y) in File.ReadLines(filePath).Select((line, index) => (line, index)))
            {
                foreach (var (c, x) in line.Select((c, x) => (c, x)))
                    universe[new Coordinate(0, y, x)] = c == '#';
            }
            return universe;
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
