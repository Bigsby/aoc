use regex::RegexBuilder;
use std::collections::HashMap;

type Next = (bool, i32, i32);
type States = HashMap<i32, (Next, Next)>;

fn solve(data: &(i32, i32, States)) -> (usize, String) {
    let (mut state, steps, states) = data;
    let mut cursor = 0;
    let mut tape: HashMap<i32, bool> = HashMap::new();
    for _ in 0..*steps {
        let (value, direction, new_state) = if *tape.entry(cursor).or_insert(false) {
            states[&state].1
        } else {
            states[&state].0
        };
        *tape.entry(cursor).or_insert(false) = value;
        state = new_state;
        cursor += direction;
    }
    (tape.values().filter(|v| **v).count(), String::default())
}

fn get_input(file_path: &String) -> (i32, i32, States) {
    let setup_regex = RegexBuilder::new(r"^Begin in state (?P<state>\w).*\s+^[^\d]*(?P<steps>\d+)")
        .multi_line(true)
        .build()
        .unwrap();
    let state_regex = RegexBuilder::new(r"^In state (?P<state>\w):\n.*If.*\n[^\d]*(?P<fValue>\d).\n.*(?P<fSlot>right|left).\n.*state (?P<fState>\w).\n.*If.*\n[^\d]*(?P<tValue>\d).\n.*(?P<tSlot>right|left).\n.*state (?P<tState>\w)")
    .multi_line(true)
    .build()
    .unwrap();
    let mut states = States::new();
    let mut initial_state = 0;
    let mut steps = 0;
    for split in std::fs::read_to_string(file_path)
        .expect("Error reading input file!")
        .split("\n\n")
    {
        if let Some(setup_match) = setup_regex.captures(split) {
            initial_state = setup_match
                .name("state")
                .unwrap()
                .as_str()
                .chars()
                .next()
                .unwrap() as i32;
            steps = setup_match.name("steps").unwrap().as_str().parse().unwrap();
        }
        if let Some(state_match) = state_regex.captures(split) {
            states.insert(
                state_match
                    .name("state")
                    .unwrap()
                    .as_str()
                    .chars()
                    .next()
                    .unwrap() as i32,
                (
                    (
                        state_match
                            .name("fValue")
                            .unwrap()
                            .as_str()
                            .parse::<i32>()
                            .unwrap()
                            == 1,
                        if state_match.name("fSlot").unwrap().as_str() == "right" {
                            1
                        } else {
                            -1
                        },
                        state_match
                            .name("fState")
                            .unwrap()
                            .as_str()
                            .chars()
                            .next()
                            .unwrap() as i32,
                    ),
                    (
                        state_match
                            .name("tValue")
                            .unwrap()
                            .as_str()
                            .parse::<i32>()
                            .unwrap()
                            == 1,
                        if state_match.name("tSlot").unwrap().as_str() == "right" {
                            1
                        } else {
                            -1
                        },
                        state_match
                            .name("tState")
                            .unwrap()
                            .as_str()
                            .chars()
                            .next()
                            .unwrap() as i32,
                    ),
                ),
            );
        }
    }
    (initial_state, steps, states)
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
    println!("P2: {}", part2_result);
    println!();
    println!("Time: {:.7}", end);
}
