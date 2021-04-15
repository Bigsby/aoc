#[derive(Copy, Clone, Debug)]
enum Param {
    Value(isize),
    Register(usize),
}

const OFFSET: usize = 'a' as usize;

impl Param {
    fn as_register(&self) -> usize {
        match self {
            Self::Value(value) => *value as usize,
            Self::Register(register) => *register,
        }
    }

    fn as_value(&self) -> isize {
        match self {
            Self::Value(value) => *value,
            Self::Register(register) => *register as isize,
        }
    }

    fn get_register(value: &str) -> usize {
        value.chars().next().unwrap() as usize - OFFSET
    }

    fn get_value(&self, registers: &Vec<isize>) -> isize {
        match self {
            Param::Value(value) => *value,
            Param::Register(register) => registers[*register],
        }
    }

    fn parse(value: &str) -> Param {
        if let Ok(immediate) = value.parse::<isize>() {
            Param::Value(immediate)
        } else {
            Param::Register(Param::get_register(value))
        }
    }
}

#[derive(Copy, Clone, Debug)]
enum Instruction {
    CPY(Param, usize),
    INC(usize),
    DEC(usize),
    JNZ(Param, Param),
    TGL(usize),
}

impl Instruction {
    fn toggle(&self) -> Instruction {
        match self {
            Self::INC(register) => Self::DEC(*register),
            Self::DEC(register) => Self::INC(*register),
            Self::TGL(register) => Self::INC(*register),
            Self::JNZ(register, value) => Self::CPY(*register, value.as_register()),
            Self::CPY(source, register) => Self::JNZ(*source, Param::Register(*register)),
        }
    }

    fn parse(line: &str) -> Instruction {
        let splits: Vec<&str> = line.split(" ").collect();
        match splits[0] {
            "inc" => Instruction::INC(Param::get_register(splits[1])),
            "dec" => Instruction::DEC(Param::get_register(splits[1])),
            "tgl" => Instruction::TGL(Param::get_register(splits[1])),
            "cpy" => Instruction::CPY(Param::parse(splits[1]), Param::get_register(splits[2])),
            "jnz" => Instruction::JNZ(Param::parse(splits[1]), Param::parse(splits[2])),
            _ => {
                panic!("Bad instruction '{}'", line);
            }
        }
    }

    fn first_value(&self) -> isize {
        match self {
            Self::INC(register) => *register as isize,
            Self::DEC(register) => *register as isize,
            Self::TGL(register) => *register as isize,
            Self::JNZ(param, _) => param.as_value(),
            Self::CPY(param, _) => param.as_value(),
        }
    }
}

fn run_instructions(instructions: &Vec<Instruction>, registers: Vec<isize>) -> isize {
    let mut registers = registers.clone();
    let mut instructions = instructions.clone();
    let mut pointer = 0;
    while pointer < instructions.len() {
        use Instruction::*;
        let mut jump = 1isize;
        match instructions[pointer] {
            CPY(source, register) => {
                registers[register] = source.get_value(&registers);
            }
            INC(register) => registers[register] += 1,
            DEC(register) => registers[register] -= 1,
            JNZ(register, value) => {
                if register.get_value(&registers) != 0 {
                    jump = value.get_value(&registers);
                }
            }
            TGL(register) => {
                let offset = registers[register];
                let pointer_to_change = if offset > 0 {
                    pointer + offset as usize
                } else {
                    pointer - (-offset as usize)
                };
                if pointer_to_change < instructions.len() {
                    instructions[pointer_to_change] = instructions[pointer_to_change].toggle();
                }
            }
        }
        if jump > 0 {
            pointer += jump as usize;
        } else {
            pointer -= -jump as usize;
        }
    }
    registers[0]
}

fn factorial(num: u64) -> u64 {
    match num {
        0 | 1 => 1,
        _ => factorial(num - 1) * num,
    }
}

fn solve(instructions: &Vec<Instruction>) -> (isize, u64) {
    let a = instructions[19].first_value() as u64;
    let b = instructions[20].first_value() as u64;
    (
        run_instructions(instructions, vec![7, 0, 0, 0]),
        factorial(12) + a * b,
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
