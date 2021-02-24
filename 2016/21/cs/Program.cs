using System;
using static System.Console;
using System.IO;
using System.Diagnostics;
using System.Linq;
using System.Collections.Generic;

namespace AoC
{
    using Instruction = Tuple<int, int, int>;

    static class Program
    {
        const int SWAP_POSITION = 0;
        const int SWAP_LETTER = 1;
        const int ROTATE_LEFT = 2;
        const int ROTATE_RIGHT = 3;
        const int ROTATE_LETTER = 4;
        const int REVERSE = 5;
        const int MOVE = 6;

        static int IndexOf(int[] password, int find)
            => password.Select((c, index) => (c, index)).First(pair => pair.c == find).index;

        static void Rotate<T>(T[] array, int count)
        {
            if (array == null || array.Length < 2) return;
            count %= array.Length;
            if (count == 0) return;
            int left = count < 0 ? -count : array.Length + count;
            int right = count > 0 ? count : array.Length - count;
            if (left <= right)
                for (int i = 0; i < left; i++)
                {
                    var temp = array[0];
                    Array.Copy(array, 1, array, 0, array.Length - 1);
                    array[array.Length - 1] = temp;
                }
            else
                for (int i = 0; i < right; i++)
                {
                    var temp = array[array.Length - 1];
                    Array.Copy(array, 0, array, 1, array.Length - 1);
                    array[0] = temp;
                }
        }

        static string Process(string start, IEnumerable<Instruction> instructions, bool reverse = false)
        {
            var password = start.Select(c => (int)c).ToArray();
            if (reverse)
                instructions = instructions.Reverse();
            foreach (var (opCode, a, b) in instructions)
            {
                switch (opCode)
                {
                    case (SWAP_POSITION):
                        var oldA = password[a];
                        password[a] = password[b];
                        password[b] = oldA;
                        break;
                    case (SWAP_LETTER):
                        var indexOfA = IndexOf(password, a);
                        var indexOfB = IndexOf(password, b);
                        oldA = password[indexOfA];
                        password[indexOfA] = password[indexOfB];
                        password[indexOfB] = oldA;
                        break;
                    case (ROTATE_LEFT):
                        Rotate(password, reverse ? a : -a);
                        break;
                    case (ROTATE_RIGHT):
                        Rotate(password, reverse ? -a : a);
                        break;
                    case (ROTATE_LETTER):
                        indexOfA = IndexOf(password, a);
                        var rotation = indexOfA + 1 + (indexOfA >= 4 ? 1 : 0);
                        if (reverse)
                            rotation = -(indexOfA / 2 + (indexOfA % 2 == 1 || indexOfA == 0 ? 1 : 5));
                        Rotate(password, rotation);
                        break;
                    case (REVERSE):
                        var prefix = password[Range.EndAt(a)];
                        var middle = password[new Range(a, b + 1)];
                        middle = middle.Reverse().ToArray();
                        var sufix = password[Range.StartAt(b + 1)];
                        password = prefix.Concat(middle.Concat(sufix)).ToArray();
                        break;
                    case (MOVE):
                        var (origin, destination) = reverse ? (b, a) : (a, b);
                        var letterToMove = password[origin];
                        var list = password.ToList();
                        list.Remove(letterToMove);
                        list.Insert(destination, letterToMove);
                        password = list.ToArray();
                        break;
                }
            }
            return new string(password.Select(c => (char)c).ToArray());
        }

        static string Part1(IEnumerable<Instruction> instructions)
            => Process("abcdefgh", instructions);

        static string Part2(IEnumerable<Instruction> instructions)
            => Process("fbgdceah", instructions, true);

        static Dictionary<string, Func<string, Instruction>> INSTRUCTION_PARSER = new Dictionary<string, Func<string, Instruction>> {
            { "swap position", line => Tuple.Create(SWAP_POSITION, int.Parse(line[14].ToString()), int.Parse(line[^1].ToString())) },
            { "swap letter", line => Tuple.Create(SWAP_LETTER, (int)line[12], (int)line[^1]) },
            { "rotate left", line => Tuple.Create(ROTATE_LEFT, int.Parse(line[12].ToString()), 0) },
            { "rotate right", line => Tuple.Create(ROTATE_RIGHT, int.Parse(line[13].ToString()), 0) },
            { "rotate based", line => Tuple.Create(ROTATE_LETTER, (int)line[^1], 0) },
            { "reverse", line => Tuple.Create(REVERSE, int.Parse(line[18].ToString()), int.Parse(line[^1].ToString())) },
            { "move", line => Tuple.Create(MOVE, int.Parse(line[14].ToString()), int.Parse(line[^1].ToString())) }
        };
        static IEnumerable<Instruction> GetInput(string filePath)
        {
            if (!File.Exists(filePath)) throw new FileNotFoundException(filePath);
            return File.ReadLines(filePath).Select(line =>
            {
                foreach (var start in INSTRUCTION_PARSER.Keys)
                    if (line.StartsWith(start))
                        return INSTRUCTION_PARSER[start](line);
                throw new Exception($"Unknown instruction '{line}'");
            });
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
