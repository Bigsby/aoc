using System;
using static System.Console;
using System.IO;
using System.Diagnostics;
using System.Linq;
using System.Collections.Generic;

namespace AoC
{
    using Maze = IEnumerable<Coordinate>;
    using KeyDoors = Dictionary<Coordinate, char>;

    class Heap<T> where T : IComparable<T>
    {
        public Heap() : this(false) { }
        public Heap(ICollection<T> collection) : this(collection, false) { }
        public Heap(ICollection<T> collection, bool minHeap)
            : this(collection.Count, minHeap)
        {
            foreach (T t in collection)
                Push(t);
        }
        public Heap(bool minHeap) : this(16, minHeap) { }
        public Heap(int capacity) : this(capacity, false) { }
        public Heap(int capacity, bool minHeap)
        {
            int cap = 2;
            while (cap < capacity) cap <<= 1;

            heap = new T[cap + 1];
            size = 0;
            this.minHeap = minHeap;
        }

        public bool IsEmpty() { return size < 1; }

        public T Peek()
        {
            if (size < 1)
                throw new ApplicationException("The heap is empty!");
            return heap[1];
        }

        public virtual T Pop()
        {
            if (size < 1)
                throw new ApplicationException("The heap is empty!");
            T max = Peek();
            heap[1] = heap[size--];
            inverse[heap[1]] = 1;
            Heapify(1);
            inverse.Remove(max);
            return max;
        }

        public virtual void Push(T value)
        {
            if (++size > heap.Length - 1)
                Array.Resize<T>(ref heap, heap.Length << 1);
            int i = size;
            while (i > 1 && ((!minHeap && heap[P(i)].CompareTo(value) < 0) || (minHeap && heap[P(i)].CompareTo(value) > 0)))
            {
                heap[i] = heap[P(i)];
                inverse[heap[i]] = i;
                i = P(i);
            }
            heap[i] = value;
            inverse[value] = i;
        }

        public virtual T PopPush(T value)
        {
            if (size < 1)
                throw new ApplicationException("The heap is empty!");
            T max = Peek();
            heap[1] = value;
            inverse[value] = 1;
            Heapify(1);
            return max;
        }

        public void Update(T old, T value)
        {
            int i = -1;
            if (old.CompareTo(value) != 0 && inverse.TryGetValue(old, out i))
            {
                inverse.Remove(old);

                heap[i] = value;
                inverse[value] = i;

                if ((!minHeap && old.CompareTo(value) > 0) || (minHeap && old.CompareTo(value) < 0))
                {
                    Heapify(i);
                }
                else
                {
                    while (i > 1 && ((!minHeap && heap[i].CompareTo(heap[P(i)]) > 0) || (minHeap && heap[i].CompareTo(heap[P(i)]) < 0)))
                    {
                        Swap(i, P(i));
                        i = P(i);
                    }
                }
            }
        }

        protected int P(int i)
        {
            return i / 2;
        }
        protected int L(int i)
        {
            return 2 * i;
        }
        protected int R(int i)
        {
            return 2 * i + 1;
        }
        protected void Heapify(int i)
        {
            int max = i;
            int l = L(i);
            int r = R(i);
            if (l <= size && ((!minHeap && heap[l].CompareTo(heap[i]) > 0) || (minHeap && heap[l].CompareTo(heap[i]) < 0)))
                max = l;
            if (r <= size && ((!minHeap && heap[r].CompareTo(heap[max]) > 0) || (minHeap && heap[r].CompareTo(heap[max]) < 0)))
                max = r;
            if (max != i)
            {
                Swap(i, max);
                Heapify(max);
            }
        }

        protected void Swap(int i, int j)
        {
            T ti = heap[i];
            T tj = heap[j];
            heap[j] = ti;
            heap[i] = tj;
            inverse[ti] = j;
            inverse[tj] = i;
        }

        protected T[] heap;
        protected Dictionary<T, int> inverse = new Dictionary<T, int>();
        protected int size;
        protected bool minHeap;
    }

    class Node : IComparable<Node>
    {
        public int Distance { get; init; }
        public IEnumerable<char> StartingPoints { get; init; }
        public IEnumerable<char> KeysFound { get; init; }
        public Node(int distance, IEnumerable<char> startingPoints, IEnumerable<char> keysFound)
        {
            Distance = distance;
            StartingPoints = startingPoints;
            KeysFound = keysFound;
        }
        public int CompareTo(Node other) => -Distance.CompareTo(other.Distance);
        public void Deconstruct(out int distance, out IEnumerable<char> startingPoints, out IEnumerable<char> keysFound)
        {
            distance = Distance;
            startingPoints = StartingPoints;
            keysFound = KeysFound;
        }
    }

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
        public static Coordinate YOne => new Coordinate(0, 1);
        public static Coordinate Zero => 0;

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

    static class Program
    {
        static void ShowMaze(Maze maze, KeyDoors keysDoors, IEnumerable<Coordinate> starts)
        {
            var maxX = maze.Max(p => p.X) + 1;
            var maxY = maze.Max(p => p.Y) + 1;
            for (var y = 0; y < maxY; y++)
            {
                for (var x = 0; x < maxX; x++)
                {
                    var c = '.';
                    var position = new Coordinate(x, y);
                    if (maze.Contains(position))
                        c = '#';
                    if (keysDoors.ContainsKey(position))
                        c = keysDoors[position];
                    if (starts.Contains(position))
                        c = '@';
                    Write(c);
                }
                WriteLine();
            }
            WriteLine();
        }

