use num::complex::Complex;
use std::collections::{HashSet, VecDeque};

fn is_position_valid(position: Complex<i32>, number: i32) -> bool {
    let (x, y) = (position.re, position.im);
    !(x < 0 || y < 0) && (x * x + 3 * x + 2 * x * y + y + y * y + number).count_ones() % 2 == 0
}

fn solve(number: &i32) -> (usize, usize) {
    let directions = vec![
        Complex::new(-1, 0),
        Complex::new(0, 1),
        Complex::new(0, -1),
        Complex::new(1, 0),
    ];
    let mut part1_result = 0;
    let start_position = Complex::new(1, 1);
    let mut queue = VecDeque::new();
    queue.push_back((start_position, vec![start_position]));
    let mut all_visited = HashSet::new();
    all_visited.insert(start_position);
    let target = Complex::new(31, 39);
    while !queue.is_empty() && part1_result == 0 {
        let (position, visited) = queue.pop_front().unwrap();
        for direction in &directions {
            let new_position = position + direction;
            if new_position == target {
                part1_result = visited.len();
            }
            if !visited.contains(&new_position) && is_position_valid(new_position, *number) {
                if visited.len() <= 50 {
                    all_visited.insert(new_position);
                }
                let mut new_visited = visited.clone();
                new_visited.push(new_position);
                queue.push_back((new_position, new_visited));
            }
        }
    }
    (part1_result, all_visited.len())
}

fn get_input(file_path: &String) -> i32 {
    std::fs::read_to_string(file_path)
        .expect("Error reading input file!")
        .trim()
        .parse()
        .unwrap()
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
