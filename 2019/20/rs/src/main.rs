use num::complex::Complex;
use std::cmp::Ordering;
use std::collections::{BinaryHeap, HashMap, HashSet, VecDeque};

type Lattice = Complex<i32>;
type Lattice3D = (Lattice, isize);
type Maze = Vec<Lattice>;
type Portals = HashMap<Lattice, usize>;
static DIRECTIONS: &'static [Lattice] = &[
    Lattice::new(0, 1),
    Lattice::new(0, -1),
    Lattice::new(1, 0),
    Lattice::new(-1, 0),
];
static START: &'static str = "AA";
static END: &'static str = "ZZ";

#[derive(Eq, PartialEq)]
struct Node {
    lattice: Lattice3D,
    distance: usize,
}
impl Ord for Node {
    fn cmp(&self, other: &Self) -> Ordering {
        other.distance.cmp(&self.distance)
    }
}
impl PartialOrd for Node {
    fn partial_cmp(&self, other: &Self) -> Option<Ordering> {
        Some(other.distance.cmp(&self.distance))
    }
}

fn _show_maze(maze: &Maze, portals: &Portals) {
    let min_x = maze.iter().map(|p| p.re).min().unwrap();
    let max_x = maze.iter().map(|p| p.re).max().unwrap();
    let min_y = maze.iter().map(|p| p.im).min().unwrap();
    let max_y = maze.iter().map(|p| p.im).max().unwrap();

    for y in min_y..max_y + 1 {
        for x in min_x..max_x + 1 {
            let lattice = Lattice::new(x, y);
            let mut c = '#';
            if maze.contains(&lattice) {
                c = '.';

                if let Some(portal) = portals.get(&lattice) {
                    c = (*portal as u8 + 48) as char;
                }
            }
            print!("{}", c);
        }
        println!();
    }
    println!();
}

fn part1(puzzle_input: &(Maze, Portals, Lattice, Lattice)) -> usize {
    let (maze, portals, start, end) = puzzle_input;
    let mut visited = HashSet::new();
    visited.insert(*start);
    let mut queue = VecDeque::new();
    queue.push_back((*start, 1));
    while let Some((lattice, distance)) = queue.pop_front() {
        let mut new_positions = Vec::new();
        if lattice != *start {
            if let Some(portal) = portals.get(&lattice) {
                new_positions.push(
                    portals
                        .iter()
                        .filter(|(l, p)| *p == portal && **l != lattice)
                        .map(|(l, _)| *l)
                        .next()
                        .unwrap(),
                );
            }
        }
        for direction in DIRECTIONS {
            new_positions.push(lattice + direction);
        }
        for new_position in new_positions {
            if new_position == *end {
                return distance;
            }
            if maze.contains(&new_position) && visited.insert(new_position) {
                queue.push_back((new_position, distance + 1));
            }
        }
    }
    panic!("Path not found")
}

fn find_paths_from_portal(
    maze: &Maze,
    portals: &Portals,
    portal: &Lattice,
) -> Vec<(Lattice, usize)> {
    let mut paths = Vec::new();
    let mut visited = HashSet::new();
    visited.insert(*portal);
    let mut queue = VecDeque::new();
    queue.push_back((*portal, 0));
    while let Some((lattice, distance)) = queue.pop_front() {
        for direction in DIRECTIONS {
            let new_lattice = lattice + direction;
            if distance != 0 && portals.contains_key(&new_lattice) {
                paths.push((new_lattice, distance + 1));
            } else if maze.contains(&new_lattice) && visited.insert(new_lattice) {
                queue.push_back((new_lattice, distance + 1));
            }
        }
    }
    paths
}

fn build_graph(maze: &Maze, portals: &Portals) -> HashMap<Lattice, Vec<(Lattice, usize)>> {
    let mut graph = HashMap::new();
    for (lattice, _) in portals {
        graph.insert(*lattice, find_paths_from_portal(maze, portals, lattice));
    }
    graph
}

