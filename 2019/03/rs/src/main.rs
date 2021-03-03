use std::collections::{HashMap, HashSet};
use std::env;
use std::fs;
use std::iter::IntoIterator;
use std::time::Instant;
use num::complex::Complex;
use regex::Regex;

type Wire = Vec<(char, u32)>;

pub struct WireWalker {
    position: Complex<i32>,
    distance: u32,
    direction: Complex<i32>,
    wire: Box<dyn Iterator<Item = (char, u32)>>,
    directions: HashMap<char, Complex<i32>>,
}

impl WireWalker {
    fn new(wire: &Wire) -> WireWalker {
        WireWalker {
            wire: Box::new(wire.clone().into_iter()),
            position: Complex::new(0, 0),
            distance: 0,
            direction: Complex::new(0, 0),
            directions: vec![
                ('R', Complex::new(1, 0)),
                ('U', Complex::new(0, -1)),
                ('L', Complex::new(-1, 0)),
                ('D', Complex::new(0, 1)),
            ]
            .into_iter()
            .collect(),
        }
    }
}

impl Iterator for WireWalker {
    type Item = Complex<i32>;
    fn next(&mut self) -> std::option::Option<<Self as std::iter::Iterator>::Item> {
        if self.distance == 0 {
            let next = self.wire.as_mut().next();
            match next {
                Some((direction, distance)) => {
                    self.distance = distance;
                    self.direction = self.directions[&direction];
                }
                None => return None,
            }
        }
        if self.distance > 0 {
            self.position += self.direction;
            self.distance -= 1;
            Some(self.position)
        } else {
            None
        }
    }
}

fn part1(wires: &(Wire, Wire)) -> i32 {
    let (wire_a, wire_b) = wires;
    let wire_a_points: HashSet<Complex<i32>> = WireWalker::new(&wire_a).collect();
    let wire_b_points: HashSet<Complex<i32>> = WireWalker::new(&wire_b).collect();
    wire_b_points
        .iter()
        .filter(|point| wire_a_points.contains(&point))
        .map(|point| i32::abs(point.re) + i32::abs(point.im))
        .min()
        .unwrap()
}

fn part2(wires: &(Wire, Wire)) -> usize {
    let (wire_a, wire_b) = wires;
    let mut wire_a_points: HashMap<Complex<i32>, usize> = HashMap::new();
    for (steps, point) in WireWalker::new(&wire_a).enumerate() {
        if !wire_a_points.contains_key(&point) {
            wire_a_points.insert(point, steps + 1);
        }
    }
    WireWalker::new(&wire_b).enumerate().filter(|(_, point)| wire_a_points.contains_key(&point))
        .map(|(steps, point)| wire_a_points.get(&point).unwrap() + steps + 1)
        .min().unwrap()
}

fn solve(wires: &(Wire, Wire)) -> (i32, usize) {
    (part1(wires), part2(wires))
}

fn parse_line(line: &str) -> Wire {
    let re = Regex::new(r"(?P<direction>R|U|L|D)(?P<distance>\d+)").unwrap();
    re.captures_iter(line)
        .map(|cap| {
            (
                cap.name("direction")
                    .map(|direction| direction.as_str().chars().next().unwrap())
                    .unwrap(),
                cap.name("distance")
                    .map(|distance| distance.as_str().parse().unwrap())
                    .unwrap(),
            )
        })
        .collect()
}

fn get_input(file_path: &String) -> (Wire, Wire) {
    let lines: Vec<String> = fs::read_to_string(file_path)
        .expect("Error reading input file!")
        .lines()
        .map(|line| String::from(line))
        .collect();
    (parse_line(&lines[0]), parse_line(&lines[1]))
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
