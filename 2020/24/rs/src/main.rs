use num::Complex;
use regex::Regex;
use std::collections::{HashMap, HashSet};

type Directions = Vec<String>;
type Tile = Complex<i32>;
type Floor = HashMap<Tile, bool>;

static DIRECTIONS: &'static [Tile] = &[
    Tile::new(1, 0),
    Tile::new(0, 1),
    Tile::new(-1, 1),
    Tile::new(-1, 0),
    Tile::new(1, -1),
    Tile::new(0, -1),
];

fn flip_initial_tiles(tile_paths: &Vec<Directions>) -> Floor {
    let mut floor = Floor::new();
    let directions: HashMap<&str, Tile> = vec![
        ("e", Tile::new(1, 0)),
        ("se", Tile::new(0, 1)),
        ("sw", Tile::new(-1, 1)),
        ("w", Tile::new(-1, 0)),
        ("ne", Tile::new(1, -1)),
        ("nw", Tile::new(0, -1)),
    ]
    .into_iter()
    .collect();
    for path in tile_paths {
        let mut current = Tile::new(0, 0);
        for direction in path {
            current += directions.get(direction.as_str()).unwrap();
        }
        floor
            .entry(current)
            .and_modify(|value| *value = !*value)
            .or_insert(true);
    }
    floor
}

fn get_black_count(tile: &Tile, floor: &Floor) -> usize {
    DIRECTIONS
        .iter()
        .map(|direction| tile + *direction)
        .filter(|neighbor| *floor.get(neighbor).unwrap_or(&false))
        .count()
}

fn get_tile_state(tile: &Tile, floor: &Floor) -> bool {
    *floor.get(tile).unwrap_or(&false)
}

fn get_new_state(tile: &Tile, floor: &Floor) -> bool {
    let adjacent_black_count = get_black_count(tile, floor);
    let tile_state = get_tile_state(tile, floor);
    if tile_state && adjacent_black_count == 0 || adjacent_black_count > 2 {
        false
    } else {
        (!tile_state && adjacent_black_count == 2) || tile_state
    }
}

fn run_day(floor: &Floor) -> Floor {
    let mut new_floor = Floor::new();
    let mut edges_to_test = HashSet::new();
    for tile in floor.keys() {
        for neighbor in DIRECTIONS.iter().map(|direction| tile + *direction) {
            if !floor.contains_key(&neighbor) {
                edges_to_test.insert(neighbor);
            }
        }
        new_floor.insert(*tile, get_new_state(tile, floor));
    }
    for tile in edges_to_test {
        new_floor.insert(tile, get_new_state(&tile, floor));
    }
    new_floor
}

fn part2(floor: &Floor) -> usize {
    let mut floor: Floor = floor.clone();
    for _ in 0..100 {
        floor = run_day(&floor)
    }
    floor.values().filter(|v| **v).count()
}

fn solve(tile_paths: &Vec<Directions>) -> (usize, usize) {
    let floor = flip_initial_tiles(tile_paths);
    (floor.values().filter(|v| **v).count(), part2(&floor))
}

fn get_input(file_path: &String) -> Vec<Directions> {
    let line_regex = Regex::new(r"e|se|sw|w|nw|ne").unwrap();
    std::fs::read_to_string(file_path)
        .expect("Error reading input file!")
        .lines()
        .map(|line| {
            line_regex
                .captures_iter(line)
                .map(|cap| String::from(cap.get(0).unwrap().as_str()))
                .collect()
        })
        .collect()
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
