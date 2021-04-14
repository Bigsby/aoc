use regex::Regex;
use std::collections::{HashMap, HashSet};

struct Food {
    ingredients: Vec<String>,
    allergens: Vec<String>,
}

fn get_allergens(foods: &Vec<Food>) -> HashSet<String> {
    let mut allergens = HashSet::new();
    for food in foods {
        for allergen in &food.allergens {
            allergens.insert(String::from(allergen));
        }
    }
    allergens
}

fn build_allergen_graph(foods: &Vec<Food>) -> HashMap<String, HashSet<String>> {
    get_allergens(foods)
        .into_iter()
        .map(|allergen| {
            (
                allergen.clone(),
                foods
                    .iter()
                    .filter(|food| food.allergens.contains(&allergen))
                    .fold(HashSet::new(), |acc, food| {
                        if acc.is_empty() {
                            food.ingredients.iter().map(|i| String::from(i)).collect()
                        } else {
                            acc.intersection(
                                &food
                                    .ingredients
                                    .iter()
                                    .map(|i| String::from(i))
                                    .collect::<HashSet<String>>(),
                            )
                            .map(|i| String::from(i))
                            .collect()
                        }
                    }),
            )
        })
        .collect()
}

fn part1(foods: &Vec<Food>, allergen_graph: &HashMap<String, HashSet<String>>) -> usize {
    let found_ingredients =
        allergen_graph
            .values()
            .fold(HashSet::new(), |acc, ingredients_for_allergen| {
                acc.union(
                    &ingredients_for_allergen
                        .iter()
                        .map(|i| String::from(i))
                        .collect::<HashSet<String>>(),
                )
                .map(|i| String::from(i))
                .collect()
            });
    let mut count = 0;
    for food in foods {
        for ingredient in &food.ingredients {
            if !found_ingredients.contains(ingredient) {
                count += 1;
            }
        }
    }
    count
}

fn part2(allergen_graph: &HashMap<String, HashSet<String>>) -> String {
    let mut allergen_graph = allergen_graph.clone();
    while allergen_graph
        .values()
        .any(|ingredients| ingredients.len() != 1)
    {
        let single_ingredient_allergens: Vec<(String, String)> = allergen_graph
            .iter()
            .filter_map(|(allergen, ingredients)| {
                if ingredients.len() == 1 {
                    Some((
                        String::from(allergen),
                        String::from(ingredients.iter().next().unwrap()),
                    ))
                } else {
                    None
                }
            })
            .collect();
        for (single_allergen, ingredient) in single_ingredient_allergens {
            let other_keys: Vec<String> = allergen_graph
                .keys()
                .filter_map(|allergen| {
                    if *allergen != single_allergen {
                        Some(String::from(allergen))
                    } else {
                        None
                    }
                })
                .collect();
            for allergen in other_keys {
                if *allergen != single_allergen {
                    allergen_graph
                        .get_mut(&allergen)
                        .unwrap()
                        .remove(&ingredient);
                }
            }
        }
    }
    let mut remaining_ingredients: Vec<String> = allergen_graph
        .values()
        .map(|ingredients| String::from(ingredients.iter().next().unwrap()))
        .collect();
    remaining_ingredients.sort_by(|a, b| a.cmp(&b));
    remaining_ingredients.join(",")
}

fn solve(foods: &Vec<Food>) -> (usize, String) {
    let allergen_graph = build_allergen_graph(foods);
    (part1(foods, &allergen_graph), part2(&allergen_graph))
}

fn get_input(file_path: &String) -> Vec<Food> {
    let line_regex =
        Regex::new(r"^(?P<ingredients>[^\(]+)\s\(contains\s(?P<allergens>[^\)]+)\)$").unwrap();
    std::fs::read_to_string(file_path)
        .expect("Error reading input file!")
        .lines()
        .map(|line| {
            line_regex
                .captures(line)
                .map(|cap| Food {
                    ingredients: cap
                        .name("ingredients")
                        .unwrap()
                        .as_str()
                        .split(' ')
                        .map(|i| String::from(i))
                        .collect(),
                    allergens: cap
                        .name("allergens")
                        .unwrap()
                        .as_str()
                        .split(", ")
                        .map(|i| String::from(i))
                        .collect(),
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
