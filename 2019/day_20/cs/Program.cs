using System;
using static System.Console;
using System.IO;
using System.Diagnostics;
using System.Linq;
using System.Collections.Generic;
using System.Text.RegularExpressions;

namespace AoC
{
    using Portals = Dictionary<Coordinate, string>;
    using Maze = IEnumerable<Coordinate>;

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
            => ToString().GetHashCode();
        public static bool operator ==(Coordinate a, Coordinate b)
            => a.Equals(b);
        public static bool operator !=(Coordinate a, Coordinate b)
            => !a.Equals(b);
        public static Coordinate operator +(Coordinate a, Coordinate b)
            => new Coordinate(a.X + b.X, a.Y + b.Y);
        public static Coordinate operator +(Coordinate a)
            => a;
        public static Coordinate operator -(Coordinate a, Coordinate b)
            => new Coordinate(a.X - b.X, a.Y - b.Y);
        public static Coordinate operator -(Coordinate a)
            => new Coordinate(-a.X, -a.Y);
        public static Coordinate operator *(Coordinate a, Coordinate b)
            => new Coordinate(a.X * b.X - a.Y * b.Y, a.Y * b.X + a.X * b.Y);
        public static implicit operator Coordinate(int i)
            => new Coordinate(i, 0);
        public static Coordinate YOne = new Coordinate(0, 1);
        public static Coordinate Zero = new Coordinate(0, 0);
        public void Deconstruct(out int x, out int y)
        {
            x = X;
            y = Y;
        }
        public override string ToString()
            => $"({X}, {Y})";
    }

    static class Program
    {
        static Coordinate[] DIRECTIONS = new[] { Coordinate.YOne, -Coordinate.YOne, 1, -1 };

        static int Part1((Maze, Portals, Coordinate, Coordinate) data)
        {
            var (maze, portals, start, end) = data;
            var visited = new List<Coordinate>();
            visited.Add(start);
            var queue = new Queue<(Coordinate, int)>();
            queue.Enqueue((start, 1));
            while (queue.Any())
            {
                var (position, distance) = queue.Dequeue();
                var newPositions = new List<Coordinate>();
                if (portals.TryGetValue(position, out var label))
                    newPositions.Add(portals.First(pair => pair.Key != position && pair.Value == label).Key);
                newPositions.AddRange(DIRECTIONS.Select(direction => direction + position));
                foreach (var newPosition in newPositions)
                {
                    if (newPosition == end)
                        return distance;
                    if (!visited.Contains(newPosition) && maze.Contains(newPosition))
                    {
                        visited.Add(newPosition);
                        queue.Enqueue((newPosition, distance + 1));
                    }
                }
            }
            throw new Exception("Path not found");
        }

        static void ShowArea(Maze maze, Coordinate current, IEnumerable<Coordinate> visited)
        {
            var offset = 40;
            var minX = maze.Min(p => p.X);
            var maxX = maze.Max(p => p.X);
            var minY = maze.Min(p => p.Y);
            var maxY = maze.Max(p => p.Y);
            minX = Math.Max(minX, current.X - offset);
            maxX = Math.Min(maxX, current.X + offset);
            minY = Math.Max(minY, current.Y - offset);
            maxY = Math.Min(maxY, current.Y + offset);
            for (var y = minY; y < maxY + 1; y++)
            {
                for (var x = minX; x < maxX + 1; x++)
                {
                    var c = '#';
                    var position = new Coordinate(x, y);
                    if (maze.Contains(position))
                        c = '.';
                    if (visited.Contains(position))
                        c = 'x';
                    if (position == current)
                        c = 'O';
                    Write(c);
                }
                WriteLine();
            }
            WriteLine();
        }

        static (int, string)[] GetDistancesFromPosition(Maze maze, Portals portals, Coordinate start)
        {
            var paths = new List<(int, string)>();
            var visited = new List<Coordinate>();
            visited.Add(start);
            var queue = new Queue<(Coordinate, int)>();
            queue.Enqueue((start, 0));
            while (queue.Any())
            {
                var (position, distance) = queue.Dequeue();
                if (distance > 0 && portals.ContainsKey(position))
                    paths.Add((distance + 1, BuildPortalKey(portals[position], position, 0)));
                else
                    foreach (var newPosition in DIRECTIONS.Select(direction => position + direction))
                        if (!visited.Contains(newPosition) && maze.Contains(newPosition))
                        {
                            visited.Add(newPosition);
                            queue.Enqueue((newPosition, distance + 1));
                        }
            }
            return paths.ToArray();
        }

        static string BuildPortalKey(string label, Coordinate position, int level, bool addLevel = false)
            => $"{label},{position.X},{position.Y}" + (addLevel ? "," + level : "");

        static Dictionary<string, bool> GetPortalsDirections(Maze maze, Portals portals)
        {
            var minX = maze.Min(p => p.X);
            var maxX = maze.Max(p => p.X);
            var minY = maze.Min(p => p.Y);
            var maxY = maze.Max(p => p.Y);
            return portals.ToDictionary(pair => BuildPortalKey(pair.Value, pair.Key, 0), pair =>
                pair.Key.X == minX || pair.Key.X == maxX ||
                pair.Key.Y == minY || pair.Key.Y == maxY).ToDictionary(kv => kv.Key, kv => kv.Value);
        }

        static Dictionary<string, string> BuildPortalPairs(IEnumerable<string> portals)
        {
            var result = new Dictionary<string, string>();
            var otherPortal = string.Empty;
            foreach (var portal in portals)
                if (!string.IsNullOrEmpty(otherPortal = portals.FirstOrDefault(key => key.StartsWith(portal[..2]) && key != portal)))
                    result[portal] = otherPortal;
            return result;
        }

        static Dictionary<string, (int distance, string portal)[]> BuildGraph((Maze, Portals, Coordinate, Coordinate) data)
        {
            var (maze, portals, start, end) = data;
            var graph = portals.ToDictionary(pair => BuildPortalKey(pair.Value, pair.Key, 0), pair => GetDistancesFromPosition(maze, portals, pair.Key));
            return graph;
        }

        static int Part2((Maze, Portals, Coordinate, Coordinate) data)
        {
            var (maze, portals, start, end) = data;
            var target = BuildPortalKey("ZZ", end, 0);
            portals[start] = "AA";
            portals[end] = "ZZ";
            var graph = BuildGraph(data);
            var portalDirections = GetPortalsDirections(maze, portals);
            var portalPairs = BuildPortalPairs(portalDirections.Keys);
            portalDirections[target] = false;
            var distances = new Dictionary<string, int>();
            distances[BuildPortalKey("AA", start, 0, true)] = 0;
            var shortestPathTree = new List<string>();
            while (true)
            {
                var minPortal = distances.Where(pair => !shortestPathTree.Contains(pair.Key)).OrderBy(pair => pair.Value).First();
                if (minPortal.Key.StartsWith(target))
                    return minPortal.Value - 1;
                shortestPathTree.Add(minPortal.Key);
                var portalSplit = minPortal.Key.Split(',');
                var currentLevel = int.Parse(portalSplit[3]);
                foreach (var path in graph[$"{portalSplit[0]},{portalSplit[1]},{portalSplit[2]}"])
                {
                    var newDistance = minPortal.Value + path.distance;
                    if (!(portalDirections[path.portal] && currentLevel == 0) && !path.portal.StartsWith("AA"))
                        if (path.portal.StartsWith("ZZ"))
                        {
                            if (currentLevel == 0)
                                distances[target] = newDistance;
                        }
                        else
                        {
                            var otherPortalKey = $"{portalPairs[path.portal]},{currentLevel + (portalDirections[path.portal] ? -1 : +1)}";
                            if (!shortestPathTree.Contains(otherPortalKey) 
                                && (!distances.ContainsKey(otherPortalKey) 
                                || distances[otherPortalKey] > newDistance))
                                distances[otherPortalKey] = newDistance;
                        }
                }
            }
        }

        static (Maze, Portals, Coordinate, Coordinate) GetInput(string filePath)
        {
            if (!File.Exists(filePath)) throw new FileNotFoundException(filePath);
            var lines = File.ReadAllLines(filePath);
            var maze = new List<Coordinate>();
            var portals = new Portals();
            var start = Coordinate.Zero;
            var end = Coordinate.Zero;
            foreach (var (line, y) in lines.Select((line, y) => (line, y)))
                foreach (var (c, x) in line.Select((c, x) => (c, x)))
                {
                    var position = new Coordinate(x, y);
                    if (c == '.')
                    {
                        maze.Add(position);
                        var portal = string.Empty;
                        if (char.IsLetter(lines[y - 1][x]))
                            portal = lines[y - 2][x] + lines[y - 1][x].ToString();
                        else if (char.IsLetter(lines[y + 1][x]))
                            portal = lines[y + 1][x] + lines[y + 2][x].ToString();
                        else if (char.IsLetter(line[x - 1]))
                            portal = line[x - 2] + line[x - 1].ToString();
                        else if (char.IsLetter(line[x + 1]))
                            portal = line[x + 1] + line[x + 2].ToString();
                        if (!string.IsNullOrWhiteSpace(portal))
                        {
                            if (portal == "AA")
                                start = position;
                            else if (portal == "ZZ")
                                end = position;
                            else
                                portals[position] = portal;
                        }
                    }
                }
            return (maze, portals, start, end);
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
