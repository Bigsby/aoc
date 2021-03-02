use std::env;
use std::fs;
use std::time::{Instant};
use regex::Regex;

fn part1(dimensions: &Vec<(u32, u32, u32)>) -> u32 {
    let mut total_paper = 0;
    for (w, l, h) in dimensions {
        let wl = w * l;
        let wh = w * h;
        let hl = h * l;
        let smallest = [&wl, &wh, &hl].iter().map(|x| *x).min().unwrap();
        total_paper += 2 * (wl + wh + hl) + smallest;
    }
    total_paper
}

fn part2(dimensions: &Vec<(u32, u32, u32)>) -> u32 {
    let mut total_ribbon = 0;
    for (w, l, h) in dimensions {
        let mut sides = [&w, &l, &h];
        sides.sort();
        total_ribbon += 2 * (*sides[0] + *sides[1]) + w * l * h;
    }
    total_ribbon
}

fn solve(dimensions: &Vec<(u32, u32, u32)>) -> (u32, u32) {
    (part1(dimensions), part2(dimensions))
}

fn get_input(file_path: &String) -> Vec<(u32, u32, u32)> {
    let re = Regex::new(r"^(\d+)x(\d+)x(\d+)$").unwrap();
    let processor = |c: &regex::Captures, index| c.get(index).unwrap().as_str().parse::<u32>().unwrap();
    fs::read_to_string(file_path)
        .expect("Error reading input file!")
        .lines()
        .map(|line| re.captures(line)
            .map(|c| (processor(&c, 1), processor(&c, 2), processor(&c, 3))).unwrap())
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