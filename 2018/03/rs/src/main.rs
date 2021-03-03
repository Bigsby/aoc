use itertools::*;
use regex::Regex;
use std::collections::HashMap;
use std::env;
use std::fs;
use std::time::Instant;

type Claim = (u32, u32, u32, u32, u32);

fn get_covered_points(claims: &Vec<Claim>) -> HashMap<(u32, u32), u32> {
    let mut covered_points = HashMap::new();
    for (_, left, top, width, height) in claims {
        for point in iproduct!(*left..*left + *width, *top..*top + *height) {
            if covered_points.contains_key(&point) {
                *covered_points.get_mut(&point).unwrap() += 1;
            } else {
                covered_points.insert(point, 1);
            }
        }
    }
    covered_points
}

fn part2(claims: &Vec<Claim>, covered_points: &HashMap<(u32, u32), u32>) -> u32 {
    for (id, left, top, width, height) in claims {
        if iproduct!(*left..*left + *width, *top..*top + *height)
            .all(|point| *covered_points.get(&point).unwrap() == 1)
        {
            return *id;
        }
    }
    panic!("Claim not found");
}

fn solve(claims: &Vec<Claim>) -> (usize, u32) {
    let covered_points = get_covered_points(claims);

    (
        covered_points.values().filter(|value| **value > 1).count(),
        part2(claims, &covered_points),
    )
}

fn get_input(file_path: &String) -> Vec<Claim> {
    let re = Regex::new(
        r"^#(?P<id>\d+)\s@\s(?P<left>\d+),(?P<top>\d+):\s(?P<width>\d+)x(?P<height>\d+)$",
    )
    .unwrap();
    fs::read_to_string(file_path)
        .expect("Error reading input file!")
        .lines()
        .map(|line| {
            re.captures(line).and_then(|cap| {
                Some((
                    cap.name("id")
                        .map(|c| c.as_str().parse().unwrap())
                        .unwrap(),
                    cap.name("left")
                        .map(|c| c.as_str().parse().unwrap())
                        .unwrap(),
                    cap.name("top")
                        .map(|c| c.as_str().parse().unwrap())
                        .unwrap(),
                    cap.name("width")
                        .map(|c| c.as_str().parse().unwrap())
                        .unwrap(),
                    cap.name("height")
                        .map(|c| c.as_str().parse().unwrap())
                        .unwrap(),
                ))
            })
        })
        .map(|c| c.unwrap())
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
