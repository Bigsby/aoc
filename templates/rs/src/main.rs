use std::env;
use std::fs;
use std::time::{Instant};

fn part1(puzzle_input: &str) -> usize {

}

fn part2(puzzle_input: &str) -> usize {

}

fn solve(puzzle_input: &str) -> (i32,usize) {
    (part1(puzzle_input), part2(puzzle_input))
}

fn get_input(file_path: &String) -> &str {
    fs::read_to_string(file_path).expect("Error reading input file!").trim()
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