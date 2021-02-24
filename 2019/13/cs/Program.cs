using System;
using static System.Console;
using System.IO;
using System.Diagnostics;
using System.Linq;
using System.Collections.Generic;
using System.Numerics;

namespace AoC
{
    using Screen = Dictionary<Complex, Tile>;

    class Memory
    {
        public Memory(long[] memory)
            => _memory = memory.Select((value, index) => (value, index))
                .ToDictionary(pair => (long)pair.index, pair => (long)pair.value);

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

        public void AddInput(int value) => _input.Enqueue(value);

        public IEnumerable<long> GetOutputs() => _output.ToArray();

        public long GetOutput()
        {
            Outputing = false;
            return _output.Pop();
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
        private Queue<long> _input;
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

    enum Tile
    {
        Empty,
        Wall,
        Block,
        Paddle,
        Ball
    }

    static class Program
    {
        static Dictionary<Tile, char> TILE_CHARS = new Dictionary<Tile, char> {
            { Tile.Empty, '.' },
            { Tile.Wall, 'W' },
            { Tile.Block, 'B' },
            { Tile.Paddle, 'P' },
            { Tile.Ball, 'X' }
        };
        static void PrintScreen(Screen screen)
        {
            var maxX = (int)(screen.Keys.Max(p => p.Real));
            var minX = (int)(screen.Keys.Min(p => p.Real));
            var maxY = (int)(screen.Keys.Max(p => p.Imaginary));
            var minY = (int)(screen.Keys.Min(p => p.Imaginary));
            for (var y = minY; y < maxY + 1; y++)
            {
                for (var x = minX; x < maxX + 1; x++)
                {
                    var c = ' ';
                    var position = new Complex(x, y);
                    if (screen.ContainsKey(position))
                        c = TILE_CHARS[screen[position]];
                    Write(c);
                }
                WriteLine();
            }
            WriteLine();
            ReadLine();
        }

        static (int blocks, long score) RunGame(long[] memory)
        {
            var cabinet = new IntCodeComputer(memory);
            var screen = new Screen();
            var currentOuput = new Stack<long>();
            var ball = 0L;
            var paddle = 0L;
            var score = 0L;
            while (cabinet.Running)
            {
                cabinet.Tick();
                if (cabinet.Polling)
                {
                    var joystick = 0;
                    if (ball > paddle)
                        joystick = 1;
                    else if (ball < paddle)
                        joystick = -1;
                    cabinet.AddInput(joystick);
                }
                if (cabinet.Outputing)
                {
                    currentOuput.Push(cabinet.GetOutput());
                    if (currentOuput.Count == 3)
                    {
                        var value = currentOuput.Pop();
                        var y = currentOuput.Pop();
                        var x = currentOuput.Pop();
                        if (x == -1)
                            score = value;
                        else
                        {
                            var tile = (Tile)value;
                            if (tile == Tile.Ball)
                                ball = x;
                            else if (tile == Tile.Paddle)
                                paddle = x;
                            screen[new Complex(x, y)] = tile;
                        }
                    }
                }
            }
            return (screen.Values.Count(tile => tile == Tile.Block), score);
        }

        static int Part1(long[] memory) => RunGame(memory).blocks;

        static long Part2(long[] memory)
        {
            memory[0] = 2;
            return RunGame(memory).score;
        }

        static long[] GetInput(string filePath)
        {
            if (!File.Exists(filePath)) throw new FileNotFoundException(filePath);
            return File.ReadAllText(filePath).Trim().Split(",").Select(long.Parse).ToArray();
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