use json::{parse, JsonValue, Result};
use regex::Regex;

fn get_total(obj: Result<JsonValue>) -> i32 {
    match obj {
        Ok(JsonValue::Number(value)) => value.as_fixed_point_i64(0).unwrap() as i32,
        Ok(JsonValue::Array(values)) => values
            .iter()
            .fold(0, |acc, value| acc + get_total(Ok(value.clone()))),
        Ok(JsonValue::Object(inner_obj)) => {
            if inner_obj
                .iter()
                .any(|(_, v)| json::JsonValue::from("red") == *v)
            {
                0
            } else {
                inner_obj
                    .iter()
                    .map(|(_, v)| v)
                    .fold(0, |acc, value| acc + get_total(Ok(value.clone())))
            }
        }
        _ => 0,
    }
}

fn solve(puzzle_input: &str) -> (i32, i32) {
    let number_regex = Regex::new(r"(-?[\d]+)").unwrap();
    (
        number_regex
            .captures_iter(puzzle_input)
            .fold(0, |acc, cap| {
                acc + cap.get(0).unwrap().as_str().parse::<i32>().unwrap()
            }),
        get_total(parse(puzzle_input)),
    )
}

fn get_input(file_path: &String) -> String {
    String::from(std::fs::read_to_string(file_path).expect("Error reading input file!"))
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
