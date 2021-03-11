use std::env;
use std::fs;
use std::time::{Instant};

fn get_count(numbers: &Vec<u32>, index_offset: usize) -> u32 {
    (0..numbers.len()).fold(0, |count, index| 
        if numbers[index] == numbers[(index + index_offset) % numbers.len()] { 
            count + numbers[index] 
        } else { 
            count 
        })
}

fn solve(numbers: &Vec<u32>) -> (u32, u32) {
    (get_count(numbers, numbers.len() - 1), get_count(numbers, numbers.len() / 2))
}

fn get_input(file_path: &String) -> Vec<u32> {
    let contents = fs::read_to_string(file_path).expect("Error reading input file!");
    contents.trim().chars().map(|c| c.to_string().parse::<u32>().unwrap()).collect()
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