        static Coordinate[] DIRECTIONS = new[] {
            new Coordinate(-1,  0),
            new Coordinate( 0, -1),
            new Coordinate( 1,  0),
            new Coordinate( 0,  1),
        };
        static Dictionary<char, (int, IEnumerable<char>)> FindPathsFromPosition(Maze maze, KeyDoors keysDoors, Coordinate start)
        {
            var visited = new List<Coordinate>();
            visited.Add(start);
            var queue = new Queue<(Coordinate, int, IEnumerable<char>)>();
            queue.Enqueue((start, 0, new char[0]));
            var paths = new Dictionary<char, (int, IEnumerable<char>)>();
            while (queue.Any())
            {
                var (position, distance, requiredKeys) = queue.Dequeue();
                foreach (var newPosition in DIRECTIONS.Select(direction => position + direction))
                    if (!maze.Contains(newPosition) && !visited.Contains(newPosition))
                    {
                        visited.Add(newPosition);
                        var newRequiredKeys = requiredKeys.ToList();
                        if (keysDoors.ContainsKey(newPosition))
                        {
                            var keyDoor = keysDoors[newPosition];
                            if ((int)keyDoor > 90)
                                paths[keyDoor] = (distance + 1, requiredKeys);
                            else
                                newRequiredKeys.Add((char)(keyDoor + 32));
                        }
                        queue.Enqueue((newPosition, distance + 1, newRequiredKeys));
                    }
            }
            return paths;
        }

        static int FindShortestPathFromKeyGragph(Dictionary<char, Dictionary<char, (int, IEnumerable<char>)>> pathsFromKeys, Dictionary<char, Coordinate> keys, IEnumerable<char> entrances)
        {
            var paths = new Heap<Node>();
            paths.Push(new Node(0, entrances, new char[0]));
            var visited = new Dictionary<string, int>();
            while (!paths.IsEmpty())
            {
                var (distanceSoFar, startingPoints, keysFound) = paths.Pop();
                if (keysFound.Count() == keys.Count)
                    return distanceSoFar;
                foreach (var (key, index) in startingPoints.Select((key, index) => (key, index)))
                    foreach (var (nextKey, (nextDistance, nextRequiredKeys)) in pathsFromKeys[key].OrderBy(pair => pair.Value.Item1))
                        if (!keysFound.Contains(nextKey))
                        {
                            var newKeys = keysFound.Concat(new[] { nextKey });
                            var newPositions = startingPoints.ToArray();
                            newPositions[index] = nextKey;
                            var nodeId = string.Join(",", newPositions) + "|" + string.Join(",", newKeys.OrderBy(c => c));
                            var newDistance = distanceSoFar + nextDistance;
                            if ((!visited.ContainsKey(nodeId) || visited[nodeId] > newDistance) && !nextRequiredKeys.Except(keysFound).Any())
                            {
                                paths.Push(new Node(newDistance, newPositions, newKeys));
                                visited[nodeId] = newDistance;
                            }
                        }
            }
            throw new Exception("Path not found");
        }

        static int FindShortestPath(Maze maze, KeyDoors keyDoors, IEnumerable<Coordinate> entrances)
        {
            var keys = keyDoors.Where(pair => (int)pair.Value > 90).ToDictionary(pair => pair.Value, pair => pair.Key);
            var keysPaths = keys.ToDictionary(pair => pair.Key, pair => FindPathsFromPosition(maze, keyDoors, pair.Value));
            foreach (var (position, index) in entrances.Select((position, index) => (position, index)))
                keysPaths[(char)(48 + index)] = FindPathsFromPosition(maze, keyDoors, position);
            return FindShortestPathFromKeyGragph(keysPaths, keys, Enumerable.Range(0, entrances.Count()).Select(index => (char)(index + 48)));
        }

        static int Part1((Maze maze, KeyDoors keyDoors, Coordinate start) data)
            => FindShortestPath(data.maze, data.keyDoors, new[] { data.start });

        static int Part2((Maze, KeyDoors, Coordinate) data)
        {
            var (maze, keyDoors, start) = data;
            var mazeList = maze.ToList();
            foreach (var offset in new[] { new Coordinate(-1, 0), new Coordinate(1, 0), new Coordinate(0, -1), new Coordinate(0, 1) })
                mazeList.Add(start + offset);
            var entrances = new[] { new Coordinate(-1, -1), new Coordinate(-1, 1), new Coordinate(1, -1), new Coordinate(1, 1) }
                .Select(offset => start + offset);
            return FindShortestPath(mazeList, keyDoors, entrances);
        }

        static (Maze maze, KeyDoors keyDoors, Coordinate start) GetInput(string filePath)
        {
            if (!File.Exists(filePath)) throw new FileNotFoundException(filePath);
            var maze = new List<Coordinate>();
            var keysDoors = new KeyDoors();
            var entrance = Coordinate.Zero;
            foreach (var (line, y) in File.ReadLines(filePath).Select((line, y) => (line, y)))
                foreach (var (c, x) in line.Select((c, x) => (c, x)))
                    if (c == '#')
                        maze.Add(new Coordinate(x, y));
                    else if (c == '@')
                        entrance = new Coordinate(x, y);
                    else if (c != '.')
                        keysDoors[new Coordinate(x, y)] = c;
            return (maze, keysDoors, entrance);
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
