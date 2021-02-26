using System;
using static System.Console;
using System.IO;
using System.Diagnostics;
using System.Linq;

namespace AoC
{
    class Elf
    {
        public int Position { get; }
        public Elf Next { get; set; }
        public Elf Previous { get; set; }

        public Elf(int position) => Position = position + 1;

        public void Remove()
        {
            Previous.Next = Next;
            Next.Previous = Previous;
        }
    }

    static class Program
    {
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

        static (int, int) Solve(int elfCount)
            => (
                Convert.ToInt32(Convert.ToString(elfCount, 2)[1..] + "1", 2),
                Part2(elfCount)
            );

        static int GetInput(string filePath)
            => !File.Exists(filePath) ? throw new FileNotFoundException(filePath)
            : int.Parse(File.ReadAllText(filePath));

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
