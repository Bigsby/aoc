using System;
using static System.Console;
using System.IO;
using System.Diagnostics;
using System.Linq;
using System.Collections.Generic;
using System.Numerics;

namespace AoC
{
    using Position = Complex;
    using Direction = Complex;
    using Map = Dictionary<Complex, MapItem>;

    enum MapItemType
    {
        Straight,
        Turn,
        Intersection
    }

    enum Orientation
    {
        Horizontal,
        Vertical
    }

    record MapItem(MapItemType type);

    record Straight : MapItem
    {
        public Orientation Orientation { get; }
        public Straight(Orientation orientation)
            : base(MapItemType.Straight) => Orientation = orientation;
    }

    record Turn : MapItem
    {
        public (Direction horizontal, Direction vertical) Directions { get; }
        public Turn((Direction, Direction) directions)
            : base(MapItemType.Turn) => Directions = directions;
    }

    record Intersection : MapItem
    {
        public Intersection() : base(MapItemType.Intersection) { }
    }

    class Cycle<T>
    {
        private IEnumerator<T> _enumerator;
        public Cycle(IEnumerable<T> source) => _enumerator = source.GetEnumerator();
        public T Next()
        {
            if (!_enumerator.MoveNext())
            {
                _enumerator.Reset();
                _enumerator.MoveNext();
            }
            return _enumerator.Current;
        }
    }

    class Train
    {
        public Position Position { get; private set; }
        public Direction Direction { get; set; }

        public void Tick() => Position += Direction;

        public void Turn() => Direction *= _directionCycle.Next();

        public Train Clone() => new Train(Position, Direction);

        public Train(Position position, Direction direction)
        {
            Position = position;
            Direction = direction;
        }

        static Direction[] DIRECTION_CHANGES = new[] { Direction.ImaginaryOne, 1, -Direction.ImaginaryOne };
        Cycle<Direction> _directionCycle = new Cycle<Direction>(DIRECTION_CHANGES);
    }

    static class Program
    {
        static Dictionary<Direction, char> TRAIN_CHAR = new Dictionary<Position, char>
        {
            { Direction.One, '>' },
            { -Direction.One, '<' },
            { Direction.ImaginaryOne, '^' },
            { -Direction.ImaginaryOne, 'v' }
        };
        static Dictionary<(Direction, Direction), char> TURN_CHAR = new Dictionary<(Direction, Direction), char>
        {
            { ( Direction.One,  Direction.ImaginaryOne), '\\' },
            { ( Direction.One, -Direction.ImaginaryOne), '/'  },
            { (-Direction.One,  Direction.ImaginaryOne), '/'  },
            { (-Direction.One, -Direction.ImaginaryOne), '\\' },
        };
        static void ShowMapArea(Map mapItems, Position start, Position end, IEnumerable<Train> trains)
        {
            for (var y = (int)start.Imaginary; y > (int)end.Imaginary - 1; y--)
            {
                for (var x = (int)start.Real; x < (int)end.Real + 1; x++)
                {
                    var position = new Position(x, y);
                    var c = ' ';
                    if (mapItems.ContainsKey(position))
                        switch (mapItems[position])
                        {
                            case Straight straight:
                                c = straight.Orientation == Orientation.Horizontal ? '-' : '|';
                                break;
                            case Intersection intersection:
                                c = '+';
                                break;
                            case Turn turn:
                                c = TURN_CHAR[turn.Directions];
                                break;
                        }
                    var train = trains.FirstOrDefault(train => train.Position == position);
                    if (train != null)
                        c = TRAIN_CHAR[train.Direction];
                    Write(c);
                }
                WriteLine();
            }
            WriteLine();
        }

        static void ShowTrain(Map mapItems, Train train, IEnumerable<Train> trains)
        {
            var offset = 40;
            var maxX = (int)mapItems.Keys.Max(p => p.Real);
            var maxY = (int)mapItems.Keys.Min(p => p.Imaginary);
            var startX = Math.Max(0, (int)train.Position.Real - offset);
            var endX = Math.Min(maxX, (int)train.Position.Real + offset);
            var startY = Math.Min(0, (int)train.Position.Imaginary + offset);
            var endY = Math.Max(maxY, (int)train.Position.Imaginary - offset);
            ShowMapArea(mapItems, new Position(startX, startY), new Position(endX, endY), trains);
        }

        static string PositionToString(Position position)
            => $"{(int)position.Real},{(int)Math.Abs(position.Imaginary)}";

