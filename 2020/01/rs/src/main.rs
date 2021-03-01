use std::env;
use std::fs;
use std::time::{Instant};
use itertools::Itertools;

fn get_combination(numbers: &Vec<u32>, length: usize) -> u32 {
    for combination in numbers.iter().combinations(length) {
        if combination.iter().map(|number| *number).sum::<u32>() == 2020 {
            return combination.iter().fold(1, |acc, &number| acc * (*number));
        }
    };
    panic!("Numbers not found");
}

fn solve(numbers: &Vec<u32>) -> (u32, u32) {
    (
        get_combination(numbers, 2), 
        get_combination(numbers, 3)
    )
}

fn get_input(file_path: &String) -> Vec<u32> {
    fs::read_to_string(file_path)
        .expect("Error reading input file!")
        .split("\n").filter(|&line| !line.is_empty())
        .map(|line| line.parse().expect(&format!("Unable to parse '{}'", line)))
        .collect()
}

fn main() {
    let args: Vec<String> = env::args().collect();
    if args.len() != 2 {
        panic!("Please, add input file path as parameter");
    }
    let now = Instant::now();
    let (part1_result, part2_result) = solve(&get_input(&args[1]));
    println!("P1: {}", part1_result);
    println!("P1: {}", part2_result);
    println!();
    println!("Time: {:?}", now.elapsed().as_secs_f32());
}