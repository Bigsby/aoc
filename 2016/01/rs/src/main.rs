use std::env;
use std::fs;
use std::time::{Instant};
use regex::Regex;
use num::complex::Complex;

#[derive(Debug)]
struct Instruction {
    direction: char,
    distance: u32,
}

fn get_manhatan_distance(position: &Complex<i32>) -> i32 {
    i32::abs(position.re) + i32::abs(position.im)
}

fn get_new_heading(current_heading: Complex<i32>, direction: char) -> Complex<i32> {
    match direction {
        'L' => current_heading * Complex::new(0, 1),
        'R' => current_heading * Complex::new(0, -1),
        _ => panic!("Unknow direction")
    }
}

fn solve(instructions: &Vec<Instruction>) -> (i32,i32) {
    let mut position = Complex::new(0, 0);
    let mut heading = Complex::new(0, 1);
    let mut first_repeated = 0;
    let mut visited_positions = Vec::new();
    for instruction in instructions {
        heading = get_new_heading(heading, instruction.direction);
        for _ in 0..instruction.distance {
            position += heading;
            if first_repeated == 0 {
                if visited_positions.contains(&position) {
                    first_repeated = get_manhatan_distance(&position);
                } else {
                    visited_positions.push(position);
                }
            }
        }
    }
    (get_manhatan_distance(&position), first_repeated)
}

fn get_input(file_path: &String) -> Vec<Instruction> {
    let re = Regex::new(r"(?P<direction>[RL])(?P<distance>\d+),?\s?").unwrap();
    fs::read_to_string(file_path).expect("Error reading input file").split(" ")
        .map(|split| re.captures(split)
            .and_then(|cap| Some(
                    (
                        cap.name("direction").map(|c| c.as_str().chars().next().unwrap()).unwrap(), 
                        cap.name("distance").map(|c| c.as_str()).unwrap()
                    )
                )
            )
        ).map(|caps|
            match caps {
                Some((direction, distance)) => Instruction{
                    direction, 
                    distance: distance.parse().expect("Unable to parse distance")
                },
                _ => panic!("Unable to parse instructions")
            }
        ).collect()
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