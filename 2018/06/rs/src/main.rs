use num::complex::Complex;
use std::collections::{HashMap,HashSet};

type Location = Complex<i32>;

fn get_manhatan_distance(location_a: &Location, location_b: &Location) -> i32 {
    i32::abs(location_a.re - location_b.re) + i32::abs(location_a.im - location_b.im)
}

fn get_map_edges(locations: &Vec<Location>) -> (i32, i32, i32, i32) {
    (
        locations.iter().map(|l| l.re).min().unwrap(),
        locations.iter().map(|l| l.re).max().unwrap(),
        locations.iter().map(|l| l.im).min().unwrap(),
        locations.iter().map(|l| l.im).max().unwrap(),
    )
}

fn find_closest_location(map_location: &Location, locations: &Vec<Location>) -> usize {
    let mut closest = 0;
    let mut closest_distance = i32::MAX;
    for (index, location) in locations.iter().enumerate() {
        let distance = get_manhatan_distance(&map_location, location);
        if distance < closest_distance {
            closest = index;
            closest_distance = distance;
        }
    }
    closest
}

fn part1(locations: &Vec<Location>) -> usize {
    let (start_x, end_x, start_y, end_y) = get_map_edges(locations);
    let mut map_locations = HashMap::new();
    let mut location_counts: Vec<usize> = (0..locations.len()).map(|_| 0).collect();
    for map_location_x in start_x..(end_x + 1) {
        for map_location_y in start_y..(end_y + 1) {
            let map_location = Complex::new(map_location_x, map_location_y);
            let closest = find_closest_location(&map_location, locations);
            *map_locations.entry(map_location).or_insert(0) = closest;
            location_counts[closest] += 1;
        }
    }
    let mut edge_locations = HashSet::new();
    for y in start_y..end_y {
        edge_locations.insert(map_locations[&Complex::new(start_x, y)]);
        edge_locations.insert(map_locations[&Complex::new(end_x, y)]);
    }
    for x in start_x..end_x {
        edge_locations.insert(map_locations[&Complex::new(x, start_y)]);
        edge_locations.insert(map_locations[&Complex::new(x, end_y)]);
    }
    *location_counts
        .iter()
        .enumerate()
        .filter(|(index, _)| !edge_locations.contains(&index))
        .map(|pair| pair.1)
        .max()
        .unwrap()
}

const MAX_DISTANCE: i32 = 10000;
fn part2(locations: &Vec<Location>) -> usize {
    let (start_x, end_x, start_y, end_y) = get_map_edges(locations);
    let mut valid_locations_count = 0;
    for map_location_x in start_x..(end_x + 1) {
        for map_location_y in start_y..(end_y + 1) {
            let map_location = Complex::new(map_location_x, map_location_y);
            let total_distances: i32 = locations
                .iter()
                .map(|location| get_manhatan_distance(&map_location, location))
                .sum();
            if total_distances < MAX_DISTANCE {
                valid_locations_count += 1;
            }
        }
    }
    valid_locations_count
}

fn solve(locations: &Vec<Location>) -> (usize, usize) {
    (part1(locations), part2(locations))
}

fn get_input(file_path: &String) -> Vec<Location> {
    std::fs::read_to_string(file_path)
        .expect("Error reading input file!")
        .lines()
        .map(|line| {
            let mut split = line.split(',');
            Complex::new(
                split.next().unwrap().trim().parse().unwrap(),
                split.next().unwrap().trim().parse().unwrap(),
            )
        })
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
    println!("P1: {}", part2_result);
    println!();
    println!("Time: {:7}", end);
}
