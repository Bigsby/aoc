use std::env;
use std::fs;
use std::time::{Instant};
use regex::Regex;
use itertools::Itertools;

fn solve(lines: &Vec<Vec<u32>>) -> (u32, u32) {
    let mut total1 = 0;
    let mut total2 = 0;
    for line in lines {
        total1 += line.iter().max().unwrap() - line.iter().min().unwrap();
        for numbers in line.iter().permutations(2) {
            let number_a = numbers[0];
            let number_b = numbers[1];
            if number_a > number_b && number_a % number_b == 0 {
                total2 += number_a / number_b;
            }
        }
    }
    (total1, total2)
}

fn get_input(file_path: &String) -> Vec<Vec<u32>> {
    let re = Regex::new(r"\d+").unwrap();
    fs::read_to_string(file_path)
        .expect("Error reading input file!")
        .lines()
        .map(|line| re.captures_iter(line).map(|m| m.get(0).unwrap().as_str().parse::<u32>().unwrap()).collect())
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