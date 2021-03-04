use std::env;
use std::fs;
use std::time::Instant;
use regex::Regex;
use std::collections::HashMap;

type Passport = HashMap<String, String>;

fn validate_int(value: &str, min: u32, max: u32) -> bool {
    match value.parse::<u32>() {
        Ok(parsed) => parsed >= min && parsed <= max,
        _ => false,
    }
}

fn validate_hgt(value: &str) -> bool {
    let hgt_regex = Regex::new(r"^(\d{2,3})(cm|in)$").unwrap();
    if let Some(cap) = hgt_regex.captures(value) {
        let height: u32 = cap.get(1).unwrap().as_str().parse().unwrap();
        return match cap.get(2).unwrap().as_str() {
            "cm" => height >= 150 && height <= 193,
            "in" => height >= 59 && height <= 76,
            _ => panic!("uknown height unit '{}'", cap.get(1).unwrap().as_str()),
        };
    }
    false
}

fn solve(passports: &Vec<Passport>) -> (usize, usize) {
    let mandatory_fields = vec!["byr", "iyr", "eyr", "hgt", "hcl", "ecl", "pid"];
    let hcl_regex = Regex::new(r"^#[0-9a-f]{6}$").unwrap();
    let pid_regex = Regex::new(r"^[\d]{9}$").unwrap();
    let ecls = vec!["amb", "blu", "brn", "gry", "grn", "hzl", "oth"];
    (
        passports
            .iter()
            .filter(|passport| {
                mandatory_fields
                    .iter()
                    .all(|field| passport.contains_key(*field))
            })
            .count(),
        passports
            .iter()
            .filter(|passport| {
                mandatory_fields.iter().all(|field| {
                    passport.contains_key(*field)
                        && match *field {
                            "byr" => validate_int(passport.get(*field).unwrap(), 1920, 2020),
                            "iyr" => validate_int(passport.get(*field).unwrap(), 2010, 2020),
                            "eyr" => validate_int(passport.get(*field).unwrap(), 2020, 2030),
                            "hgt" => validate_hgt(passport.get(*field).unwrap()),
                            "hcl" => hcl_regex.is_match(passport.get(*field).unwrap()),
                            "ecl" => ecls.contains(&passport.get(*field).unwrap().as_str()),
                            "pid" => pid_regex.is_match(passport.get(*field).unwrap()),
                            _ => {
                                panic!("No validation for field '{}'", field);
                            }
                        }
                })
            })
            .count(),
    )
}

fn get_input(file_path: &String) -> Vec<Passport> {
    let entry_regex = Regex::new(r"([a-z]{3}):([^\s]+)").unwrap();
    fs::read_to_string(file_path)
        .expect("Error reading input file!")
        .split("\n\n")
        .map(|line| {
            entry_regex
                .captures_iter(line)
                .map(|cap| {
                    (
                        String::from(cap.get(1).unwrap().as_str()),
                        String::from(cap.get(2).unwrap().as_str()),
                    )
                })
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
