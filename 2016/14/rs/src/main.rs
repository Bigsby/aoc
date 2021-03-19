use fancy_regex::Regex;

fn _pause() {
    let mut input: String = String::new();
    std::io::stdin()
        .read_line(&mut input)
        .expect("error inputing");
}

fn find_key(salt: &str, stretch: usize) -> usize {
    let triplet_regex = Regex::new(r"(.)\1{2}").unwrap();
    let quintet_regex = Regex::new(r"(.)\1{4}").unwrap();
    let mut index = 0usize;
    let mut keys = Vec::new();
    let mut threes: Vec<(char, usize)> = Vec::new();
    while keys.len() < 64 {
        let mut value = format!("{}{}", salt, index);
        for _ in 0..stretch + 1 {
            value = format!("{:x}", md5::compute(value));
        }
        if let Ok(Some(cap)) = quintet_regex.captures(&value) {
            let digit = cap.get(1).unwrap().as_str().chars().next().unwrap();
            for (_, triplet_index) in threes
                .iter()
                .filter(|(c, ti)| c == &digit && index - ti <= 1000)
            {
                keys.push(*triplet_index);
            }
            threes.retain(|(c, _)| c != &digit);
        }
        if let Ok(Some(cap)) = triplet_regex.captures(&value) {
            threes.push((cap.get(1).unwrap().as_str().chars().next().unwrap(), index));
        }
        index += 1;
    }
    keys.into_iter().nth(63).unwrap()
}

fn solve(salt: &str) -> (usize, usize) {
    (find_key(salt, 0), find_key(salt, 2016))
}

fn get_input(file_path: &String) -> String {
    String::from(
        std::fs::read_to_string(file_path)
            .expect("Error reading input file!")
            .trim(),
    )
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
