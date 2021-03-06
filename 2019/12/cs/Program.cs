﻿using System;
using static System.Console;
using System.IO;
using System.Diagnostics;
using System.Linq;
using System.Collections.Generic;
using System.Text.RegularExpressions;

namespace AoC
{
    class Moon : ICloneable
    {
        public (long x, long y, long z) Position { get; set; }
        public (long x, long y, long z) Velocity { get; set; } = (0L, 0L, 0L);
        public Moon(long x, long y, long z) =>
            Position = (x, y, z);

        static long GetDelta(long thisValue, long otherValue)
        {
            if (thisValue < otherValue)
                return 1;
            if (thisValue > otherValue)
                return -1;
            return 0;
        }

        static (long x, long y, long z) GetCoordinateDelta((long x, long y, long z) one, (long x, long y, long z) two)
            => (GetDelta(one.x, two.x), GetDelta(one.y, two.y), GetDelta(one.z, two.z));

        static (long x, long y, long z) Sum((long x, long y, long z) one, (long x, long y, long z) two)
            => (one.x + two.x, one.y + two.y, one.z + two.z);

        static long SumAbs((long x, long y, long z) coordinates)
            => Math.Abs(coordinates.x) + Math.Abs(coordinates.y) + Math.Abs(coordinates.z);

        public void UpdateVelocity(Moon otherMoon)
            => Velocity = Sum(Velocity, GetCoordinateDelta(Position, otherMoon.Position));

        public void UpdatePosition()
            => Position = Sum(Position, Velocity);

        public long GetTotalEnergy()
            => SumAbs(Position) * SumAbs(Velocity);

        public object Clone() => new Moon(Position.Item1, Position.Item2, Position.Item3);

        public override string ToString() => $"{Position} {Velocity}";
    }

    class Program
    {
        static IEnumerable<T[]> Combinations<T>(IEnumerable<T> source, int length)
        {
            T[] result = new T[length];
            Stack<int> stack = new Stack<int>();
            var data = source.ToArray();
            stack.Push(0);
            while (stack.Count > 0)
            {
                int resultIndex = stack.Count - 1;
                int dataIndex = stack.Pop();
                while (dataIndex < data.Length)
                {
                    result[resultIndex++] = data[dataIndex];
                    stack.Push(++dataIndex);
                    if (resultIndex == length)
                    {
                        yield return result;
                        break;
                    }
                }
            }
        }

        static void RunStep(Moon[] moons)
        {
            foreach (var combination in Combinations(Enumerable.Range(0, moons.Length), 2))
            {
                moons[combination[0]].UpdateVelocity(moons[combination[1]]);
                moons[combination[1]].UpdateVelocity(moons[combination[0]]);
            }
            foreach (var moon in moons)
                moon.UpdatePosition();
        }

        static long Part1(IEnumerable<Moon> moons)
        {
            var step = 1000;
            var moonArray = moons.Select(moon => (Moon)moon.Clone()).ToArray();
            while (step > 0)
            {
                step--;
                RunStep(moonArray);
            }
            return moonArray.Sum(moon => moon.GetTotalEnergy());
        }

        static Tuple<long[], long[]> BuildStateForCoordinate(Func<(long, long, long), long> getValueFunc,
            IEnumerable<Moon> moons)
            => Tuple.Create(
                moons.Select(moon => getValueFunc(moon.Position)).ToArray(),
                moons.Select(moon => getValueFunc(moon.Velocity)).ToArray());

        static bool AreArraysEqual(long[] one, long[] two)
            => Enumerable.Range(0, one.Length).All(index => one[index] == two[index]);

        static bool AreEqualStates(Tuple<long[], long[]> one, Tuple<long[], long[]> two)
             => AreArraysEqual(one.Item1, two.Item1) && AreArraysEqual(one.Item2, two.Item2);

        static Dictionary<char, Func<(long x, long y, long z), long>> COORDINATES =
            new Dictionary<char, Func<(long x, long y, long z), long>> {
            { 'x', t => t.x },
            { 'y', t => t.y },
            { 'z', t => t.z }
        };

        static long GCD(long a, long b)
        {
            while (a != 0 && b != 0)
            {
                if (a > b)
                    a %= b;
                else
                    b %= a;
            }
            return a | b;
        }

        static long Part2(IEnumerable<Moon> moons)
        {
            var step = 0;
            var moonsArray = moons.ToArray();
            var initialStates = COORDINATES.ToDictionary(
                coordinate => coordinate.Key,
                coordinate => BuildStateForCoordinate(coordinate.Value, moonsArray));
            var cycles = COORDINATES.ToDictionary(
                coordinate => coordinate.Key,
                _ => 0L
            );
            while (cycles.Values.Any(value => value == 0))
            {
                step++;
                RunStep(moonsArray);
                foreach (var coordinate in COORDINATES)
                {
                    if (cycles[coordinate.Key] == 0)
                    {
                        var currentState = BuildStateForCoordinate(coordinate.Value, moonsArray);
                        if (AreEqualStates(currentState, initialStates[coordinate.Key]))
                            cycles[coordinate.Key] = step;
                    }
                }
            }
            return cycles.Values.Aggregate((soFar, cycle) => soFar * cycle / GCD(soFar, cycle));
        }

        static (long, long) Solve(IEnumerable<Moon> moons)
            => (
                Part1(moons),
                Part2(moons)
            );

        static Regex lineRegex = new Regex(@"^<x=(?<x>-?\d+),\sy=(?<y>-?\d+),\sz=(?<z>-?\d+)>$", RegexOptions.Compiled);
        static IEnumerable<Moon> GetInput(string filePath)
            => !File.Exists(filePath) ? throw new FileNotFoundException(filePath)
            : File.ReadAllLines(filePath).Select(line =>
            {
                var match = lineRegex.Match(line);
                if (match.Success)
                    return new Moon(
                        long.Parse(match.Groups["x"].Value),
                        long.Parse(match.Groups["y"].Value),
                        long.Parse(match.Groups["z"].Value));
                throw new Exception($"Bad format '{line}'");
            });

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