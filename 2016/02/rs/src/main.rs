use std::env;
use std::fs;
use std::time::{Instant};
use std::collections::HashMap;
use num::complex::Complex;

type Position = Complex<i32>;
type Keypad = HashMap<Position, char>;
type Directions = HashMap<char, Position>;
macro_rules! dictionary { ($vec: expr) => { $vec.into_iter().collect() } }
macro_rules! c { ($x:expr, $y:expr) => { Complex::new($x, $y) } }

fn get_button_for_path(position: &mut Position, path: &str, directions: &Directions,keypad: &Keypad) -> char {
    *position = path.chars().fold(*position, |current, move_| {
        let new_position = current + directions.get(&move_).unwrap();
        if keypad.contains_key(&new_position) {
            new_position
        } else {
            current
        }
    });
    *keypad.get(&position).unwrap()
}

fn get_code(paths: &Vec<String>, directions: &Directions, keypad: &Keypad) -> String {
    let mut position = c!(0, 0);
    paths.iter().map(|path| get_button_for_path(&mut position, path, directions, keypad)).into_iter().collect()
}

fn solve(paths: &Vec<String>) -> (String,String) {
    let directions = dictionary!(vec![
            ('U', c!( 0, -1)),
            ('D', c!( 0,  1)),
            ('L', c!(-1,  0)),
            ('R', c!( 1,  0)),
    ]);
    (
        get_code(&paths, &directions, &dictionary!(vec![
            (c!(-1, -1), '1'), (c!(0, -1), '2'), (c!(1, -1), '3'),
            (c!(-1,  0), '4'), (c!(0,  0), '5'), (c!(1,  0), '6'),
            (c!(-1,  1), '7'), (c!(0,  1), '8'), (c!(1,  1), '9'),
        ])), 
        get_code(&paths, &directions, &dictionary!(vec![
                                                  (c!(0, -2), '1'),
                               (c!(-1, -1), '2'), (c!(0, -1), '3'), (c!(1, -1), '4'),
            (c!(-2,  0), '5'), (c!(-1,  0), '6'), (c!(0,  0), '7'), (c!(1,  0), '8'), (c!(2, 0), '9'),
                               (c!(-1,  1), 'A'), (c!(0,  1), 'B'), (c!(1,  1), 'C'),
                                                  (c!(0,  2), 'D'),
        ]))
    )
}

fn get_input(file_path: &String) -> Vec<String> {
    fs::read_to_string(file_path)
        .expect("Error reading input file!")
        .lines()
        .map(|line| String::from(line))
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