using System;
using static System.Console;
using System.IO;
using System.Diagnostics;
using System.Linq;
using System.Collections.Generic;
using System.Numerics;

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

 
    static class Program
    {
        static Dictionary<int, Complex> DIRECTIONS = new Dictionary<int, Complex>
        {
            { 1, -Complex.ImaginaryOne },
            { 2, Complex.ImaginaryOne },
            { 3, -1 },
            { 4, 1 }
        };

        static (int result, Complex oxygenSystem, IEnumerable<Complex> openSpaces) RunUntilOxygenSystem(long[] memory)
        {
            var startPosition = Complex.Zero;
            var openSpaces = new List<Complex>();
            var oxygenPosition = Complex.Zero;
            var stepsToOxygenSystem = 0;
            var queue = new Queue<(Complex position, IEnumerable<Complex> path, IntCodeComputer droid)>();
            queue.Enqueue((startPosition, new [] { startPosition }, new IntCodeComputer(memory)));
            var visited = new List<Complex>();
            visited.Add(startPosition);
            while (queue.Any())
            {
                var (position, path, droid) = queue.Dequeue();
                foreach (var (command, direction) in DIRECTIONS.Select(pair => (pair.Key, pair.Value)))
                {
                    var newPosition = position + direction;
                    if (!visited.Contains(newPosition))
                    {
                        visited.Add(newPosition);
                        var newDroid = droid.Clone();
                        newDroid.AddInput(command);
                        while (!newDroid.Outputing)
                            newDroid.Tick();
                        switch (newDroid.GetOutput())
                        {
                            case 2: // Oxygen Ssytem
                                if (stepsToOxygenSystem == 0)
                                    stepsToOxygenSystem = path.Count();
                                oxygenPosition = newPosition;
                                break;
                            case 1: // Open space
                                openSpaces.Add(newPosition);
                                while (!newDroid.Polling)
                                    newDroid.Tick();
                                var newPath = path.ToList();
                                newPath.Add(newPosition);
                                queue.Enqueue((newPosition, newPath, newDroid));
                                break;
                        }
                    }
                }
            }
            return (stepsToOxygenSystem, oxygenPosition, openSpaces);
        }

        static (int, int) Solve(long[] memory)
        {
            var (stepsToOxygenSystem, oxygenSystemPosition, openSpaces) = RunUntilOxygenSystem(memory);
            var openSpacesList = openSpaces.ToList();
            var filled = new List<Complex>();
            filled.Add(oxygenSystemPosition);
            var minutes = 0;
            while (openSpacesList.Any())
            {
                minutes++;
                foreach (var oxygen in filled.ToArray())
                    foreach(var direction in DIRECTIONS.Values)
                    {
                        var position = oxygen + direction;
                        if (openSpacesList.Contains(position))
                            filled.Add(position);
                            openSpacesList.Remove(position);
                    }
            }
            return (stepsToOxygenSystem, minutes);
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