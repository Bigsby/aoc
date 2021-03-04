use std::env;
use std::fs;
use std::time::Instant;

fn is_anagram(word1: &str, word2: &str) -> bool {
    word1.len() == word2.len()
        && word1
            .chars()
            .all(|c| word1.matches(c).count() == word2.matches(c).count())
}

fn has_no_anagram(passphrase: &Vec<String>) -> bool {
    !(0..passphrase.len()).any(|index| {
        (0..passphrase.len()).any(|other_index| {
            index != other_index && is_anagram(&passphrase[index], &passphrase[other_index])
        })
    })
}

fn solve(passphrases: &Vec<Vec<String>>) -> (usize, usize) {
    (
        passphrases
            .iter()
            .filter(|passphrase| {
                !passphrase
                    .iter()
                    .any(|word| passphrase.iter().filter(|w| *w == word).count() > 1)
            })
            .count(),
        passphrases
            .iter()
            .filter(|passphrase| has_no_anagram(passphrase))
            .count(),
    )
}

fn get_input(file_path: &String) -> Vec<Vec<String>> {
    fs::read_to_string(file_path)
        .expect("Error reading input file!")
        .lines()
        .map(|line| line.split(" ").map(|split| String::from(split)).collect())
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
