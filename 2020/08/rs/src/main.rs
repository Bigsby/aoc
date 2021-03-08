use regex::Regex;

type Instruction = (String, i32);
static JMP: &str = "jmp";
static NOP: &str = "nop";
static ACC: &str = "acc";

fn run_instruction(op: &Instruction, accumulator: i32, instruction_pointer: i32) -> (i32, i32) {
    let (mnemonic, argument) = op;
    (
        accumulator + if mnemonic == ACC { *argument } else { 0 },
        instruction_pointer + if mnemonic == JMP { *argument } else { 1 },
    )
}

fn run_boot(boot: &Vec<Instruction>) -> (bool, i32) {
    let mut accumulator = 0;
    let mut instruction_pointer = 0;
    let mut visited = Vec::new();
    let boot_length = boot.len() as i32;
    loop {
        visited.push(instruction_pointer);
        let result = run_instruction(
            &boot[instruction_pointer as usize],
            accumulator,
            instruction_pointer,
        );
        accumulator = result.0;
        instruction_pointer = result.1;
        if visited.contains(&instruction_pointer) {
            return (false, accumulator);
        }
        if instruction_pointer == boot_length {
            return (true, accumulator);
        }
    }
}

fn switch_and_test(index: usize, boot: &Vec<Instruction>) -> (bool, i32) {
    let mut boot = boot.clone();
    let (mnemonic, argument) = &boot[index];
    boot[index] = (
        if mnemonic == JMP {
            String::from(NOP)
        } else {
            String::from(JMP)
        },
        *argument,
    );
    run_boot(&boot)
}

fn part2(boot: &Vec<Instruction>) -> i32 {
    for index in 0..boot.len() {
        if boot[index].0 == ACC {
            continue;
        }
        let (success, accumulator) = switch_and_test(index, boot);
        if success {
            return accumulator;
        }
    }
    panic!("Valid boot not found")
}

fn solve(instructions: &Vec<Instruction>) -> (i32, i32) {
    (run_boot(instructions).1, part2(instructions))
}

fn get_input(file_path: &String) -> Vec<Instruction> {
    let re = Regex::new(r"^(nop|acc|jmp)\s\+?(-?\d+)$").unwrap();
    std::fs::read_to_string(file_path)
        .expect("Error reading input file!")
        .lines()
        .map(|line| {
            re.captures(line)
                .map(|cap| {
                    (
                        String::from(cap.get(1).unwrap().as_str()),
                        cap.get(2).unwrap().as_str().parse().unwrap(),
                    )
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
    println!("P1: {}", part2_result);
    println!();
    println!("Time: {:.7}", end);
}
