use regex::Regex;
use std::env;
use std::fs;
use std::time::Instant;

fn is_triange_possible(side_a: &u32, side_b: &u32, side_c: &u32) -> bool {
    *side_a < (side_b + side_c) && *side_b < (side_a + side_c) && *side_c < (side_a + side_b)
}

fn solve(triangle_sides: &Vec<Vec<u32>>) -> (usize, usize) {
    (
        triangle_sides
            .iter()
            .filter(|sides| is_triange_possible(&sides[0], &sides[1], &sides[2]))
            .count(),
        (0..triangle_sides.len())
            .filter(|index| {
                is_triange_possible(
                    &triangle_sides[(index / 3) * 3][index % 3],
                    &triangle_sides[(index / 3) * 3 + 1][index % 3],
                    &triangle_sides[(index / 3) * 3 + 2][index % 3],
                )
            })
            .count(),
    )
}

fn get_input(file_path: &String) -> Vec<Vec<u32>> {
    let re = Regex::new(r"\d+").unwrap();
    fs::read_to_string(file_path)
        .expect("Error reading input file!")
        .lines()
        .map(|line| {
            re.captures_iter(line)
                .map(|cap| Some(cap.get(0).unwrap().as_str().parse::<u32>().unwrap()))
                .map(|i: Option<u32>| i.unwrap())
                .collect()
        })
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
