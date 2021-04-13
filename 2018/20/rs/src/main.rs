use num::Complex;
use std::collections::HashMap;

type Coordinate = Complex<i32>;

fn get_distances(routes: &str) -> Vec<i32> {
    let direction: HashMap<char, Coordinate> = vec![
        ('N', Coordinate::new(0, 1)),
        ('S', Coordinate::new(0, -1)),
        ('E', Coordinate::new(1, 0)),
        ('W', Coordinate::new(-1, 0)),
    ]
    .into_iter()
    .collect();
    let mut distances = HashMap::new();
    distances.insert(Coordinate::new(0, 0), 0);
    let mut group_ends = Vec::new();
    let mut head = Coordinate::new(0, 0);
    for c in routes.chars().skip(1).take(routes.len() - 2) {
        match c {
            '(' => group_ends.push(head),
            ')' => head = group_ends.pop().unwrap(),
            '|' => head = *group_ends.last().unwrap(),
            _ => {
                let previous = head;
                head += direction.get(&c).unwrap();
                let current = *distances.entry(head).or_insert(i32::MAX);
                *distances.get_mut(&head).unwrap() =
                    current.min(distances.get(&previous).unwrap() + 1);
            }
        }
    }
    distances.values().map(|d| *d).collect()
}

fn solve(routes: &str) -> (i32, usize) {
    let distances = get_distances(routes);
    (
        distances.iter().map(|d| *d).max().unwrap(),
        distances
            .iter()
            .filter(|distance| **distance >= 1000)
            .count(),
    )
}

fn get_input(file_path: &String) -> String {
    std::fs::read_to_string(file_path).expect("Error reading input file!")
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
