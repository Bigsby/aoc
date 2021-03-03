use std::env;
use std::fs;
use std::time::Instant;
use num::complex::Complex;
use std::collections::{HashMap, HashSet};

type Direction = Complex<i32>;
type Position = Complex<i32>;

fn process_direction(
    visited_houses: &mut HashSet<Position>,
    position: &mut Position,
    direciton: &Direction,
) {
    *position += direciton;
    visited_houses.insert(*position);
}

fn part1(directions: &Vec<Direction>) -> usize {
    let mut visited_houses = HashSet::new();
    let mut position = Complex::new(0, 0);
    visited_houses.insert(position);
    directions.iter().for_each(|direction| process_direction(&mut visited_houses, &mut position, &direction));
    visited_houses.len()
}

fn part2(directions: &Vec<Direction>) -> usize {
    let mut visited_houses = HashSet::new();
    let mut santa_position = Complex::new(0, 0);
    let mut robot_position = Complex::new(0, 0);
    visited_houses.insert(santa_position);    
    for (index, direction) in directions.iter().enumerate() {
        if index % 2 == 0 {
            process_direction(&mut visited_houses, &mut robot_position, &direction);
        } else {
            process_direction(&mut visited_houses, &mut santa_position, &direction);
        }
    }
    visited_houses.len()
}

fn solve(directions: &Vec<Direction>) -> (usize, usize) {
    (part1(directions), part2(directions))
}

fn get_input(file_path: &String) -> Vec<Direction> {
    let directions: HashMap<_, _> = vec![
        ('^', Complex::new(0, -1)),
        ('v', Complex::new(0, 1)),
        ('>', Complex::new(1, 0)),
        ('<', Complex::new(-1, 0)),
    ]
    .into_iter()
    .collect();
    fs::read_to_string(file_path)
        .expect("Error reading input file!")
        .chars()
        .map(|c| *directions.get(&c).unwrap())
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
    println!("Time: {:7}", now.elapsed().as_secs_f32());
}
