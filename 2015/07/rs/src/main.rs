use regex::Regex;
use std::clone::Clone;
use std::collections::HashMap;

type Connections = HashMap<String, Connection>;

pub enum Operand {
    Scalar(u32),
    Wire(String),
}

impl Operand {
    fn new(value: String) -> Operand {
        if let Ok(scalar) = value.parse() {
            return Operand::Scalar(scalar);
        }
        Operand::Wire(value)
    }
}

impl Clone for Operand {
    fn clone(&self) -> Operand {
        match self {
            Operand::Scalar(v) => Operand::Scalar(*v),
            Operand::Wire(w) => Operand::Wire(String::from(w)),
        }
    }
}

pub enum Operation {
    And,
    Or,
    Lshift,
    Rshift,
}

impl Operation {
    fn new(value: &str) -> Operation {
        match value {
            "AND" => Operation::And,
            "OR" => Operation::Or,
            "LSHIFT" => Operation::Lshift,
            "RSHIFT" => Operation::Rshift,
            _ => panic!("Unrecognized operation {}", value),
        }
    }
}

pub enum Connection {
    Input(Operand),
    Not(Operand),
    Binary(Operand, Operand, Operation),
}

pub struct CircuitSolver {
    solutions: Box<HashMap<String, u32>>,
}

impl CircuitSolver {
    pub fn new(solutions: HashMap<String, u32>) -> CircuitSolver {
        CircuitSolver {
            solutions: Box::new(solutions),
        }
    }

    fn get_value_from_operand(&mut self, operand: &Operand, connections: &Connections) -> u32 {
        match operand {
            Operand::Scalar(value) => *value,
            Operand::Wire(wire) => {
                self.get_value_from_connection(wire, connections.get(wire).unwrap(), connections)
            }
        }
    }

    fn get_value_from_binary_connection(
        &mut self,
        operand1: &Operand,
        operand2: &Operand,
        operation: &Operation,
        connections: &Connections,
    ) -> u32 {
        let x = self.get_value_from_operand(&operand1, connections);
        let y = self.get_value_from_operand(&operand2, connections);
        match operation {
            Operation::And => x & y,
            Operation::Or => x | y,
            Operation::Lshift => x << y,
            Operation::Rshift => x >> y,
        }
    }

    fn calculate_value_for_connection(
        &mut self,
        connection: &Connection,
        connections: &Connections,
    ) -> u32 {
        match connection {
            Connection::Input(operand) => self.get_value_from_operand(operand, connections),
            Connection::Not(operand) => !self.get_value_from_operand(operand, connections),
            Connection::Binary(operand1, operand2, operation) => {
                self.get_value_from_binary_connection(operand1, operand2, operation, connections)
            }
        }
    }

    fn get_value_from_connection(
        &mut self,
        target: &str,
        connection: &Connection,
        connections: &Connections,
    ) -> u32 {
        if let Some(value) = self.solutions.get(target) {
            return *value;
        } else {
            let result = self.calculate_value_for_connection(connection, connections);
            self.solutions
                .entry(String::from(target.clone()))
                .or_insert(result);
            result
        }
    }

    pub fn solve_for(&mut self, target: &str, connections: &Connections) -> u32 {
        self.get_value_from_connection(target, connections.get(target).unwrap(), connections)
    }
}

fn solve(connections: &Connections) -> (u32, u32) {
    let part1 = CircuitSolver::new(HashMap::new()).solve_for("a", connections);
    let mut solutions = HashMap::new();
    solutions.insert(String::from("b"), part1);
    (
        part1,
        CircuitSolver::new(solutions).solve_for("a", connections),
    )
}

fn get_input(file_path: &String) -> Connections {
    let source_target_regex = Regex::new(r"^(.*)\s->\s(\w+)$").unwrap();
    let input_regex = Regex::new(r"^[^\s]+$").unwrap();
    let unary_regex = Regex::new(r"NOT\s(\w+)$").unwrap();
    let binary_regex = Regex::new(r"^(\w+|\d+)\s+(AND|OR|LSHIFT|RSHIFT)\s+(\w+|\d+)").unwrap();
    std::fs::read_to_string(file_path)
        .expect("Error reading input file!")
        .lines()
        .map(|line| match source_target_regex.captures(line) {
            Some(cap) => {
                let source = String::from(cap.get(1).unwrap().as_str());
                let target = String::from(cap.get(2).unwrap().as_str());
                if input_regex.is_match(&source) {
                    return (target, Connection::Input(Operand::new(source)));
                }
                if let Some(unary_cap) = unary_regex.captures(&source) {
                    return (
                        target,
                        Connection::Not(Operand::new(String::from(
                            unary_cap.get(1).unwrap().as_str(),
                        ))),
                    );
                }
                if let Some(binary_cap) = binary_regex.captures(&source) {
                    return (
                        target,
                        Connection::Binary(
                            Operand::new(String::from(binary_cap.get(1).unwrap().as_str())),
                            Operand::new(String::from(binary_cap.get(3).unwrap().as_str())),
                            Operation::new(binary_cap.get(2).unwrap().as_str()),
                        ),
                    );
                };
                panic!("Unrecognized operation source: {}", source)
            }
            _ => panic!("Unrecognized operation line: {}", line),
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
    println!("Time: {:7}", end);
}
