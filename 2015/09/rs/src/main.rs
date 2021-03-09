use regex::Regex;
use std::collections::HashSet;

struct Edge {
    node_a: String,
    node_b: String,
    distance: u32,
}

fn get_single_nodes(edges: &Vec<Edge>) -> HashSet<String> {
    let mut nodes = HashSet::new();
    for edge in edges.into_iter() {
        nodes.insert(edge.node_a.clone());
        nodes.insert(edge.node_b.clone());
    }
    nodes
}

fn get_best_path(edges: &Vec<Edge>, longest: bool) -> u32 {
    let single_nodes = get_single_nodes(edges);
    let length = single_nodes.len();
    let mut stack: Vec<(Vec<String>, String, u32)> = single_nodes
        .iter()
        .map(|node| (vec![node.clone()], node.clone(), 0))
        .collect();
    let mut best_distance = if longest { 0 } else { u32::MAX };
    while !stack.is_empty() {
        let (path, current, distance) = stack.pop().unwrap();
        for edge in edges
            .iter()
            .filter(|edge| edge.node_a == current || edge.node_b == current)
        {
            let next_node = if current == edge.node_a {
                &edge.node_b
            } else {
                &edge.node_a
            };
            if path.contains(next_node) {
                continue;
            }
            let new_distance = distance + edge.distance;
            if !longest && new_distance > best_distance {
                continue;
            }
            let mut new_path = path.clone();
            new_path.push(next_node.clone());
            if new_path.len() == length {
                best_distance = if longest {
                    best_distance.max(new_distance)
                } else {
                    best_distance.min(new_distance)
                };
            } else {
                stack.push((new_path, next_node.clone(), new_distance));
            }
        }
    }
    best_distance
}

fn solve(edges: &Vec<Edge>) -> (u32, u32) {
    (get_best_path(edges, false), get_best_path(edges, true))
}

fn get_input(file_path: &String) -> Vec<Edge> {
    let re = Regex::new(r"^(.*)\sto\s(.*)\s=\s(\d+)$").unwrap();
    std::fs::read_to_string(file_path)
        .expect("Error reading input file!")
        .lines()
        .map(|line| {
            re.captures(line)
                .map(|cap| Edge {
                    node_a: String::from(cap.get(1).unwrap().as_str()),
                    node_b: String::from(cap.get(2).unwrap().as_str()),
                    distance: cap.get(3).unwrap().as_str().parse().unwrap(),
                })
                .unwrap()
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
    println!("P1: {}", part2_result);
    println!();
    println!("Time: {:.7}", end);
}
