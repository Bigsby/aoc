use regex::Regex;
use std::collections::{HashMap, HashSet, VecDeque};

fn get_program_group(program: u32, connections: &HashMap<u32, Vec<u32>>) -> HashSet<u32> {
    let mut queue = VecDeque::new();
    let mut result = HashSet::new();
    queue.push_back(program);
    result.insert(program);
    while let Some(program) = queue.pop_front() {
        for connection in connections.get(&program).unwrap() {
            if result.insert(*connection) {
                queue.push_back(*connection);
            }
        }
    }
    result
}

fn solve(connections: &HashMap<u32, Vec<u32>>) -> (usize, usize) {
    let part1_result = get_program_group(0, &connections).len();
    let mut connections: HashMap<u32, Vec<u32>> = connections
        .into_iter()
        .map(|(k, v)| (*k, v.into_iter().map(|c| *c).collect()))
        .collect();
    let mut groups_count = 0;
    while !connections.is_empty() {
        groups_count += 1;
        for connection in get_program_group(*connections.keys().next().unwrap(), &connections) {
            connections.remove_entry(&connection);
        }
    }
    (part1_result, groups_count)
}

fn get_input(file_path: &String) -> HashMap<u32, Vec<u32>> {
    let line_regex = Regex::new(r"^(?P<one>\d+)\s<->\s(?P<two>.*)$").unwrap();
    std::fs::read_to_string(file_path)
        .expect("Error reading input file!")
        .lines()
        .map(|line| {
            if let Some(cap) = line_regex.captures(line) {
                (
                    cap.name("one").unwrap().as_str().parse::<u32>().unwrap(),
                    cap.name("two")
                        .unwrap()
                        .as_str()
                        .split(",")
                        .map(|split| split.trim().parse::<u32>().unwrap())
                        .collect(),
                )
            } else {
                panic!("Bad format '{}'", line)
            }
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
