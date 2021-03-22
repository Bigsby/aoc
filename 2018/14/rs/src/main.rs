fn _pause() {
    let mut input: String = String::new();
    std::io::stdin()
        .read_line(&mut input)
        .expect("error inputing");
}

fn solve(target: &usize) -> (String, usize) {
    let target = *target;
    let mut part1_result = String::default();
    let mut part1_set = false;
    let score_sequence: Vec<usize> = target
        .to_string()
        .chars()
        .map(|c| c as usize - 48)
        .collect();
    let score_length = score_sequence.len();
    let mut recipes = vec![3, 7];
    let mut elf1 = 0;
    let mut elf2 = 1;
    loop {
        let mut score = recipes[elf1] + recipes[elf2];
        let two_digit_score = score > 9;
        if two_digit_score {
            recipes.push(score / 10);
            score %= 10;
        }
        recipes.push(score);
        elf1 = (elf1 + 1 + recipes[elf1]) % recipes.len();
        elf2 = (elf2 + 1 + recipes[elf2]) % recipes.len();
        let recipes_length = recipes.len();
        if !part1_set && recipes_length > target + 10 {
            part1_set = true;
            part1_result = recipes[target..target + 10]
                .iter()
                .map(|v| v.to_string())
                .collect();
        }
        if recipes_length > score_length
            && recipes[recipes_length - score_length..recipes_length] == score_sequence
        {
            return (part1_result, recipes_length - score_length);
        }
        if two_digit_score
            && recipes_length > score_length + 1
            && recipes[recipes_length - 1 - score_length..recipes_length - 1] == score_sequence
        {
            return (part1_result, recipes_length - 1 - score_length);
        }
    }
}

fn get_input(file_path: &String) -> usize {
    std::fs::read_to_string(file_path)
        .expect("Error reading input file!")
        .trim()
        .parse()
        .unwrap()
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
