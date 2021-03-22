use itertools::Itertools;
use regex::Regex;
use std::collections::HashMap;

struct Entry {
    name: i32,
    capacity: i32,
    durability: i32,
    flavor: i32,
    texture: i32,
    calories: i32,
}

impl Entry {
    fn get_value_for_property(&self, property: &str) -> i32 {
        match property {
            "capacity" => self.capacity,
            "durability" => self.durability,
            "flavor" => self.flavor,
            "texture" => self.texture,
            "calories" => self.calories,
            _ => {
                panic!("Unknow property '{}'", property)
            }
        }
    }
}

fn get_value_for_property(
    solution: &HashMap<i32, i32>,
    entries: &Vec<Entry>,
    property: &str,
) -> i32 {
    entries.into_iter().fold(0, |acc, entry| {
        acc + entry.get_value_for_property(property) * solution.get(&entry.name).unwrap()
    })
}

fn find_value_for_solution(solution: &HashMap<i32, i32>, entries: &Vec<Entry>) -> (i32, i32) {
    (
        vec!["capacity", "durability", "flavor", "texture"]
            .into_iter()
            .map(|property| get_value_for_property(solution, entries, property))
            .into_iter()
            .filter(|value| *value > 0)
            .fold(1, |acc, value| acc * value),
        get_value_for_property(solution, entries, "calories"),
    )
}

fn get_possible_combinations(ingredients: &Vec<i32>, total_spoons: usize) -> Vec<Vec<i32>> {
    ingredients
        .into_iter()
        .combinations_with_replacement(total_spoons)
        .map(|combination| combination.into_iter().map(|i| *i).collect())
        .collect()
}

fn create_solution_from_combination(
    combination: &Vec<i32>,
    ingredients: &Vec<i32>,
) -> HashMap<i32, i32> {
    ingredients
        .into_iter()
        .map(|ingredient| {
            (
                ingredient.clone(),
                combination.iter().filter(|i| *i == ingredient).count() as i32,
            )
        })
        .collect()
}

fn solve(entries: &Vec<Entry>) -> (i32, i32) {
    let ingredients: Vec<i32> = entries.into_iter().map(|entry| entry.name).collect();
    let possible_combinations = get_possible_combinations(&ingredients, 100);
    let mut part1 = 0;
    let mut part2 = 0;
    for combination in possible_combinations {
        let solution = create_solution_from_combination(&combination, &ingredients);
        let (solution_result, calories) = find_value_for_solution(&solution, entries);
        part1 = part1.max(solution_result);
        if calories == 500 {
            part2 = part2.max(solution_result);
        }
    }
    (part1, part2)
}

fn get_input(file_path: &String) -> Vec<Entry> {
    let line_regex = Regex::new(
    r"^(\w+):\scapacity\s(-?\d+),\sdurability\s(-?\d+),\sflavor\s(-?\d+),\stexture\s(-?\d+),\scalories\s(-?\d+)$").unwrap();
    std::fs::read_to_string(file_path)
        .expect("Error reading input file!")
        .lines()
        .enumerate()
        .map(|(index, line)| {
            line_regex
                .captures(line)
                .map(|cap| Entry {
                    name: index as i32,
                    capacity: cap.get(2).unwrap().as_str().parse().unwrap(),
                    durability: cap.get(3).unwrap().as_str().parse().unwrap(),
                    flavor: cap.get(4).unwrap().as_str().parse().unwrap(),
                    texture: cap.get(5).unwrap().as_str().parse().unwrap(),
                    calories: cap.get(6).unwrap().as_str().parse().unwrap(),
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
    println!("P2: {}", part2_result);
    println!();
    println!("Time: {:.7}", end);
}
