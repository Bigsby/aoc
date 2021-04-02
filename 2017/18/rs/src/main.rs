use core::cell::RefCell;
use std::collections::{HashMap, VecDeque};
use std::sync::mpsc::{channel, Sender};

type Register = u8;
type Value = i64;

#[derive(Debug, Copy, Clone)]
enum Param {
    Register(Register),
    Value(Value),
}

impl Param {
    fn parse_register(value: &str) -> u8 {
        value.chars().next().unwrap() as u8
    }

    fn parse(value: &str) -> Param {
        if let Ok(int) = value.parse() {
            Param::Value(int)
        } else {
            Param::Register(Param::parse_register(value))
        }
    }
}

#[derive(Debug, Copy, Clone)]
enum Instruction {
    Set(Register, Param),
    Add(Register, Param),
    Mul(Register, Param),
    Mod(Register, Param),
    Snd(Register),
    Rcv(Register),
    Jgz(Param, Param),
}

struct Program {
    instructions: Vec<Instruction>,
    id: Value,
    output_on_receive: bool,
    registers: RefCell<HashMap<Register, Value>>,
    pointer: usize,
    output: Value,
    inputs: RefCell<VecDeque<Value>>,
    output_count: usize,
    running: bool,
    polling: bool,
    sender: Sender<(Value, Value)>,
}

impl Program {
    pub fn new(
        instructions: &Vec<Instruction>,
        id: Value,
        output_on_receive: bool,
        sender: Sender<(Value, Value)>,
    ) -> Program {
        let mut registers = HashMap::new();
        registers.insert(b'p', id);
        Program {
            instructions: instructions.into_iter().map(|i| *i).collect(),
            id,
            output_on_receive,
            registers: RefCell::new(registers),
            pointer: 0,
            output: 0,
            inputs: RefCell::new(VecDeque::new()),
            output_count: 0,
            running: true,
            polling: false,
            sender,
        }
    }

    fn _pause() {
        let mut input: String = String::new();
        std::io::stdin()
            .read_line(&mut input)
            .expect("error inputing");
    }

    fn get_value(&mut self, param: Param) -> Value {
        match param {
            Param::Register(register) => *self.registers.borrow_mut().entry(register).or_insert(0),
            Param::Value(value) => value,
        }
    }

    fn add_intput(&mut self, value: Value) {
        self.inputs.borrow_mut().push_back(value);
    }

    fn tick(&mut self) -> bool {
        use Instruction::*;
        if self.running {
            match self.instructions[self.pointer] {
                Set(register, param) => {
                    *self.registers.borrow_mut().entry(register).or_insert(0) =
                        self.get_value(param)
                }
                Add(register, param) => {
                    *self.registers.borrow_mut().entry(register).or_insert(0) +=
                        self.get_value(param)
                }
                Mul(register, param) => {
                    *self.registers.borrow_mut().entry(register).or_insert(0) *=
                        self.get_value(param)
                }
                Mod(register, param) => {
                    *self.registers.borrow_mut().entry(register).or_insert(0) %=
                        self.get_value(param)
                }
                Snd(register) => {
                    self.output_count += 1;
                    self.output = self.get_value(Param::Register(register));
                    if let Err(_) = self.sender.send((self.id, self.output)) {
                        panic!("Error sending message.");
                    }
                }
                Rcv(register) => {
                    if self.output_on_receive {
                        return false;
                    } else if let Some(input) = self.inputs.borrow_mut().pop_front() {
                        self.polling = false;
                        *self.registers.borrow_mut().entry(register).or_insert(0) = input;
                    } else {
                        self.polling = true;
                        self.pointer -= 1;
                    }
                }
                Jgz(param1, param2) => {
                    if self.get_value(param1) > 0 {
                        self.pointer =
                            (self.pointer as Value + self.get_value(param2)) as usize - 1;
                    }
                }
            }
            self.pointer += 1;
            self.running = self.pointer < self.instructions.len()
        }
        self.running && !self.polling
    }
}

fn part1(instructions: &Vec<Instruction>) -> Value {
    let (sender, _receiver) = channel();
    let mut program = Program::new(instructions, 0, true, sender);
    while program.tick() {}
    program.output
}

fn part2(instructions: &Vec<Instruction>) -> usize {
    let (sender, receiver) = channel();
    let mut program0 = Program::new(instructions, 0, false, sender.clone());
    let mut program1 = Program::new(instructions, 1, false, sender.clone());
    while program0.tick() || program1.tick() {
        while let Ok((id, value)) = receiver.try_recv() {
            match id {
                0 => program1.add_intput(value),
                1 => program0.add_intput(value),
                _ => {
                    panic!("Invalid id for transmission '{}'", id)
                }
            }
        }
    }
    program1.output_count
}

fn solve(instructions: &Vec<Instruction>) -> (Value, usize) {
    (part1(instructions), part2(instructions))
}

fn get_input(file_path: &String) -> Vec<Instruction> {
    use Instruction::*;
    std::fs::read_to_string(file_path)
        .expect("Error reading input file!")
        .lines()
        .map(|line| {
            let splits: Vec<&str> = line.split(" ").collect();
            match splits[0] {
                "set" => Set(Param::parse_register(splits[1]), Param::parse(splits[2])),
                "add" => Add(Param::parse_register(splits[1]), Param::parse(splits[2])),
                "mul" => Mul(Param::parse_register(splits[1]), Param::parse(splits[2])),
                "mod" => Mod(Param::parse_register(splits[1]), Param::parse(splits[2])),
                "snd" => Snd(Param::parse_register(splits[1])),
                "rcv" => Rcv(Param::parse_register(splits[1])),
                "jgz" => Jgz(Param::parse(splits[1]), Param::parse(splits[2])),
                _ => {
                    panic!("Unknow instructions '{}'", line)
                }
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
