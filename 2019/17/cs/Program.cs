﻿using System;
using static System.Console;
using System.IO;
using System.Diagnostics;
using System.Linq;
using System.Collections.Generic;

namespace AoC
{
    class Memory
    {
        public Memory(long[] memory)
            => _memory = memory.Select((value, index) => (value, index))
                .ToDictionary(pair => (long)pair.index, pair => (long)pair.value);
        
        public static Memory FromMemory(Memory memory)
        {
            var result = new Memory(new long[0]);
            result._memory = new Dictionary<long, long>(memory._memory);
            return result;
        }

        public long this[long key]
        {
            get
            {
                if (!_memory.ContainsKey(key))
                    _memory[key] = 0;
                return _memory[key];
            }
            set => _memory[key] = value;
        }

        private IDictionary<long, long> _memory;
    }

    class IntCodeComputer
    {
        public bool Running { get; private set; } = true;
        public bool Polling { get; private set; }
        public bool Outputing { get; private set; }
        
        public IntCodeComputer(long[] memory, IEnumerable<long> input = default(List<long>))
        {
            _memory = new Memory(memory);
            _input = new Queue<long>(input ?? new long[0]);
            _output = new Stack<long>();
        }

        public long Run()
        {
            while (Running) Tick();
            return _output.Pop();
        }

        public void AddInput(long value) => _input.Enqueue(value);

        public IEnumerable<long> GetOutputs() => _output.ToArray();

        public long GetOutput()
        {
            Outputing = false;
            return _output.Pop();
        }

        public IntCodeComputer Clone()
        {
            var cloneComputer = new IntCodeComputer(new long[0]);
            cloneComputer._memory = Memory.FromMemory(_memory);
            cloneComputer._pointer = _pointer;
            cloneComputer._base = _base;
            return cloneComputer;
        }

        public void Tick()
        {
            if (!Running) return;
            var instruction = _memory[_pointer];
            var (opCode, p1Mode, p2Mode, p3mode) = ((int)instruction % 100, (int)(instruction / 100) % 10, (int)(instruction / 1000) % 10, (int)(instruction / 10000) % 10);
            switch (opCode)
            {
                case 1: // ADD
                    _memory[GetAddress(3, p3mode)] = GetParameter(1, p1Mode) + GetParameter(2, p2Mode);
                    _pointer += 4;
                    break;
                case 2: // MUL
                    _memory[GetAddress(3, p3mode)] = GetParameter(1, p1Mode) * GetParameter(2, p2Mode);
                    _pointer += 4;
                    break;
                case 3: // INPUT
                    if (_input.Any())
                    {
                        Polling = false;
                        _memory[GetAddress(1, p1Mode)] = _input.Dequeue();
                        _pointer += 2;
                    }
                    else
                        Polling = true;
                    break;
                case 4: // OUTPUT
                    Outputing = true;
                    _output.Push(GetParameter(1, p1Mode));
                    _pointer += 2;
                    break;
                case 5: // JMP_TRUE
                    if (GetParameter(1, p1Mode) != 0)
                        _pointer = GetParameter(2, p2Mode);
                    else
                        _pointer += 3;
                    break;
                case 6: // JMP_FALSE
                    if (GetParameter(1, p1Mode) == 0)
                        _pointer = GetParameter(2, p2Mode);
                    else
                        _pointer += 3;
                    break;
                case 7: // LESS_THAN
                    _memory[GetAddress(3, p3mode)] = GetParameter(1, p1Mode) < GetParameter(2, p2Mode) ? 1 : 0;
                    _pointer += 4;
                    break;
                case 8: // LESS_THAN
                    _memory[GetAddress(3, p3mode)] = GetParameter(1, p1Mode) == GetParameter(2, p2Mode) ? 1 : 0;
                    _pointer += 4;
                    break;
                case 9:
                    _base += GetParameter(1, p1Mode);
                    _pointer += 2;
                    break;
                case 99: // HATL
                    Running = false;
                    break;
                default:
                    throw new Exception($"Unknown instruction {_pointer} {opCode}");
            }
        }
        private Memory _memory;
        public Queue<long> _input;
        private Stack<long> _output;
        private long _pointer;
        private long _base;

