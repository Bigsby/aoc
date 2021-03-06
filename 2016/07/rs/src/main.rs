use fancy_regex::Regex;
use std::collections::HashSet;

fn supports_tls(ip: &Vec<String>) -> bool {
    let abba_regex = Regex::new(r"([a-z])((?!\1)[a-z])\2\1").unwrap();
    !(1..ip.len())
        .step_by(2)
        .into_iter()
        .any(|index| abba_regex.is_match(&ip[index]).unwrap())
        && (0..ip.len())
            .step_by(2)
            .into_iter()
            .any(|index| abba_regex.is_match(&ip[index]).unwrap())
}

fn find_babs(supernet: &str) -> HashSet<String> {
    (0..supernet.len() - 2)
        .into_iter()
        .filter(|index| supernet.chars().nth(*index) == supernet.chars().nth(*index + 2))
        .map(|index| {
            [
                supernet.chars().nth(index + 1).unwrap(),
                supernet.chars().nth(index).unwrap(),
                supernet.chars().nth(index + 1).unwrap(),
            ]
            .iter()
            .collect()
        })
        .collect()
}

fn supports_ssl(ip: &Vec<String>) -> bool {
    let babs: HashSet<String> = (0..ip.len())
        .step_by(2)
        .into_iter()
        .fold(HashSet::new(), |acc, index| {
            acc.union(&find_babs(&ip[index])).map(|bab| bab.clone()).collect()
        });
    for bab in babs {
        for index in (1..ip.len()).step_by(2) {
            if ip.iter().nth(index).unwrap().contains(&bab) {
                return true;
            }
        }
    }
    false
}

fn solve(ips: &Vec<Vec<String>>) -> (usize, usize) {
    (
        ips.iter().filter(|ip| supports_tls(ip)).count(),
        ips.iter().filter(|ip| supports_ssl(ip)).count(),
    )
}

fn get_input(file_path: &String) -> Vec<Vec<String>> {
    let line_regex = Regex::new(r"(\[?[a-z]+\]?)").unwrap();
    std::fs::read_to_string(file_path)
        .expect("Error reading input file!")
        .lines()
        .map(|line| {
            line_regex
                .find_iter(line)
                .map(|f| String::from(f.unwrap().as_str()))
                .collect()
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
