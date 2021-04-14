use num::complex::Complex;
use regex::Regex;
use std::collections::{HashMap, HashSet, VecDeque};

type Lattice = Complex<i32>;
type FileSystem = HashMap<Lattice, (i32, i32)>;

static DIRECTIONS: &'static [Lattice] = &[
    Lattice::new(0, -1),
    Lattice::new(-1, 0),
    Lattice::new(1, 0),
    Lattice::new(0, 1),
];

fn get_empty_and_non_viable_nodes(file_system: &FileSystem) -> (Lattice, Vec<Lattice>) {
    let node_names: Vec<Lattice> = file_system.keys().map(|l| *l).collect();
    let mut empty = Lattice::new(0, 0);
    let mut non_viable_nodes = HashSet::new();
    for this_node in &node_names {
        let this_used = file_system.get(&this_node).unwrap().1;
        if this_used == 0 {
            empty = *this_node;
            continue;
        }
        for other_node in &node_names {
            if other_node != this_node && this_used > file_system.get(&other_node).unwrap().0 {
                non_viable_nodes.insert(*this_node);
            }
        }
    }
    (empty, non_viable_nodes.iter().map(|l| *l).collect())
}

fn get_steps_to_target(
    nodes: &Vec<Lattice>,
    non_viable: &Vec<Lattice>,
    start: &Lattice,
    destination: &Lattice,
) -> usize {
    let mut visited = HashSet::new();
    visited.insert(*start);
    let mut queue = VecDeque::new();
    queue.push_back((*start, 0));
    while let Some((current_node, length)) = queue.pop_front() {
        for direction in DIRECTIONS {
            let new_node = current_node + direction;
            if new_node == *destination {
                return length + 1;
            }
            if nodes.contains(&new_node)
                && !non_viable.contains(&new_node)
                && visited.insert(new_node)
            {
                queue.push_back((new_node, length + 1));
            }
        }
    }
    panic!("Path not found");
}

fn solve(file_system: &FileSystem) -> (usize, usize) {
    let (empty, non_viable) = get_empty_and_non_viable_nodes(file_system);
    let nodes: Vec<Lattice> = file_system.keys().map(|l| *l).collect();
    let empty_destination_x = nodes.iter().map(|l| l.re).max().unwrap();
    (
        file_system.len() - non_viable.len() - 1,
        get_steps_to_target(
            &nodes,
            &non_viable,
            &empty,
            &Lattice::new(empty_destination_x, 0),
        ) + (empty_destination_x as usize - 1) * 5,
    )
}

fn get_input(file_path: &String) -> FileSystem {
    let line_regex =
        Regex::new(r"^/dev/grid/node-x(?P<x>\d+)-y(?P<y>\d+)\s+(?P<size>\d+)T\s+(?P<used>\d+)")
            .unwrap();
    std::fs::read_to_string(file_path)
        .expect("Error reading input file!")
        .lines()
        .filter_map(|line| line_regex.captures(line))
        .map(|cap| {
            (
                Lattice::new(
                    cap.name("x").unwrap().as_str().parse().unwrap(),
                    cap.name("y").unwrap().as_str().parse().unwrap(),
                ),
                (
                    cap.name("size").unwrap().as_str().parse().unwrap(),
                    cap.name("used").unwrap().as_str().parse().unwrap(),
                ),
            )
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
