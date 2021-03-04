use regex::Regex;
use std::collections::HashMap;
use std::env;
use std::fs;
use std::time::Instant;

type Room = (String, u32, String);

fn is_room_valid(name: &str, checksum: &str) -> bool {
    let name = name.replace("-", "");
    let counts: HashMap<char, usize> = name.chars().map(|c| (c, name.matches(c).count())).collect();
    let mut counts: Vec<(&char, &usize)> = counts.iter().collect::<Vec<(&char, &usize)>>();
    counts.sort_by(|a, b| b.0.cmp(&a.0));
    counts.sort_by(|a, b| a.1.cmp(&b.1));
    counts.reverse();
    return checksum == counts.iter().map(|(c, _)| *c).take(5).collect::<String>();
}

const A_ORD: u8 = 97;
const Z_ORD: u8 = 122;
const DASH_ORD: u8 = 45;
const SPACE_ORD: u8 = 32;
fn get_next_char(c: u8) -> u8 {
    match c {
        DASH_ORD | SPACE_ORD => SPACE_ORD,
        Z_ORD => A_ORD,
        _ => c + 1,
    }
}

fn rotate_name(name: &str, count: u32) -> String {
    let mut name_ints = name.chars().map(|c| c as u8).collect::<Vec<u8>>();
    for _ in 0..count {
        for index in 0..name_ints.len() {
            name_ints[index] = get_next_char(name_ints[index]);
        }
    }
    name_ints.iter().map(|c| *c as char).collect::<String>()
}

const SEARCH_NAME: &str = "northpole object storage";
fn solve(rooms: &Vec<Room>) -> (u32, u32) {
    (
        rooms
            .iter()
            .filter(|(name, _, checksum)| is_room_valid(name, checksum))
            .map(|room| room.1)
            .sum(),
        rooms
            .iter()
            .filter(|(name, id, checksum)| {
                is_room_valid(name, checksum) && rotate_name(name, *id) == SEARCH_NAME
            })
            .next()
            .expect("Room not found")
            .1,
    )
}

fn get_input(file_path: &String) -> Vec<Room> {
    let re = Regex::new(r"^(?P<name>[a-z\-]+)-(?P<id>\d+)\[(?P<checksum>\w+)\]$").unwrap();
    fs::read_to_string(file_path)
        .expect("Error reading input file!")
        .lines()
        .map(|line| {
            re.captures(line)
                .map(|cap| {
                    (
                        String::from(cap.name("name").map(|c| c.as_str()).unwrap()),
                        cap.name("id").map(|c| c.as_str().parse().unwrap()).unwrap(),
                        String::from(cap.name("checksum").map(|c| c.as_str()).unwrap()),
                    )
                })
                .unwrap()
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
