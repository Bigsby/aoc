using System;
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
        public int OutputCount => _output.Count;
        public int InputCount => _input.Count;
        
        public IntCodeComputer(long[] memory, IEnumerable<long> input = default(List<long>), bool defaultInput = false, long defaultValue = -1)
        {
            _memory = new Memory(memory);
            _input = new Queue<long>(input ?? new long[0]);
            _output = new Stack<long>();
            _defaultInput = defaultInput;
            _defaultValue = defaultValue;
        }

        public long Run()
        {
            while (Running) Tick();
            return GetOutput();
        }

        public void AddInput(long value) => _input.Enqueue(value);

        public IEnumerable<long> GetOutputs() => _output.ToArray();

        public long GetOutput()
        {
            Outputing = false;
            return _output.Pop();
        }

        public void CleanInputs()
        {
            _input.Clear();
            Polling = false;
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
                    else if (_defaultInput)
                    {
                     
                        _memory[GetAddress(1, p1Mode)] = _defaultValue;
                        _pointer += 2;
                        Polling = true;
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
        private bool _defaultInput;
        private long _defaultValue;

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
        static long RunDroid(long[] memory, IEnumerable<string> instructions)
        {
            var droid = new IntCodeComputer(memory);
            foreach (var instruction in instructions)
            {
                foreach (var c in instruction)
                    droid.AddInput((long)c);
                droid.AddInput(10);
            }
            return droid.Run();
        }

        static long Part1(long[] memory)
        {
            var network = Enumerable.Range(0, 50).Select(address => new IntCodeComputer(memory, new long[] { address })).ToArray();
            while (true)
                foreach (var computer in network)
                {
                    computer.Tick();
                    if (computer.Outputing)
                    {
                        if (computer.OutputCount == 3)
                        {
                            var y = computer.GetOutput();
                            var x = computer.GetOutput();
                            var address = computer.GetOutput();
                            if (address == 255)
                                return y;
                            network[address].AddInput(x);
                            network[address].AddInput(y);
                        }
                    }
                    else if (computer.Polling && computer.InputCount == 0)
                        computer.AddInput(-1);
                }
        }

        static long Part2(long[] memory)
        {
            var network = Enumerable.Range(0, 50).Select(address => new IntCodeComputer(memory, new long[] { address }, true, -1)).ToArray();
            var sentYs = new List<long>();
            (long x, long y) natPacket = (0, 0);
            while (true)
            {
                foreach (var computer in network)
                {
                    computer.Tick();
                    if (computer.Outputing)
                        if (computer.OutputCount == 3)
                        {
                            var y = computer.GetOutput();
                            var x = computer.GetOutput();
                            var address = computer.GetOutput();
                            if (address == 255)
                                natPacket = (x, y);
                            else 
                            {
                                network[address].AddInput(x);
                                network[address].AddInput(y);
                            }
                        }
                }
                if (network.All(computer => computer.Polling))
                {
                    foreach (var computer in network)
                        computer.CleanInputs();
                    if (sentYs.Any() && natPacket.y == sentYs.Last())
                        return natPacket.y;
                    else
                        sentYs.Add(natPacket.y);
                    network[0].AddInput(natPacket.x);
                    network[0].AddInput(natPacket.y);
                }
            }
        }

        static (long, long) Solve(long[] memory)
            => (
                Part1(memory),
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