        static (string, string) Solve((Map map, IEnumerable<Train> trains) data)
        {
            var (mapItems, trains) = data;
            var trainLocations = trains.ToDictionary(train => train.Position, train => train.Clone());
            var part1Result = string.Empty;
            while (true)
            {
                foreach (var position in trainLocations.Keys.ToArray().OrderBy(p => -p.Imaginary).ThenBy(p => p.Real))
                {
                    if (!trainLocations.ContainsKey(position))
                        continue;
                    var train = trainLocations[position];
                    trainLocations.Remove(position);
                    train.Tick();
                    if (trainLocations.ContainsKey(train.Position))
                    {
                        if (string.IsNullOrEmpty(part1Result))
                            part1Result = PositionToString(train.Position);
                        trainLocations.Remove(train.Position);
                    }
                    else
                        trainLocations[train.Position] = train;
                    switch (mapItems[train.Position])
                    {
                        case Intersection intersection:
                            train.Turn();
                            break;
                        case Turn turn:
                            train.Direction = train.Direction.Real != 0 ? turn.Directions.vertical : turn.Directions.horizontal;
                            break;
                    }
                }
                if (trainLocations.Count == 1)
                    return (part1Result, PositionToString(trainLocations.Keys.First()));
            }
        }

        static Dictionary<char, Direction> TRAINS = new Dictionary<char, Position>
        {
            { '>',  1 },
            { '<', -1 },
            { '^', Direction.ImaginaryOne },
            { 'v', -Direction.ImaginaryOne }
        };
        static char[] TURNS = new[] { '/', '\\' };
        static Dictionary<string, (Direction, Direction)> TURN_DIRECTIONS = new Dictionary<string, (Direction, Direction)>
        {
            { " /",  ( Direction.One, -Direction.ImaginaryOne) },
            { "-/",  (-Direction.One,  Direction.ImaginaryOne) },
            { "</",  (-Direction.One,  Direction.ImaginaryOne) },
            { ">/",  (-Direction.One,  Direction.ImaginaryOne) },
            { "+/",  (-Direction.One,  Direction.ImaginaryOne) },
            { "-\\", (-Direction.One, -Direction.ImaginaryOne) },
            { "<\\", (-Direction.One, -Direction.ImaginaryOne) },
            { ">\\", (-Direction.One, -Direction.ImaginaryOne) },
            { "+\\", (-Direction.One, -Direction.ImaginaryOne) },
            { " \\", ( Direction.One,  Direction.ImaginaryOne) }
        };
        static Dictionary<char, Orientation> STRAIGHTS = new Dictionary<char, Orientation>
        {
            { '-', Orientation.Horizontal },
            { '|', Orientation.Vertical }
        };
        const char INTERSECTION = '+';
        static char[] TURN_PREVIOUS = new[] { '-', '+', '<', '>' };
        static (Map map, IEnumerable<Train> trains) GetInput(string filePath)
        {
            if (!File.Exists(filePath)) throw new FileNotFoundException(filePath);
            var trains = new List<Train>();
            var map = new Map();
            var previousC = ' ';
            var trainPositionToFillIn = new List<Position>();
            var trainIndex = 0;
            foreach (var (line, y) in File.ReadLines(filePath).Select((line, y) => (line, y)))
                foreach (var (c, x) in line.Select((c, x) => (c, x)))
                {
                    var position = new Position(x, -y);
                    if (c == INTERSECTION)
                        map[position] = new Intersection();
                    else if (STRAIGHTS.ContainsKey(c))
                        map[position] = new Straight(STRAIGHTS[c]);
                    else if (TURNS.Contains(c))
                    {
                        if (!TURN_PREVIOUS.Contains(previousC))
                            previousC = ' ';
                        map[position] = new Turn(TURN_DIRECTIONS[new string(new[] { previousC, c })]);
                    }
                    else if (TRAINS.ContainsKey(c))
                    {
                        trains.Add(new Train(position, TRAINS[c]));
                        trainIndex++;
                        trainPositionToFillIn.Add(position);
                    }
                    previousC = c;
                }
            foreach (var position in trainPositionToFillIn)
                foreach (var direction in TRAINS.Values)
                    if (map.ContainsKey(position + direction))
                    {
                        var mapPosition = map[position + direction];
                        if (mapPosition.type == MapItemType.Straight)
                            map[position] = mapPosition;
                        else if (mapPosition.type == MapItemType.Intersection)
                            map[position] = new Straight(direction.Real != 0 ? Orientation.Horizontal : Orientation.Vertical);
                    }
            return (map, trains);
        }

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