fn part2(data: &(Maze, Portals, Lattice, Lattice)) -> usize {
    let (maze, portals, start, end) = data;
    let min_x = maze.iter().map(|p| p.re).min().unwrap();
    let max_x = maze.iter().map(|p| p.re).max().unwrap();
    let min_y = maze.iter().map(|p| p.im).min().unwrap();
    let max_y = maze.iter().map(|p| p.im).max().unwrap();
    let graph = build_graph(maze, portals);
    let portal_directions = portals
        .iter()
        .map(|(lattice, _)| {
            (
                *lattice,
                lattice.re == min_x
                    || lattice.re == max_x
                    || lattice.im == min_y
                    || lattice.im == max_y,
            )
        })
        .collect::<HashMap<Lattice, bool>>();
    let portal_pairs: HashMap<Lattice, Lattice> = portals
        .iter()
        .filter(|(lattice, _)| *lattice != start && *lattice != end)
        .map(|(lattice, label)| {
            (
                *lattice,
                portals
                    .iter()
                    .filter_map(|(other_lattice, other_label)| {
                        if other_label == label && other_lattice != lattice {
                            Some(*other_lattice)
                        } else {
                            None
                        }
                    })
                    .next()
                    .unwrap(),
            )
        })
        .collect();
    let mut visited = HashSet::new();
    let mut queue = BinaryHeap::new();
    queue.push(Node {
        lattice: (*start, 0),
        distance: 0,
    });
    loop {
        let Node {
            lattice: (lattice, level),
            distance,
        } = queue.pop().unwrap();
        visited.insert((lattice, level));
        if lattice == *end && level == 0 {
            return distance;
        }
        for (next_portal, new_distance) in graph.get(&lattice).unwrap() {
            if next_portal == start {
                continue;
            }
            if next_portal == end {
                if level == 0 {
                    queue.push(Node {
                        lattice: (*next_portal, 0),
                        distance: distance + new_distance,
                    })
                }
                continue;
            }
            if *portal_directions.get(&next_portal).unwrap() {
                let next_lattice3d = (*portal_pairs.get(next_portal).unwrap(), level + 1);
                if level < 0 && !visited.contains(&next_lattice3d) {
                    queue.push(Node {
                        lattice: next_lattice3d,
                        distance: distance + new_distance + 1,
                    });
                }
            } else if !visited.contains(&(lattice, level - 1)) {
                let next_lattice3d = (*portal_pairs.get(next_portal).unwrap(), level - 1);
                if !visited.contains(&next_lattice3d) {
                    queue.push(Node {
                        lattice: next_lattice3d,
                        distance: distance + new_distance + 1,
                    });
                }
            }
        }
    }
}

fn solve(puzzle_input: &(Maze, Portals, Lattice, Lattice)) -> (usize, usize) {
    (part1(puzzle_input), part2(puzzle_input))
}

fn get_input(file_path: &String) -> (Maze, Portals, Lattice, Lattice) {
    let mut maze = Maze::new();
    let mut portals = Portals::new();
    let mut start = Lattice::new(0, 0);
    let mut end = Lattice::new(0, 0);
    let mut portal_indexes: Vec<String> = Vec::new();
    let get_portal_index = &mut |portal| {
        if let Some(index) = portal_indexes.iter().position(|p| *p == portal) {
            index
        } else {
            portal_indexes.push(portal);
            portal_indexes.len() - 1
        }
    };
    let lines = std::fs::read_to_string(file_path)
        .expect("Error reading input file!")
        .lines()
        .map(|line| line.chars().collect())
        .collect::<Vec<Vec<char>>>();
    for (y, line) in lines.iter().enumerate() {
        for (x, c) in line.iter().enumerate() {
            let lattice = Lattice::new(x as i32, y as i32);
            if *c == '.' {
                maze.push(lattice);
                let mut portal = String::new();
                if lines[y - 1][x].is_alphabetic() {
                    portal.push(lines[y - 2][x]);
                    portal.push(lines[y - 1][x]);
                } else if lines[y + 1][x].is_alphabetic() {
                    portal.push(lines[y + 1][x]);
                    portal.push(lines[y + 2][x]);
                } else if line[x - 1].is_alphabetic() {
                    portal.push(lines[y][x - 2]);
                    portal.push(line[x - 1]);
                } else if line[x + 1].is_alphabetic() {
                    portal.push(line[x + 1]);
                    portal.push(line[x + 2]);
                }
                if !portal.is_empty() {
                    let is_start = portal == START;
                    let is_end = portal == END;
                    let portal_index = get_portal_index(portal);
                    portals.insert(lattice, portal_index);
                    if is_start {
                        start = lattice;
                    } else if is_end {
                        end = lattice;
                    }
                }
            }
        }
    }
    (maze, portals, start, end)
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
