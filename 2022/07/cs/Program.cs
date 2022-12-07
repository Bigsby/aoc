using System;
using static System.Console;
using System.IO;
using System.Diagnostics;
using System.Linq;
using System.Collections.Generic;

namespace AoC
{
    using Input = IEnumerable<string[]>;

    readonly record struct FileData(string Name, int Size);

    class Directory
    {
        public Directory(string name, Directory parent)
        {
            Name = name;
            Parent = parent;
        }

        public string Name { get; init; }
        public Directory Parent { get; init; }
        public readonly IList<FileData> Files = new List<FileData>();
        public readonly IList<Directory> Children = new List<Directory>();

        public int GetSize()
            => Files.Sum(file => file.Size) + Children.Sum(child => child.GetSize());
    }

    static class Program
    {
        static IEnumerable<int> GetAllSizes(Directory directory)
        {
            yield return directory.GetSize();
            foreach (var child in directory.Children)
                foreach (var size in GetAllSizes(child))
                    yield return size;
        }

        static Directory BuildFileSystem(Input output)
        {
            var root = new Directory("/", null);
            var current = root;
            foreach (var line in output)
                if (line[0] == "$")
                {
                    if (line[1] == "cd")
                        switch (line[2])
                        {
                            case "..":
                                current = current.Parent;
                                break;
                            case "/":
                                break;
                            default:
                                var newDirectory = new Directory(line[2], current);
                                current.Children.Add(newDirectory);
                                current = newDirectory;
                                break;
                        }
                }
                else if (line[0] != "dir")
                    current.Files.Add(new FileData(line[1], int.Parse(line[0])));
            return root;
        }

        static int Part1(IEnumerable<int> sizes)
            => sizes.Where(size => size <= 100_000).Sum();

        static int Part2(IEnumerable<int> sizes)
        {
            var freeSpace = 70_000_000 - sizes.Max();
            var minimumToDelete = 30_000_000 - freeSpace;
            return sizes.Where(size => size >= minimumToDelete).Min();
        }

        static (int, int) Solve(Input puzzleInput)
        {
            var sizes = GetAllSizes(BuildFileSystem(puzzleInput)).ToArray();
            return (Part1(sizes), Part2(sizes));
        }

        static Input GetInput(string filePath)
            => !File.Exists(filePath) ? throw new FileNotFoundException(filePath)
            : File.ReadAllLines(filePath).Select(line => line.Split(" "));

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
