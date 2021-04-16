use itertools::Itertools;
use num::Complex;
use std::collections::{HashMap, HashSet, VecDeque};

type Lattice = Complex<i32>;
type Maze = Vec<Lattice>;

static DIRECTIONS: &'static [Lattice] = &[
    Lattice::new(-1, 0),
    Lattice::new(0, -1),
    Lattice::new(1, 0),
    Lattice::new(0, 1),
];

fn find_paths_from_location(
    maze: &Maze,
    numbers: &HashMap<Lattice, u8>,
    start: &Lattice,
) -> HashMap<u8, usize> {
    let mut visited = HashSet::new();
    visited.insert(*start);
    let mut queue = VecDeque::new();
    queue.push_back((*start, 0));
    let mut paths = HashMap::new();
    while let Some((position, distance)) = queue.pop_front() {
        for direction in DIRECTIONS {
            let new_position = position + direction;
            if maze.contains(&new_position) && visited.insert(new_position) {
                if numbers.contains_key(&new_position) {
                    paths.insert(numbers[&new_position], distance + 1);
                }
                queue.push_back((new_position, distance + 1));
            }
        }
    }
    paths
}

fn get_steps_for_path(
    path: &Vec<&u8>,
    paths_from_numbers: &HashMap<u8, HashMap<u8, usize>>,
    return_home: bool,
) -> usize {
    let mut steps = 0;
    let mut current = 0;
    let mut path: VecDeque<u8> = path.iter().map(|n| **n).collect();
    while !path.is_empty() {
        let next = path.pop_front().unwrap();
        steps += paths_from_numbers[&current][&next];
        current = next;
    }
    if return_home {
        steps += paths_from_numbers[&current][&0];
    }
    steps
}

fn solve(data: &(Maze, HashMap<Lattice, u8>)) -> (usize, usize) {
    let (maze, numbers) = data;
    let paths_from_numbers: HashMap<u8, HashMap<u8, usize>> = numbers
        .iter()
        .map(|(position, number)| (*number, find_paths_from_location(maze, numbers, position)))
        .collect();
    let numbers_besides_start: Vec<u8> = numbers
        .values()
        .copied()
        .filter(|number| *number != 0)
        .collect();
    let mut minimum_steps = usize::MAX;
    let mut return_minimum_steps = usize::MAX;
    for combination in numbers_besides_start
        .iter()
        .permutations(numbers_besides_start.len())
    {
        minimum_steps =
            minimum_steps.min(get_steps_for_path(&combination, &paths_from_numbers, false));
        return_minimum_steps =
            return_minimum_steps.min(get_steps_for_path(&combination, &paths_from_numbers, true));
    }
    (minimum_steps, return_minimum_steps)
}

fn get_input(file_path: &String) -> (Maze, HashMap<Lattice, u8>) {
    let mut maze = Maze::new();
    let mut numbers = HashMap::new();
    for (y, line) in std::fs::read_to_string(file_path)
        .expect("Error reading input file!")
        .lines()
        .enumerate()
    {
        for (x, c) in line.chars().enumerate() {
            let position = Lattice::new(x as i32, y as i32);
            if c == '.' {
                maze.push(position);
            } else if c.is_digit(10) {
                numbers.insert(position, c as u8 - 48);
                maze.push(position);
            }
        }
    }
    (maze, numbers)
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
