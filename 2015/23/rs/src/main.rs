enum Instruction {
    HLF(usize),
    TPL(usize),
    INC(usize),
    JMP(isize),
    JIE(usize, isize),
    JIO(usize, isize),
}

const OFFSET: usize = 'a' as usize;
impl Instruction {
    fn parse(line: &str) -> Instruction {
        let splits: Vec<&str> = line.split(" ").collect();
        if line.starts_with("hlf") {
            Self::HLF(splits[1].chars().next().unwrap() as usize - OFFSET)
        } else if line.starts_with("tpl") {
            Self::TPL(splits[1].chars().next().unwrap() as usize - OFFSET)
        } else if line.starts_with("inc") {
            Self::INC(splits[1].chars().next().unwrap() as usize - OFFSET)
        } else if line.starts_with("jmp") {
            Self::JMP(splits[1].parse().unwrap())
        } else if line.starts_with("jie") {
            Self::JIE(
                splits[1].chars().next().unwrap() as usize - OFFSET,
                splits[2].parse().unwrap(),
            )
        } else if line.starts_with("jio") {
            Self::JIO(
                splits[1].chars().next().unwrap() as usize - OFFSET,
                splits[2].parse().unwrap(),
            )
        } else {
            panic!("Bad format '{}'", line);
        }
    }
}

fn run_program(instructions: &Vec<Instruction>, registers: Vec<i32>) -> i32 {
    let mut registers = registers.clone();
    let mut pointer = 0;
    while pointer < instructions.len() {
        use Instruction::*;
        let mut jump = 1;
        match instructions[pointer] {
            HLF(register) => registers[register] /= 2,
            TPL(register) => registers[register] *= 3,
            INC(register) => registers[register] += 1,
            JMP(value) => jump = value,
            JIE(register, value) => {
                if registers[register] % 2 == 0 {
                    jump = value
                }
            }
            JIO(register, value) => {
                if registers[register] == 1 {
                    jump = value
                }
            }
        }
        if jump > 0 {
            pointer += jump as usize;
        } else {
            pointer -= -jump as usize;
        }
    }
    registers[1]
}

fn solve(instructions: &Vec<Instruction>) -> (i32, i32) {
    (
        run_program(instructions, vec![0, 0]),
        run_program(instructions, vec![1, 0]),
    )
}

fn get_input(file_path: &String) -> Vec<Instruction> {
    std::fs::read_to_string(file_path)
        .expect("Error reading input file!")
        .lines()
        .map(|line| Instruction::parse(line))
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
