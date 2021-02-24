using System;
using static System.Console;
using System.IO;
using System.Diagnostics;
using System.Linq;
using System.Collections.Generic;
using System.Text.RegularExpressions;

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

        public IntCodeComputer RunUntilPaused()
        {
            _paused = false;
            while (!_paused && Running)
                Tick();
            return this;
        }
        
        public void AddInput(long value) => _input.Enqueue(value);

        public IEnumerable<long> GetOutputs() => _output.ToArray();

        public long GetOutput()
        {
            Outputing = false;
            return _output.Pop();
        }

        public IEnumerable<long> GetAllOutput()
        {
            var output = _output.ToArray();
            _output.Clear();
            return output;
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
                        _paused = true;
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
        private bool _paused;

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
        static (string, IEnumerable<string>, IEnumerable<string>) ParseRoomOutput(string output)
        {
            var stage = 0;
            var room = string.Empty;
            var doors = new List<string>();
            var items = new List<string>();
            Match match;
            foreach (var line in output.Split("\n"))
                switch (stage)
                {
                    case 0:
                        match = Regex.Match(line, @"^== (?<room>.*) ==");
                        if (match.Success)
                        {
                            room = match.Groups["room"].Value;
                            stage = 1;
                        }
                        break;
                    case 1:
                        if (line.StartsWith("Doors"))
                            stage = 2;
                        break;
                    case 2:
                        match = Regex.Match(line, @"- (?<entry>.*)");
                        if (match.Success)
                            doors.Add(match.Groups["entry"].Value);
                        else
                            stage = 3;
                        break;
                    case 3:
                        if (line.StartsWith("Items"))
                            stage = 4;
                        break;
                    case 4:
                        match = Regex.Match(line, @"- (?<entry>.*)");
                        if (match.Success)
                            items.Add(match.Groups["entry"].Value);
                        else
                            break;
                        break;
                }
            return (room, doors, items);
        }

        static string RunCommand(IntCodeComputer droid, string command)
        {
            if (!string.IsNullOrEmpty(command))
                foreach (var c in command + "\n")
                    droid.AddInput((int)c);
            droid.RunUntilPaused();
            return string.Join("", droid.GetAllOutput().Reverse().Select(c => (char)c));
        }

        // use to play manually
        static void ManualScout(long[] memory)
        {
            WriteLine("Scounting");
            var droid = new IntCodeComputer(memory);
            var command = "";
            while (command != "quit" && droid.Running)
            {
                var output = RunCommand(droid, command);
                WriteLine(output);
                Write("$ ");
                command = ReadLine();
            }
        }

        static Dictionary<string, string> WAY_INVERSE = new Dictionary<string, string> {
            { "", "" },
            { "north", "south" },
            { "south", "north" },
            { "west", "east" },
            { "east", "west" }
        };
        static string[] FORBIDEN_ITEMS = new[] {
            "molten lava",
            "photons",
            "infinite loop",
            "giant electromagnet",
            "escape pod"
        };
        const string PRESSURE_ROOM = "Pressure-Sensitive Floor";
        const string SECURITY_CHECKPOINT = "Security Checkpoint";
        const string TAKE = "take ";

        static (string, IEnumerable<string>, string) NavigateRooms(IntCodeComputer droid, string command, string destination, bool pickupItems)
        {
            var visited = new List<string>();
            var wayIn = new Dictionary<string, string>();
            var lastDirection = string.Empty;
            var pressureRoomWayIn = string.Empty;
            var inventory = new List<string>();
            while (droid.Running)
            {
                var output = RunCommand(droid, command);
                var (room, doors, items) = ParseRoomOutput(output);
                if (room == destination)
                    break;
                if (room == PRESSURE_ROOM)
                    pressureRoomWayIn = lastDirection;
                if (!wayIn.ContainsKey(room))
                    wayIn[room] = lastDirection;
                if (pickupItems)
                    foreach (var item in items.Where(item => !FORBIDEN_ITEMS.Contains(item)))
                    {
                        RunCommand(droid, TAKE + item);
                        inventory.Add(item);
                    }
                var newDoor = false;
                foreach (var door in doors)
                    if (!visited.Contains($"{room},{door}"))
                    {
                        if (door == WAY_INVERSE[wayIn[room]])
                            continue;
                        newDoor = true;
                        visited.Add($"{room},{door}");
                        command = lastDirection = door;
                        break;
                    }
                if (!newDoor)
                {
                    if (string.IsNullOrEmpty(wayIn[room]))
                    {
                        // assume that first room only has 1 door
                        command = doors.First();
                        break;
                    }
                    command = WAY_INVERSE[wayIn[room]];
                }
            }
            return (command, inventory, pressureRoomWayIn);
        }
        
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

        const string DROP = "drop ";
        static string FindPassword(long[] memory)
        {
            var droid = new IntCodeComputer(memory);
            // navigate all rooms and pickup non-forbiden items
            var (command, inventory, pressureRoomWayIn) = NavigateRooms(droid, string.Empty, string.Empty, true);
            // go to Security Checkpoint
            NavigateRooms(droid, command, SECURITY_CHECKPOINT, false);
            // test combinations of items
            foreach (var newInventory in Combinations(inventory, 4))
            {
                foreach (var item in newInventory.Where(item => !inventory.Contains(item)))
                        RunCommand(droid, TAKE + item);
                foreach (var item in inventory.Where(item => !newInventory.Contains(item)))
                        RunCommand(droid, DROP + item);
                var output = RunCommand(droid, pressureRoomWayIn);
                var passwordMatch = Regex.Match(output, @"typing (?<password>\d+)", RegexOptions.Multiline);
                if (passwordMatch.Success)
                    return passwordMatch.Groups["password"].Value;
                inventory = newInventory.ToArray();
            }
            throw new Exception("Pasword not found");
        }


        static string Part1(long[] memory) => FindPassword(memory);

        static object Part2(object puzzleInput) => null;

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