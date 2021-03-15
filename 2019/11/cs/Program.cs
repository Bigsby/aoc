using System;
using static System.Console;
using System.IO;
using System.Diagnostics;
using System.Linq;
using System.Collections.Generic;
using System.Numerics;

namespace AoC
{
    using Screen = Dictionary<Complex, int>;
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

        public IntCodeComputer(long[] memory, IEnumerable<int> input)
        {
            _memory = new Memory(memory);
            _input = new Queue<long>(input.Select(Convert.ToInt64));
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
            var (opCode, p1Mode, p2Mode, p3mode) = (
                (int)instruction % 100,
                (int)(instruction / 100) % 10,
                (int)(instruction / 1000) % 10,
                (int)(instruction / 10000) % 10
            );
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

    class Program
    {
        const int CHARACTER_WIDTH = 5;
        static IDictionary<int, char> LETTERS = new Dictionary<int, char> {
            {   (0b01100 << CHARACTER_WIDTH * 0) +
                (0b10010 << CHARACTER_WIDTH * 1) +
                (0b10010 << CHARACTER_WIDTH * 2) +
                (0b11110 << CHARACTER_WIDTH * 3) +
                (0b10010 << CHARACTER_WIDTH * 4) +
                (0b10010 << CHARACTER_WIDTH * 5), 'A' },

            {   (0b11100 << CHARACTER_WIDTH * 0) +
                (0b10010 << CHARACTER_WIDTH * 1) +
                (0b11100 << CHARACTER_WIDTH * 2) +
                (0b10010 << CHARACTER_WIDTH * 3) +
                (0b10010 << CHARACTER_WIDTH * 4) +
                (0b11100 << CHARACTER_WIDTH * 5), 'B' },

            {   (0b01100 << CHARACTER_WIDTH * 0) +
                (0b10010 << CHARACTER_WIDTH * 1) +
                (0b10000 << CHARACTER_WIDTH * 2) +
                (0b10000 << CHARACTER_WIDTH * 3) +
                (0b10010 << CHARACTER_WIDTH * 4) +
                (0b01100 << CHARACTER_WIDTH * 5), 'C' },

            {   (0b11100 << CHARACTER_WIDTH * 0) +
                (0b10010 << CHARACTER_WIDTH * 1) +
                (0b10010 << CHARACTER_WIDTH * 2) +
                (0b10010 << CHARACTER_WIDTH * 3) +
                (0b10010 << CHARACTER_WIDTH * 4) +
                (0b11100 << CHARACTER_WIDTH * 5), 'D' },

            {   (0b11110 << CHARACTER_WIDTH * 0) +
                (0b10000 << CHARACTER_WIDTH * 1) +
                (0b11100 << CHARACTER_WIDTH * 2) +
                (0b10000 << CHARACTER_WIDTH * 3) +
                (0b10000 << CHARACTER_WIDTH * 4) +
                (0b11110 << CHARACTER_WIDTH * 5), 'E' },

            {   (0b11110 << CHARACTER_WIDTH * 0) +
                (0b10000 << CHARACTER_WIDTH * 1) +
                (0b11100 << CHARACTER_WIDTH * 2) +
                (0b10000 << CHARACTER_WIDTH * 3) +
                (0b10000 << CHARACTER_WIDTH * 4) +
                (0b10000 << CHARACTER_WIDTH * 5), 'F' },

            {   (0b01100 << CHARACTER_WIDTH * 0) +
                (0b10010 << CHARACTER_WIDTH * 1) +
                (0b10000 << CHARACTER_WIDTH * 2) +
                (0b10110 << CHARACTER_WIDTH * 3) +
                (0b10010 << CHARACTER_WIDTH * 4) +
                (0b01110 << CHARACTER_WIDTH * 5), 'G' },

            {   (0b10010 << CHARACTER_WIDTH * 0) +
                (0b10010 << CHARACTER_WIDTH * 1) +
                (0b11110 << CHARACTER_WIDTH * 2) +
                (0b10010 << CHARACTER_WIDTH * 3) +
                (0b10010 << CHARACTER_WIDTH * 4) +
                (0b10010 << CHARACTER_WIDTH * 5), 'H' },

            {   (0b01110 << CHARACTER_WIDTH * 0) +
                (0b00100 << CHARACTER_WIDTH * 1) +
                (0b00100 << CHARACTER_WIDTH * 2) +
                (0b00100 << CHARACTER_WIDTH * 3) +
                (0b00100 << CHARACTER_WIDTH * 4) +
                (0b01110 << CHARACTER_WIDTH * 5), 'I' },

            {   (0b00110 << CHARACTER_WIDTH * 0) +
                (0b00010 << CHARACTER_WIDTH * 1) +
                (0b00010 << CHARACTER_WIDTH * 2) +
                (0b00010 << CHARACTER_WIDTH * 3) +
                (0b10010 << CHARACTER_WIDTH * 4) +
                (0b01100 << CHARACTER_WIDTH * 5), 'J' },

            {   (0b10010 << CHARACTER_WIDTH * 0) +
                (0b10100 << CHARACTER_WIDTH * 1) +
                (0b11000 << CHARACTER_WIDTH * 2) +
                (0b10100 << CHARACTER_WIDTH * 3) +
                (0b10100 << CHARACTER_WIDTH * 4) +
                (0b10010 << CHARACTER_WIDTH * 5), 'K' },

            {   (0b10000 << CHARACTER_WIDTH * 0) +
                (0b10000 << CHARACTER_WIDTH * 1) +
                (0b10000 << CHARACTER_WIDTH * 2) +
                (0b10000 << CHARACTER_WIDTH * 3) +
                (0b10000 << CHARACTER_WIDTH * 4) +
                (0b11110 << CHARACTER_WIDTH * 5), 'L' },

            {   (0b01100 << CHARACTER_WIDTH * 0) +
                (0b10010 << CHARACTER_WIDTH * 1) +
                (0b10010 << CHARACTER_WIDTH * 2) +
                (0b10010 << CHARACTER_WIDTH * 3) +
                (0b10010 << CHARACTER_WIDTH * 4) +
                (0b01100 << CHARACTER_WIDTH * 5), 'O' },

            {   (0b11100 << CHARACTER_WIDTH * 0) +
                (0b10010 << CHARACTER_WIDTH * 1) +
                (0b10010 << CHARACTER_WIDTH * 2) +
                (0b11100 << CHARACTER_WIDTH * 3) +
                (0b10000 << CHARACTER_WIDTH * 4) +
                (0b10000 << CHARACTER_WIDTH * 5), 'P' },

            {   (0b11100 << CHARACTER_WIDTH * 0) +
                (0b10010 << CHARACTER_WIDTH * 1) +
                (0b10010 << CHARACTER_WIDTH * 2) +
                (0b11100 << CHARACTER_WIDTH * 3) +
                (0b10100 << CHARACTER_WIDTH * 4) +
                (0b10010 << CHARACTER_WIDTH * 5), 'R' },

            {   (0b01110 << CHARACTER_WIDTH * 0) +
                (0b10000 << CHARACTER_WIDTH * 1) +
                (0b10000 << CHARACTER_WIDTH * 2) +
                (0b01100 << CHARACTER_WIDTH * 3) +
                (0b00010 << CHARACTER_WIDTH * 4) +
                (0b11100 << CHARACTER_WIDTH * 5), 'S' },

            {   (0b10010 << CHARACTER_WIDTH * 0) +
                (0b10010 << CHARACTER_WIDTH * 1) +
                (0b10010 << CHARACTER_WIDTH * 2) +
                (0b10010 << CHARACTER_WIDTH * 3) +
                (0b10010 << CHARACTER_WIDTH * 4) +
                (0b01100 << CHARACTER_WIDTH * 5), 'U' },

            {   (0b10001 << CHARACTER_WIDTH * 0) +
                (0b10001 << CHARACTER_WIDTH * 1) +
                (0b01010 << CHARACTER_WIDTH * 2) +
                (0b00100 << CHARACTER_WIDTH * 3) +
                (0b00100 << CHARACTER_WIDTH * 4) +
                (0b00100 << CHARACTER_WIDTH * 5), 'Y' },

            {   (0b11110 << CHARACTER_WIDTH * 0) +
                (0b00010 << CHARACTER_WIDTH * 1) +
                (0b00100 << CHARACTER_WIDTH * 2) +
                (0b01000 << CHARACTER_WIDTH * 3) +
                (0b10000 << CHARACTER_WIDTH * 4) +
                (0b11110 << CHARACTER_WIDTH * 5), 'Z' }
        };

        static Dictionary<int, Complex> DIRECTION_CHANGES = new Dictionary<int, Complex> {
            { 0, Complex.ImaginaryOne },
            { 1, -Complex.ImaginaryOne }
        };
        static Screen RunProgram(long[] memory, Screen panels)
        {
            var robot = new IntCodeComputer(memory, new int[0]);
            var position = Complex.Zero;
            var heading = Complex.ImaginaryOne;
            var waitingForColor = true;
            while (robot.Running)
            {
                robot.Tick();
                if (robot.Polling)
                    robot.AddInput(panels.ContainsKey(position) ? panels[position] : 0);
                else if (robot.Outputing)
                    if (waitingForColor)
                    {
                        waitingForColor = false;
                        panels[position] = (int)robot.GetOutput();
                    }
                    else
                    {
                        waitingForColor = true;
                        heading *= DIRECTION_CHANGES[(int)robot.GetOutput()];
                        position += heading;
                    }
            }
            return panels;
        }

        static int Part1(long[] memory)
            => RunProgram(memory, new Screen { { 0, 0 } }).Count;

        static ((int width, int height), int minX, int maxX, int minY, int maxY) GetDimensions(IEnumerable<Complex> points)
        {
            var minX = (int)points.Min(p => p.Real);
            var maxX = (int)points.Max(p => p.Real);
            var minY = (int)points.Min(p => p.Imaginary);
            var maxY = (int)points.Max(p => p.Imaginary);
            var size = (Math.Abs(maxX - minX + 1), Math.Abs(maxY - minY + 1));
            return (size, minX, maxX, minY, maxY);
        }

        static char GetCharacterInScreen(IEnumerable<Complex> screen, int index, int width, int height, int xOffset, int yOffset)
        {
            var screenValue = Enumerable.Range(0, height).SelectMany(y => Enumerable.Range(0, width).Select(x => (x, y)))
                .Where(pair => screen.Contains(new Complex(width * index + pair.x + xOffset, pair.y + yOffset)))
                .Sum(pair => (int)Math.Pow(2, width - 1 - pair.x) << (pair.y * width));
            return LETTERS[screenValue];
        }

        static void PrintPoints(IEnumerable<Complex> panels)
        {
            if (panels.Count() == 0)
            {
                WriteLine("no points");
                return;
            }
            var (_, minX, maxX, minY, maxY) = GetDimensions(panels);
            for (var y = minY; y <= maxY; y++)
            {
                for (var x = minX; x <= maxX; x++)
                {
                    var c = '.';
                    if (panels.Contains(new Complex(x, y)))
                        c = '#';
                    Write(c);
                }
                WriteLine();
            }
            WriteLine();
        }

        static string Part2(long[] memory)
        {
            var panels = RunProgram(memory, new Screen { { 0, 1 } });
            var panelPoints = panels.Where(pair => pair.Value != 0).Select(pair => new Complex(pair.Key.Real, -pair.Key.Imaginary));
            var ((width, height), minX, _, minY, _) = GetDimensions(panelPoints);
            return string.Join("", Enumerable.Range(0, (width / CHARACTER_WIDTH) + 1).Select(index =>
                GetCharacterInScreen(panelPoints, index, CHARACTER_WIDTH, height, minX, minY)));
        }

        static (int, string) Solve(long[] memory)
            => (
                RunProgram(memory, new Screen { { 0, 0 } }).Count,
                Part2(memory)
            );

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