        private long GetAddress(int offset, int mode)
        {
            var value = _memory[_pointer + offset];
            switch (mode)
            {
                case 0: // POSITION
                    return value;
                case 2: // RELATIVE
                    return _base + value;
                default:
                    throw new Exception($"Unrecognized address mode '{mode}'");
            }
        }

        private long GetParameter(int offset, int mode)
        {
            var value = _memory[_pointer + offset];
            switch (mode)
            {
                case 0: // POSITION
                    return _memory[value];
                case 1: // IMMEDIATE
                    return value;
                case 2: // RELATIVE
                    return _memory[_base + value];
                default:
                    throw new Exception($"Unrecognized parameter mode '{mode}'");
            }
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
        static Dictionary<char, Coordinate> DIRECTIONS = new Dictionary<char, Coordinate> {
            { 'v', Coordinate.YOne },
            { '>', 1 },
            { '^', -Coordinate.YOne },
            { '<', -1 }
        };

        static void PrintArea(IEnumerable<Coordinate> scafolds, (Coordinate position, Coordinate direction) robot)
        {
            var minX = scafolds.Min(c => c.X);
            var maxX = scafolds.Max(c => c.X);
            var minY = scafolds.Min(c => c.Y);
            var maxY = scafolds.Max(c => c.Y);
            WriteLine($"{minX} {maxX} {minY} {maxY}");
            for (var y = minY; y < maxY + 1; y++)
            {
                for (var x = minX; x < maxX + 1; x++)
                {
                    var position = new Coordinate(x, y);
                    var c = '.';
                    if (scafolds.Contains(position))
                        c = '#';
                    if (position == robot.position)
                        c = DIRECTIONS.First(pair => pair.Value == robot.direction).Key;
                    Write(c);
                }
                WriteLine();
            }
            WriteLine();
        }

        static (IEnumerable<Coordinate>, (Coordinate, Coordinate)) GetScafoldsAndRobot(IntCodeComputer asciiComputer)
        {
            var position = Coordinate.Zero;
            var scafolds = new List<Coordinate>();
            var robot = (Coordinate.Zero, Coordinate.Zero);
            while (asciiComputer.Running)
            {
                asciiComputer.Tick();
                if (asciiComputer.Outputing)
                {
                    var code = asciiComputer.GetOutput();
                    if (code == 35) // '#'
                    {
                        scafolds.Add(position);
                        position += 1;
                    }
                    else if (code == 46) // '.'
                        position += 1;
                    else if (code == 10) // line feed
                        position = new Coordinate(0, position.Y + 1);
                    else
                    {
                        robot = (position, DIRECTIONS[(char)code]);
                        position += 1;
                    }
                }
            }
            return (scafolds, robot);
        }

        static int Part1(IEnumerable<Coordinate> scafolds)
        {
            var alignment = 0;
            foreach (var scafold in scafolds)
                if (DIRECTIONS.Values.All(direction => scafolds.Contains(scafold + direction)))
                    alignment += scafold.X * scafold.Y;
            return alignment;
        }

        static (Coordinate, string)[] TURNS = new [] {
            ( -Coordinate.YOne, "L" ),
            ( Coordinate.YOne, "R" )
        };
        static string[] FindPath(IEnumerable<Coordinate> scafolds, (Coordinate, Coordinate) robot)
        {
            var path = new List<string>();
            var currentTurn = string.Empty;
            var turnFound = true;
            while (turnFound)
            {
                var (position, direction) = robot;
                if (!scafolds.Contains(position + direction))
                {
                    turnFound = false;
                    foreach (var (turn, code) in TURNS)
                        if (scafolds.Contains(position + direction * turn))
                        {
                            turnFound = true;
                            currentTurn = code;
                            robot = (position, direction * turn);
                        }
                }
                else
                {
                    var currentLength = 0;
                    while (scafolds.Contains(position + direction))
                    {
                        position += direction;
                        currentLength++;
                    }
                    robot = (position, direction);
                    path.Add(currentTurn);
                    path.Add(currentLength.ToString());
                }
            }
            return path.ToArray();
        }

        static bool AreSegmentsEqual(string[] a, string[] b)
            => Enumerable.Range(0, a.Length).All(index => a[index] == b[index]);

        static (int, int)[] GetRepeatsInPath(string[] path, string[] segment)
            => Enumerable.Range(0, path.Length - segment.Length + 1)
                .Where(start => AreSegmentsEqual(path[new Range(start, start + segment.Length)], segment))
                .Select(start => (start, start + segment.Length)).ToArray();
        
        static bool IsPermutationValid(string[] path, IEnumerable<(int, int)> permutation)
        {
            var pathList = path.ToList();
            foreach (var (length, repeatCount) in permutation)
            {
                var segment = pathList.Take(length).ToArray();
                if (segment.Length * 2 - 1 > 20)
                    return false;
                var repeatIndexes = GetRepeatsInPath(pathList.ToArray(), segment);
                if (repeatIndexes.Length != repeatCount)
                    return false;
                foreach (var (start, _) in repeatIndexes.Reverse())
                    foreach (var _ in Enumerable.Range(0, length))
                        pathList.RemoveAt(start);
            }
            return !pathList.Any();
        }

        static IEnumerable<T[]> Permutations<T>(IEnumerable<T> source, int length) where T: IEquatable<T>
        {
            var stack = new Stack<List<T>>(source.Select(item => new List<T>(new [] { item })));
            while (stack.Any())
            {
                var current = stack.Pop();
                foreach (var item in source.Where(item => !current.Contains(item)))
                {
                    var newCurrent = current.ToList();
                    newCurrent.Add(item);
                    if (newCurrent.Count == length)
                        yield return newCurrent.ToArray();
                    else
                        stack.Push(newCurrent);
                }
            }
        }

        static Dictionary<int, (string[] segment, IEnumerable<(int, int)> indexes)> GetRoutines(string[] path)
        {
            var routines = new Dictionary<int, (string[], IEnumerable<(int, int)>)>();
            foreach (var permutation in Permutations(new [] { (6, 4), (10, 3), (8, 3), (6, 3) }, 3)) // possible (length, repeat counts)
            {
                if (IsPermutationValid(path, permutation))
                {
                    var indexesToGroup = Enumerable.Range(0, path.Length).ToList();
                    foreach (var ((length, _), c) in permutation.Select((p, index) => (p, index)))
                    {
                        var index = indexesToGroup.Min();
                        var segment = path[new Range(index, index + length)];
                        var repeatIndexes = GetRepeatsInPath(path, segment);
                        routines[c + (int)'A'] = (segment, repeatIndexes);
                        foreach (var (start, end) in repeatIndexes)
                            for (var i = start; i < end; i++)
                                indexesToGroup.Remove(i);
                    }
                }
            }
            return routines;
        }

        static long Part2(long[] memory, IEnumerable<Coordinate> scafolds, (Coordinate, Coordinate) robot)
        {
            var path = FindPath(scafolds, robot);
            var routines = GetRoutines(path);
            var mainRoutineSegments = new Dictionary<int, int>();
            var inputs = new List<string>();
            foreach (var (routine, (segments, indexes)) in routines.Select(pair => (pair.Key, pair.Value)))
            {
                inputs.Add(string.Join(",", segments) + (char)10);
                foreach (var indexGroup in indexes)
                    mainRoutineSegments[indexGroup.Item1] = routine;
            }
            inputs.Insert(0, string.Join(",", mainRoutineSegments.OrderBy(pair => pair.Key).Select(pair => (char)pair.Value)) + (char)10);
            inputs.Add("n" + (char)10);
            memory[0] = 2;
            var asciiComputer = new IntCodeComputer(memory);
            foreach (var inputLine in inputs)
                foreach (var c in inputLine)
                    asciiComputer.AddInput((int)c);
            return asciiComputer.Run();
        }

        static (int, long) Solve(long[] memory)
        {
            var asciiComputer = new IntCodeComputer(memory);
            var (scafolds, robot) = GetScafoldsAndRobot(asciiComputer);
            return (
                Part1(scafolds),
                Part2(memory, scafolds, robot)
            );
        }

        static long[] GetInput(string filePath)
            => !File.Exists(filePath) ? throw new FileNotFoundException(filePath)
            : File.ReadAllText(filePath).Trim().Split(",").Select(long.Parse).ToArray();

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