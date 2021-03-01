use std::env;
use std::fs;
use std::time::{Instant};

macro_rules! mass_fuel {
    ($mass:expr) => {
        $mass / 3 - 2
    };
}

fn get_fuel(mass: &i32) -> i32 {
    let mut total = 0;
    let mut current_mass = *mass;
    loop {
        let fuel: i32 = mass_fuel!(current_mass as i32);
        if fuel <= 0 {
            return total
        }
        total += fuel;
        current_mass = fuel;
    }
}

fn solve(masses: &Vec<i32>) -> (i32, i32) {
    (
        masses.iter().map(|mass| mass_fuel!(mass)).sum(), 
        masses.iter().map(get_fuel).sum()
    )
}

fn get_input(file_path: &String) -> Vec<i32> {
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