use num::complex::Complex;
use std::cmp::Ordering;
use std::collections::{BinaryHeap, HashMap, HashSet, VecDeque};

type Position = Complex<i32>;
type Maze = Vec<Position>;
type KeysDoors = HashMap<Position, u8>;

#[derive(Eq, PartialEq)]
struct Node {
    distance: usize,
    current_points: Vec<u8>,
    keys_found: HashSet<u8>,
}

impl Ord for Node {
    fn cmp(&self, other: &Self) -> Ordering {
        other.distance.cmp(&self.distance)
    }
}

impl PartialOrd for Node {
    fn partial_cmp(&self, other: &Self) -> Option<Ordering> {
        Some(self.cmp(other))
    }
}

fn _show_maze(maze: &Maze, keys_doors: &KeysDoors, starts: &Vec<Position>) {
    let max_x = maze.iter().map(|p| p.re).max().unwrap();
    let max_y = maze.iter().map(|p| p.im).max().unwrap();
    for y in 0..max_y + 1 {
        for x in 0..max_x + 1 {
            let mut c = '.';
            let position = Position::new(x, y);
            if maze.contains(&position) {
                c = '#';
            }
            if let Some(key_door) = keys_doors.get(&position) {
                c = *key_door as char;
            }
            if starts.contains(&position) {
                c = '@';
            }
            print!("{}", c);
        }
        println!();
    }
    println!();
}

static DIRECTIONS: &'static [Position] = &[
    Position::new(-1, 0),
    Position::new(0, -1),
    Position::new(1, 0),
    Position::new(0, 1),
];

fn find_paths_from_position(
    maze: &Maze,
    keys_doors: &KeysDoors,
    start: Position,
) -> HashMap<u8, (usize, HashSet<u8>)> {
    let mut visited = HashSet::new();
    visited.insert(start);
    let mut queue: VecDeque<(Position, usize, HashSet<u8>)> = VecDeque::new();
    queue.push_back((start, 0, HashSet::new()));
    let mut paths = HashMap::new();
    while let Some((position, distance, required_keys)) = queue.pop_front() {
        for direction in DIRECTIONS {
            let new_position = position + direction;
            if !maze.contains(&new_position) && visited.insert(new_position) {
                let mut new_required_keys = required_keys.clone();
                if let Some(key_door) = keys_doors.get(&new_position) {
                    if *key_door > b'Z' {
                        // lower case
                        paths.insert(*key_door, (distance + 1, required_keys.clone()));
                    } else {
                        new_required_keys.insert(*key_door + 32);
                    }
                }
                queue.push_back((new_position, distance + 1, new_required_keys));
            }
        }
    }
    paths
}

fn find_shortest_path_from_key_gragph(
    paths_from_keys: &HashMap<u8, HashMap<u8, (usize, HashSet<u8>)>>,
    keys: &HashMap<u8, Position>,
    entrances: &Vec<u8>,
) -> usize {
    let mut paths = BinaryHeap::new();
    paths.push(Node {
        distance: 0,
        current_points: entrances.clone(),
        keys_found: HashSet::new(),
    });
    let mut visited: HashMap<String, usize> = HashMap::new();
    while let Some(Node {
        distance,
        current_points,
        keys_found,
    }) = paths.pop()
    {
        if keys_found.len() == keys.len() {
            return distance;
        }
        for (current_index, current_key) in current_points.iter().enumerate() {
            for (next_key, next_path) in paths_from_keys.get(&current_key).unwrap() {
                if !keys_found.contains(&next_key) {
                    let mut next_keys = keys_found.clone();
                    next_keys.insert(*next_key);
                    let mut next_positions: Vec<u8> = current_points.iter().map(|p| *p).collect();
                    next_positions[current_index] = *next_key;
                    let node_id = format!("{:?}|{:?}", next_positions, next_keys);
                    let new_distance = distance + next_path.0;
                    if next_path.1.is_subset(&keys_found)
                        && (!visited.contains_key(&node_id)
                            || visited.get(&node_id).unwrap() > &new_distance)
                    {
                        paths.push(Node {
                            distance: new_distance,
                            current_points: next_positions,
                            keys_found: next_keys,
                        });
                        visited.insert(node_id, new_distance);
                    }
                }
            }
        }
    }
    panic!("Path not found")
}

fn find_shortest_path(maze: &Maze, keys_doors: &KeysDoors, entrances: &Vec<Position>) -> usize {
    let keys: HashMap<u8, Position> = keys_doors
        .iter()
        .filter(|(_, key_door)| **key_door > b'Z')
        .map(|(position, key_door)| (*key_door, *position))
        .collect();
    let mut keys_paths: HashMap<u8, HashMap<u8, (usize, HashSet<u8>)>> = keys
        .iter()
        .map(|(key, position)| (*key, find_paths_from_position(maze, keys_doors, *position)))
        .collect();
    for (index, position) in entrances.iter().enumerate() {
        keys_paths.insert(
            index as u8,
            find_paths_from_position(maze, keys_doors, *position),
        );
    }
    find_shortest_path_from_key_gragph(
        &keys_paths,
        &keys,
        &entrances
            .iter()
            .enumerate()
            .map(|(index, _)| index as u8)
            .collect(),
    )
}

fn solve(data: &(Maze, KeysDoors, Position)) -> (usize, usize) {
    let (maze, keys_doors, start) = data;
    let part1_result = find_shortest_path(maze, keys_doors, &vec![*start]);
    let mut maze = maze.clone();
    for offset in vec![
        Position::new(-1, 0),
        Position::new(0, -1),
        Position::new(1, 0),
        Position::new(0, 1),
    ] {
        maze.push(start + offset);
    }
    let entrances = vec![
        Position::new(-1, -1),
        Position::new(1, -1),
        Position::new(-1, 1),
        Position::new(1, 1),
    ]
    .into_iter()
    .map(|offset| start + offset)
    .collect();
    (
        part1_result,
        find_shortest_path(&maze, keys_doors, &entrances),
    )
}

fn get_input(file_path: &String) -> (Maze, KeysDoors, Position) {
    let mut maze = Maze::new();
    let mut keys_doors = KeysDoors::new();
    let mut entrance = Position::new(0, 0);
    for (y, line) in std::fs::read_to_string(file_path)
        .expect("Error reading input file!")
        .lines()
        .enumerate()
    {
        for (x, c) in line.chars().enumerate() {
            let position = Position::new(x as i32, y as i32);
            if c == '#' {
                maze.push(position);
            } else if c == '@' {
                entrance = position;
            } else if c != '.' {
                keys_doors.insert(position, c as u8);
            }
        }
    }
    (maze, keys_doors, entrance)
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
