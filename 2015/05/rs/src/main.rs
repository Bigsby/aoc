use regex::Regex;

fn has_repeated_chars(word: &str) -> bool {
    let word = word.chars().collect::<Vec<char>>();
    (0..word.len() - 1).any(|index| word[index] == word[index + 1])
}

fn part1(words: &Vec<String>) -> usize {
    let forbidden_pairs = vec!["ab", "cd", "pq", "xy"];
    let vowel_regex = Regex::new(r"[aeiou]").unwrap();
    words
        .iter()
        .filter(|word| {
            !forbidden_pairs.iter().any(|pair| word.contains(pair))
                && vowel_regex.captures_iter(word).count() > 2
                && has_repeated_chars(word)
        })
        .count()
}

fn has_repeating_pair(word: &str) -> bool {
    (0..(word.len() - 2)).any(|pair_start| {
        let pair_to_test: &str = &word[pair_start..pair_start + 2];
        word[..pair_start].contains(pair_to_test) || word[pair_start + 2..].contains(pair_to_test)
    })
}

fn has_repeating_letter(word: &str) -> bool {
    let word = word.chars().collect::<Vec<char>>();
    (0..(word.len() - 2)).any(|index| word[index] == word[index + 2])
}

fn solve(words: &Vec<String>) -> (usize, usize) {
    (
        part1(words),
        words
            .iter()
            .filter(|word| has_repeating_pair(word) && has_repeating_letter(word))
            .count(),
    )
}

fn get_input(file_path: &String) -> Vec<String> {
    std::fs::read_to_string(file_path)
        .expect("Error reading input file!")
        .lines()
        .map(|line| String::from(line.trim()))
        .collect()
}

fn main() {
    let args: Vec<String> = std::env::args().collect();
    if args.len() != 2 {
        panic!("Please, add input file path as parameter");
    }
    let now = std::time::Instant::now();
    let (part1_result, part2_result) = solve(&get_input(&args[1]));
    println!("P1: {}", part1_result);
    println!("P1: {}", part2_result);
    println!();
    println!("Time: {:7}", now.elapsed().as_secs_f32());
}
