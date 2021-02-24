using System;
using static System.Console;
using System.IO;
using System.Diagnostics;
using System.Linq;

namespace AoC
{
    class Elf
    {
        public int Position { get; init; }
        public Elf Next { get; set; }
        public Elf Previous { get; set; }

        public Elf(int position)
        {
            Position = position + 1;
            Next = this;
            Previous = this;
        }

        public void Remove()
        {
            Previous.Next = Next;
            Next.Previous = Previous;
        }
    }

    static class Program
    {
        static int Part1(int elfCount)
            => Convert.ToInt32(Convert.ToString(elfCount, 2)[1..] + "1", 2);

        static int Part2(int elfCount)
        {
            var elves = Enumerable.Range(0, elfCount).Select(position => new Elf(position)).ToArray();
            for (var index = 0; index < elfCount; index++)
            {
                elves[index].Next = elves[(index + 1) % elfCount];
                elves[index].Previous = elves[index == 0 ? elfCount - 1 : (index - 1) % elfCount];
            }
            var currentElf = elves[0];
            var elfToRemove = elves[elfCount / 2];
            for (var index = 0; index < elfCount - 1; index++)
            {
                elfToRemove.Remove();
                elfToRemove = elfToRemove.Next;
                if ((elfCount - index) % 2 == 1)
                    elfToRemove = elfToRemove.Next;
                currentElf = currentElf.Next;
            }
            return currentElf.Position;
        }

        static int GetInput(string filePath)
        {
            if (!File.Exists(filePath)) throw new FileNotFoundException(filePath);
            return int.Parse(File.ReadAllText(filePath));
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
