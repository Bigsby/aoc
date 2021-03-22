use regex::Regex;
use std::collections::{HashMap, HashSet};

static CENTER_OF_MASS: &str = "COM";

fn part1(planet_orbits: &HashMap<String, String>) -> u32 {
    let mut planets = HashSet::new();
    for (orbiter, orbited) in planet_orbits {
        planets.insert(orbiter);
        planets.insert(orbited);
    }
    let mut orbit_counts: HashMap<String, u32> = HashMap::new();
    orbit_counts.insert(String::from(CENTER_OF_MASS), 0);
    while orbit_counts.len() != planets.len() {
        for planet in &planets {
            if orbit_counts.contains_key(*planet) {
                continue;
            }
            let mut orbits = 0;
            if let Some(orbited_planet) = planet_orbits.get(*planet) {
                if let Some(orbited_orbits) = orbit_counts.get(orbited_planet) {
                    orbits = orbited_orbits + 1;
                }
            } else {
                orbits = 1;
            }
            if orbits > 0 {
                orbit_counts.insert(String::from(*planet), orbits);
            }
        }
    }
    orbit_counts.values().sum()
}

fn get_path_to_center_of_mass(
    planet: &str,
    planet_orbits: &HashMap<String, String>,
) -> Vec<String> {
    let mut route = vec![];
    let mut planet = planet;
    while planet != CENTER_OF_MASS {
        planet = planet_orbits[&String::from(planet)].as_str();
        route.push(String::from(planet));
    }
    route
}

static YOU: &str = "YOU";
static SAN: &str = "SAN";
fn part2(planet_orbits: &HashMap<String, String>) -> usize {
    let mut you_path = get_path_to_center_of_mass(YOU, planet_orbits);
    let mut san_path = get_path_to_center_of_mass(SAN, planet_orbits);
    while you_path.pop() == san_path.pop() {}
    you_path.len() + san_path.len() + 2
}

fn solve(planet_orbits: &HashMap<String, String>) -> (u32, usize) {
    (part1(planet_orbits), part2(planet_orbits))
}

fn get_input(file_path: &String) -> HashMap<String, String> {
    let re = Regex::new(r"^(?P<orbited>[A-Z\d]{3})\)(?P<orbiter>[A-Z\d]{3})$").unwrap();
    std::fs::read_to_string(file_path)
        .expect("Error reading input file!")
        .lines()
        .map(|line| {
            re.captures(line)
                .map(|cap| {
                    (
                        String::from(cap.name("orbiter").unwrap().as_str()),
                        String::from(cap.name("orbited").unwrap().as_str()),
                    )
                })
                .unwrap()
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
