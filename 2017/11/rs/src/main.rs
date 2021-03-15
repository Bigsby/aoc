use num::complex::Complex;
use std::collections::HashMap;

fn get_hex_manhatan_distance(position: Complex<i32>) -> i32 {
    if (position.re > 0) ^ (position.im > 0) {
        i32::abs(position.re).max(i32::abs(position.im))
    } else {
        i32::abs(position.re) + i32::abs(position.im)
    }
}

fn solve(instructions: &Vec<String>) -> (i32, i32) {
    let mut furthest = 0;
    let mut current_hex = Complex::new(0, 0);
    let directions: HashMap<String, Complex<i32>> = vec![
        (String::from("s"), Complex::new(0, 1)),
        (String::from("se"), Complex::new(1, 0)),
        (String::from("sw"), Complex::new(-1, 1)),
        (String::from("ne"), Complex::new(1, -1)),
        (String::from("nw"), Complex::new(-1, 0)),
        (String::from("n"), Complex::new(0, -1)),
    ]
    .into_iter()
    .collect();
    for instruction in instructions {
        current_hex += directions[instruction];
        furthest = furthest.max(get_hex_manhatan_distance(current_hex));
    }
    (get_hex_manhatan_distance(current_hex), furthest)
}

fn get_input(file_path: &String) -> Vec<String> {
    std::fs::read_to_string(file_path)
        .expect("Error reading input file!")
        .split(",")
        .map(|i| String::from(i))
        .collect()
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
