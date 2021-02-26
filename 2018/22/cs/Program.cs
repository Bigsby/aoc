using System;
using static System.Console;
using System.IO;
using System.Diagnostics;
using System.Linq;
using System.Collections.Generic;
using System.Numerics;
using System.Text.RegularExpressions;

namespace AoC
{
    using Coordiante = Complex;

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

    record Node(int duration, int x, int y, int risk) : IComparable<Node>
    {
        public int CompareTo(Node other)
        {
            if (duration != other.duration)
                return -duration.CompareTo(other.duration);
            if (x != other.x)
                return -x.CompareTo(other.x);
            return -y.CompareTo(other.y);
        }

        public override string ToString()
            => $"{duration} {x} {y} {risk}";
    }

    static class Program
    {
        const int GEOLOGIC_X_CONSTANT = 16807;
        const int GEOLOGIC_Y_CONSTANT = 48271;
        const int EROSION_CONSTANT = 20183;

        static int GetGeologicIndex(Coordiante coordinate, int depth, Coordiante target, Dictionary<Coordiante, int> calculated)
        {
            if (coordinate == 0 || coordinate == target)
                return 0;
            var (x, y) = ((int)coordinate.Real, (int)coordinate.Imaginary);
            if (x == 0)
                return y * GEOLOGIC_Y_CONSTANT;
            else if (y == 0)
                return x * GEOLOGIC_X_CONSTANT;
            return GetErosionLevel(new Coordiante(x - 1, y), depth, target, calculated) *
                GetErosionLevel(new Coordiante(x, y - 1), depth, target, calculated);
        }

        static int GetErosionLevel(Coordiante coordiante, int depth, Coordiante target, Dictionary<Coordiante, int> calculated)
        {
            if (!calculated.ContainsKey(coordiante))
                calculated[coordiante] = (GetGeologicIndex(coordiante, depth, target, calculated) + depth) % EROSION_CONSTANT;
            return calculated[coordiante];
        }

        static int GetRisk(Coordiante coordiante, int depth, Coordiante target, Dictionary<Coordiante, int> calculated)
            => GetErosionLevel(coordiante, depth, target, calculated) % 3;

        static int Part1((int, int, int) data)
        {
            var (depth, targetX, targetY) = data;
            var target = new Coordiante(targetX, targetY);
            var calculated = new Dictionary<Coordiante, int>();
            var total = 0;
            for (var y = 0; y < targetY + 1; y++)
                for (var x = 0; x < targetX + 1; x++)
                    total += GetRisk(new Coordiante(x, y), depth, target, calculated);
            return total;
        }

        static Coordiante[] DIRECTIONS = new[] { 1, Coordiante.ImaginaryOne, -1, -Coordiante.ImaginaryOne };
        static int Part2((int, int, int) data)
        {
            var (depth, targetX, targetY) = data;
            var target = new Coordiante(targetX, targetY);
            var calculated = new Dictionary<Coordiante, int>();
            var final = $"{targetX},{targetY},1";
            var queue = new Heap<Node>();
            queue.Push(new Node(0, 0, 0, 1));
            var bestTimes = new Dictionary<string, int>();
            while (!queue.IsEmpty())
            {
                var (duration, x, y, risk) = queue.Pop();
                var coordinate = new Coordiante(x, y);
                var state = $"{(int)coordinate.Real},{(int)coordinate.Imaginary},{risk}";
                if (bestTimes.ContainsKey(state) && bestTimes[state] <= duration)
                    continue;
                if (state == final)
                    return duration;
                bestTimes[state] = duration;
                for (var tool = 0; tool < 3; tool++)
                    if (tool != risk && tool != GetRisk(coordinate, depth, target, calculated))
                        queue.Push(new Node(duration + 7, x, y, tool));
                foreach (var newCoordinate in DIRECTIONS.Select(direction => coordinate + direction))
                    if (newCoordinate.Real >= 0 && newCoordinate.Imaginary >= 0
                        && GetRisk(newCoordinate, depth, target, calculated) != risk)
                        queue.Push(new Node(duration + 1, (int)newCoordinate.Real, (int)newCoordinate.Imaginary, risk));
            }
            throw new Exception("Path not found");
        }

        static (int, int) Solve((int, int, int) data)
            => (
                Part1(data),
                Part2(data)
            );

        static (int, int, int) GetInput(string filePath)
        {
            if (!File.Exists(filePath)) throw new FileNotFoundException(filePath);
            var matches = Regex.Matches(File.ReadAllText(filePath), @"\d+").ToArray();
            return (
                int.Parse(matches[0].Value),
                int.Parse(matches[1].Value),
                int.Parse(matches[2].Value)
            );
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
