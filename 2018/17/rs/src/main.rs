use num::Complex;
use regex::Regex;
use std::collections::HashSet;

type Position = Complex<i32>;
type ClaySquares = Vec<Position>;
type Water = HashSet<Position>;
static UP: Position = Position::new(0, -1);
static DOWN: Position = Position::new(0, 1);

fn find_edge(spring: Position, direction: i32, settled: &Water, clay: &ClaySquares) -> (i32, bool) {
    let mut x = direction;
    loop {
        let current = spring + x;
        if clay.contains(&current) {
            return (x - direction, false);
        }
        let below = current + DOWN;
        if !clay.contains(&below) && !settled.contains(&below) {
            return (x, true);
        }
        x += direction;
    }
}

// def find_edge(spring: Position, direction: int, settled: Water, clay: ClaySquares) -> Tuple[int, bool]:
//     x = direction
//     while True:
//         current = spring + x
//         if current in clay:
//             return x - direction, False
//         below = current + 1j
//         if below not in clay and below not in settled:
//             return x, True
//         x += direction

// def solve(clay: ClaySquares) -> Tuple[int, int]:
//     maxY = int(max(map(lambda s: s.imag, clay)))
//     minY = int(min(map(lambda s: s.imag, clay)))
//     settled: Water = set()
//     flowing: Water = set()
//     queue = [500 + minY * 1j]
//     while queue:
//         spring = queue.pop()
//         below = spring + 1j
//         if below in flowing:
//             continue
//         flowing.add(spring)
//         while below.imag <= maxY and below not in clay and below not in settled:
//             flowing.add(below)
//             below += 1j
//         if below in clay or below in settled:
//             x, y = int(below.real), below.imag * 1j - 1j
//             left_offset, left_overflown = find_edge(
//                 below - 1j, -1, settled, clay)
//             right_offset, right_overflown = find_edge(
//                 below - 1j, 1, settled, clay)
//             is_overflown = left_overflown or right_overflown
//             if not is_overflown:
//                 queue.append(below - 2j)
//             for levelX in range(x + left_offset, x + right_offset + 1):
//                 position = levelX + y
//                 if is_overflown:
//                     flowing.add(position)
//                 else:
//                     settled.add(position)
//                     if position in flowing:
//                         flowing.remove(position)
//                     if position in queue:
//                         queue.remove(position)
//             if left_overflown:
//                 queue.append(x + left_offset + y)
//             if right_overflown:
//                 queue.append(x + right_offset + y)
//     return len(settled) + len(flowing), len(settled)|

fn solve(clay: &ClaySquares) -> (usize, usize) {
    let max_y = clay.iter().map(|p| p.im).max().unwrap();
    let min_y = clay.iter().map(|p| p.im).min().unwrap();
    let mut settled = Water::new();
    let mut flowing = Water::new();
    let mut queue = Vec::new();
    queue.push(Position::new(500, min_y));
    while let Some(spring) = queue.pop() {
        let mut below = spring + DOWN;
        if flowing.contains(&below) {
            continue;
        }
        flowing.insert(below);
        while below.im <= max_y && !clay.contains(&below) && !settled.contains(&below) {
            flowing.insert(below);
            below += DOWN;
        }
        if clay.contains(&below) || settled.contains(&below) {
            let (x, y) = (below.re, Position::new(0, below.im - 1));
            let (left_offset, left_overflown) = find_edge(below + UP, -1, &settled, clay);
            let (right_offset, right_overflown) = find_edge(below + UP, 1, &settled, clay);
            let is_overflown = left_overflown || right_overflown;
            if !is_overflown {
                queue.push(below + 2 * UP);
            }
            for leve_x in x + left_offset..x + right_offset + 1 {
                let position = leve_x + y;
                if is_overflown {
                    flowing.insert(position);
                } else {
                    settled.insert(position);
                    flowing.remove(&position);
                    if let Some(index) = queue.iter().position(|p| *p == position) {
                        queue.remove(index);
                    }
                }
            }
            if left_overflown {
                queue.push(x + left_offset + y);
            }
            if right_overflown {
                queue.push(x + right_offset + y);
            }
        }
    }
    (settled.len() + flowing.len(), settled.len())
}

// def parse_line(line: str) -> ClaySquares:
//     match = lineRegex.match(line)
//     if match:
//         result: ClaySquares = []
//         sC, sV, mS, mE = match.group("sC"), int(match.group("sV")), int(
//             match.group("mS")), int(match.group("mE"))
//         if sC == "x":
//             for y in range(mS, mE + 1):
//                 result.append(sV + y * 1j)
//         else:
//             for x in range(mS, mE + 1):
//                 result.append(x + sV * 1j)
//         return result
//     raise Exception("Bad format", line)

// def get_input(file_path: str) -> ClaySquares:
//     if not os.path.isfile(file_path):
//         raise FileNotFoundError(file_path)

//     with open(file_path, "r") as file:
//         clay: ClaySquares = []
//         for line in file.readlines():
//             clay += parse_line(line)
//         return clay

fn get_input(file_path: &String) -> ClaySquares {
    let line_regex =
        Regex::new(r"^(?P<sC>x|y)=(?P<sV>\d+), (?:x|y)=(?P<mS>\d+)..(?P<mE>\d+)$").unwrap();
    let mut clay = ClaySquares::new();
    for line in std::fs::read_to_string(file_path)
        .expect("Error reading input file!")
        .lines()
    {
        if let Some(cap) = line_regex.captures(line) {
            let (sc, sv, ms, me) = (
                cap.name("sC").unwrap().as_str(),
                cap.name("sV").unwrap().as_str().parse::<i32>().unwrap(),
                cap.name("mS").unwrap().as_str().parse::<i32>().unwrap(),
                cap.name("mE").unwrap().as_str().parse::<i32>().unwrap(),
            );
            if sc == "x" {
                for y in ms..me + 1 {
                    clay.push(Position::new(sv, y));
                }
            } else {
                for x in ms..me + 1 {
                    clay.push(Position::new(x, sv));
                }
            }
        }
    }
    clay
}

fn main() {
    let args: Vec<String> = std::env::args().collect();
    if args.len() != 2 {
        panic!("Please, add input file path as parameter");
    }
    let now = std::time::Instant::now();
    let (part1_result, part2_result) = solve(&get_input(&args[1]));
    let end = now.elapsed().as_secs_f32();
    println!("P1: {}", part1_result);
    println!("P2: {}", part2_result);
    println!();
    println!("Time: {:.7}", end);
}
