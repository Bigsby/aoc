use std::env;
use std::fs;
use std::time::{Instant};

fn part1(numbers: &Vec<u32>) -> u32 {
    let list_length = numbers.len();
    (0..list_length).fold(0, |count, index| 
        if numbers[index] == numbers[(index + list_length - 1) % list_length] { 
            count + numbers[index] 
        } else { 
            count 
        })
}

fn part2(numbers: &Vec<u32>) -> u32 {
    let list_length = numbers.len();
    let half_length = list_length / 2;
    (0..list_length).fold(0, |count, index| 
        if numbers[index] == numbers[(index + half_length) % list_length] {
            count + numbers[index]
        } else {
            count
        })
}

fn solve(numbers: &Vec<u32>) -> (u32, u32) {
    (part1(numbers), part2(numbers))
}

fn get_input(file_path: &String) -> Vec<u32> {
    let contents = fs::read_to_string(file_path).expect("Error reading input file!");
    contents.trim().chars().map(|c| c.to_string().parse::<u32>().unwrap()).collect()
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