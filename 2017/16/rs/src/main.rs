type Instruction = (usize, usize, usize);

fn to_ord(programs: &str) -> Vec<u8> {
    programs.chars().map(|c| c as u8).collect()
}

fn to_str(programs: &Vec<u8>) -> String {
    programs.into_iter().map(|c| *c as char).collect()
}

fn dance(instructions: &Vec<Instruction>, programs: Vec<u8>) -> Vec<u8> {
    let mut programs = programs.clone();
    for (move_, a, b) in instructions {
        match move_ {
            0 => {
                let index = programs.len() - a;
                let tail: Vec<u8> = programs.clone().into_iter().take(index).collect();
                programs = programs.into_iter().skip(index).collect();
                programs.extend(tail);
            }
            1 => {
                let old_a = programs[*a];
                programs[*a] = programs[*b];
                programs[*b] = old_a;
            }
            2 => {
                let a_index = programs.iter().position(|c| *c == *a as u8).unwrap();
                let b_index = programs.iter().position(|c| *c == *b as u8).unwrap();
                let old_a = programs[a_index];
                programs[a_index] = programs[b_index];
                programs[b_index] = old_a;
            }
            _ => {}
        }
    }
    programs
}

fn part2(instructions: &Vec<Instruction>) -> String {
    const CYCLES: usize = usize::pow(10, 9);
    let mut programs = to_ord("abcdefghijklmnop");
    let mut seen = Vec::new();
    seen.push(programs.clone());
    for cycle in 0..CYCLES {
        programs = dance(instructions, programs);
        let p = programs.clone();
        if seen.contains(&p) {
            return to_str(&seen[CYCLES % (cycle + 1)]);
        }
        seen.push(p);
    }
    to_str(&programs)
}

fn solve(instructions: &Vec<Instruction>) -> (String, String) {
    (
        to_str(&dance(instructions, to_ord("abcdefghijklmnop"))),
        part2(instructions),
    )
}

fn get_input(file_path: &String) -> Vec<Instruction> {
    std::fs::read_to_string(file_path)
        .expect("Error reading input file!")
        .split(",")
        .map(|text| {
            if text.starts_with("s") {
                (0, text[1..].parse().unwrap(), 0)
            } else if text.starts_with("x") {
                let split: Vec<&str> = text[1..].split("/").collect();
                (1, split[0].parse().unwrap(), split[1].parse().unwrap())
            } else if text.starts_with("p") {
                let split: Vec<&str> = text[1..].split("/").collect();
                (
                    2,
                    split[0].chars().nth(0).unwrap() as usize,
                    split[1].chars().nth(0).unwrap() as usize,
                )
            } else {
                panic!("Unknown instructions '{}'", text)
            }
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
