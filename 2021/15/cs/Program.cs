using System;
using static System.Console;
using System.IO;
using System.Diagnostics;
using System.Linq;
using System.Collections.Generic;
using System.Drawing;

namespace AoC
{
    using Input = Tuple<Dictionary<Point, int>, int, int>;

    class PriorityNode
    {
        public PriorityNode(Point point, int distance)
        {
            Point = point;
            Distance = distance;
            Next = null;
        }

        public PriorityNode Next { get; set; }
        public int Distance { get; init; }
        public Point Point { get; init; }
        public void Deconstruct(out Point point, out int distance)
        {
            point = Point;
            distance = Distance;
        }
    }

    class PriorityQueue
    {
        private PriorityNode _head;
        public void Enqueue(Point point, int distance)
        {
            PriorityNode current = _head;
            PriorityNode previous = null;
            while (current != null && current.Distance < distance)
            {
                previous = current;
                current = current.Next;
            }
            PriorityNode newNode = new PriorityNode(point, distance);
            newNode.Next = current;
            if (previous != null)
                previous.Next = newNode;
            _head = previous == null ? newNode : _head;
        }

        public bool TryDequeue(out Point point, out int distance)
        {
            if (_head == null)
            {
                point = new Point(0, 0);
                distance = 0;
                return false;
            }
            var (nextPoint, nextDistance) = Dequeue();
            point = nextPoint;
            distance = nextDistance;
            return true;
        }

        PriorityNode Dequeue()
        {
            if (_head == null)
                throw new Exception("Dequeueing for empty queue");
            var nextNode = _head;
            _head = nextNode.Next;
            return nextNode;
        }
    }

    static class Program
    {
        static IEnumerable<Point> GetNeighbors(Point point, int width, int height)
        {
            if (point.X > 0)
                yield return new Point(point.X - 1, point.Y);
            if (point.Y > 0)
                yield return new Point(point.X, point.Y - 1);
            if (point.X < width - 1)
                yield return new Point(point.X + 1, point.Y);
            if (point.Y < height - 1)
                yield return new Point(point.X, point.Y + 1);
        }

        static int GetPointRisk(Dictionary<Point, int> riskLevels, Point point, int width, int height, int expansion)
        {
            var risk = riskLevels[new Point(point.X % width, point.Y % height)] + point.X / width + point.Y / height;
            return risk < 10 ? risk : risk - 9;
        }

        static int GetLowestRisk(Input puzzleInput, int expansion)
        {
            var (riskLevels, width, height) = puzzleInput;
            var expandedWidth = width * expansion;
            var expandedHeight = height * expansion;
            var target = new Point(expandedWidth - 1, expandedHeight - 1);
            var distances = new Dictionary<Point, int>();
            distances[new Point(0, 0)] = 0;
            var queue = new PriorityQueue();
            queue.Enqueue(new Point(0, 0), 0);
            Point current;
            int currentRisk;
            while (queue.TryDequeue(out current, out currentRisk))
            {
                if (current == target)
                    return currentRisk;
                foreach (var neighbor in GetNeighbors(current, expandedWidth, expandedHeight))
                {
                    var newNeighborRisk = currentRisk + GetPointRisk(riskLevels, neighbor, width, height, expansion);
                    if (!distances.TryGetValue(neighbor, out var neighborDistance) || neighborDistance > newNeighborRisk)
                    {
                        distances[neighbor] = newNeighborRisk;
                        queue.Enqueue(neighbor, newNeighborRisk);
                    }
                }
            }
            throw new Exception("Lowers risk not found");
        }

        static (int, int) Solve(Input puzzleInput)
            => (GetLowestRisk(puzzleInput, 1), GetLowestRisk(puzzleInput, 5));

        static Input GetInput(string filePath)
        {
            if (!File.Exists(filePath)) throw new FileNotFoundException(filePath);
            var riskLevels = new Dictionary<Point, int>();
            var y = 0;
            var x = 0;
            foreach (var line in File.ReadAllLines(filePath))
            {
                x = 0;
                foreach (var c in line)
                {
                    riskLevels[new Point(x, y)] = c - '0';
                    x++;
                }
                y++;
            }
            return Tuple.Create(riskLevels, x, y);
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
