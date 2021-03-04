fn part1(polymer: &str) -> usize {
    let mut polymer_ints = polymer
        .as_bytes()
        .iter()
        .map(|c| *c as i8)
        .collect::<Vec<i8>>();
    let mut had_changes = true;
    while had_changes {
        had_changes = false;
        let mut index = 0;
        while index < polymer_ints.len() - 1 {
            if i8::abs(polymer_ints[index] - polymer_ints[index + 1]) == 32 {
                polymer_ints.remove(index as usize);
                polymer_ints.remove(index as usize);
                had_changes = true;
            } else {
                index += 1;
            }
        }
    }
    polymer_ints.len()
}

fn part2(polymer: &str) -> usize {
    let mut min_units = usize::MAX;
    for c_ord in b'A'..(b'Z' + 1) {
        let stripped_polymer = polymer.replace((c_ord as char).to_string().as_str(), "");
        let stripped_polymer = stripped_polymer.replace(((c_ord + 32) as char).to_string().as_str(), "");
        min_units = min_units.min(part1(&stripped_polymer));
    }
    min_units
}

fn solve(polymer: &str) -> (usize, usize) {
    (part1(polymer), part2(polymer))
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
    println!("P1: {}", part1_result);
    println!("P1: {}", part2_result);
    println!();
    println!("Time: {:7}", now.elapsed().as_secs_f32());
}
