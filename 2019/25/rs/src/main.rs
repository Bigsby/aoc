use itertools::Itertools;
use regex::Regex;
use std::cell::RefCell;
use std::collections::{HashMap, VecDeque};

#[derive(Clone)]
pub struct IntCodeComputer {
    memory: RefCell<HashMap<i64, i64>>,
    input: RefCell<VecDeque<i64>>,
    output: RefCell<VecDeque<i64>>,
    pointer: i64,
    base: i64,
    pub running: bool,
    pub outputing: bool,
    pub polling: bool,
    paused: bool,
}

impl IntCodeComputer {
    pub fn new(memory: &Vec<i64>, input: Vec<i64>) -> IntCodeComputer {
        IntCodeComputer {
            memory: RefCell::new(
                memory
                    .clone()
                    .into_iter()
                    .enumerate()
                    .map(|(index, value)| (index as i64, value))
                    .collect(),
            ),
            input: RefCell::new(VecDeque::from(input)),
            output: RefCell::new(VecDeque::new()),
            pointer: 0,
            base: 0,
            running: true,
            outputing: false,
            polling: false,
            paused: false,
        }
    }

    pub fn run(&mut self) -> i64 {
        while self.tick() {}
        self.output.borrow_mut().pop_back().unwrap()
    }

    pub fn run_until_paused(&mut self) {
        self.paused = false;
        while !self.paused && self.running {
            self.tick();
        }
    }

    pub fn get_output(&mut self) -> Option<i64> {
        self.outputing = false;
        self.output.borrow_mut().pop_front()
    }

    fn add_input(&mut self, value: i64) {
        self.input.borrow_mut().push_back(value);
    }

    fn get_memory_value(&self, location: i64) -> i64 {
        if let Some(value) = self.memory.borrow().get(&location) {
            *value
        } else {
            0
        }
    }

    fn get_parameter(&self, offset: i64, mode: i64) -> i64 {
        let value = self.get_memory_value(self.pointer + offset);
        match mode {
            0 => self.get_memory_value(value),             // POSITION
            1 => value,                                    // IMMEDIATE
            2 => self.get_memory_value(self.base + value), // RELATIVE
            _ => {
                panic!("Unrecognized parameter mode '{}'", mode);
            }
        }
    }

    fn get_address(&self, offset: i64, mode: i64) -> i64 {
        let value = self.get_memory_value(self.pointer + offset);
        match mode {
            0 => value,             // POSITION
            2 => self.base + value, // RELATIVE
            _ => {
                panic!("Unrecognized address mode '{}'", mode);
            }
        }
    }

    fn set_memory(&mut self, offset: i64, mode: i64, value: i64) {
        let address = self.get_address(offset, mode);
        *self.memory.borrow_mut().entry(address).or_insert(0) = value;
    }

    fn tick(&mut self) -> bool {
        if !self.running {
            return false;
        }
        let instruction = *self.memory.borrow().get(&self.pointer).unwrap();
        let (opcode, p1_mode, p2_mode, p3_mode) = (
            instruction % 100,
            (instruction / 100) % 10,
            (instruction / 1000) % 10,
            (instruction / 10000) % 10,
        );
        match opcode {
            1 => {
                // ADD
                self.set_memory(
                    3,
                    p3_mode,
                    self.get_parameter(1, p1_mode) + self.get_parameter(2, p2_mode),
                );
                self.pointer += 4;
            }
            2 => {
                // MUL
                self.set_memory(
                    3,
                    p3_mode,
                    self.get_parameter(1, p1_mode) * self.get_parameter(2, p2_mode),
                );
                self.pointer += 4;
            }
            3 => {
                // INPUT
                let input = self.input.borrow_mut().pop_front();
                if let Some(value) = input {
                    self.polling = false;
                    self.set_memory(1, p1_mode, value);
                    self.pointer += 2;
                } else {
                    self.paused = true;
                }
            }
            4 => {
                // OUTPUT
                self.outputing = true;
                self.output
                    .borrow_mut()
                    .push_back(self.get_parameter(1, p1_mode));
                self.pointer += 2;
            }
            5 => {
                // JMP_TRUE
                if self.get_parameter(1, p1_mode) != 0 {
                    self.pointer = self.get_parameter(2, p2_mode);
                } else {
                    self.pointer += 3;
                }
            }
            6 => {
                // JMP_FALSE
                if self.get_parameter(1, p1_mode) == 0 {
                    self.pointer = self.get_parameter(2, p2_mode);
                } else {
                    self.pointer += 3;
                }
            }
            7 => {
                // LESS_THAN
                self.set_memory(
                    3,
                    p3_mode,
                    if self.get_parameter(1, p1_mode) < self.get_parameter(2, p2_mode) {
                        1
                    } else {
                        0
                    },
                );
                self.pointer += 4;
            }
            8 => {
                // EQUALS
                self.set_memory(
                    3,
                    p3_mode,
                    if self.get_parameter(1, p1_mode) == self.get_parameter(2, p2_mode) {
                        1
                    } else {
                        0
                    },
                );
                self.pointer += 4;
            }
            9 => {
                // SET_BASE
                self.base += self.get_parameter(1, p1_mode);
                self.pointer += 2;
            }
            99 => {
                // HALT
                self.running = false;
            }
            _ => panic!("Unknown instruction {} {}", self.pointer, opcode),
        }
        self.running
    }
}

struct Crawler<'a> {
    room_regex: Regex,
    entry_regex: Regex,
    password_regex: Regex,
    forbiden_items: Vec<&'a str>,
    rooms: RefCell<Vec<String>>,
    directions: Vec<&'a str>,
    pressure_room: usize,
    items: RefCell<Vec<String>>,
    take: &'a str,
    drop: &'a str,
    droid: IntCodeComputer,
}

impl Crawler<'_> {
    fn new(memory: &Vec<i64>) -> Crawler<'static> {
        Crawler {
            room_regex: Regex::new(r"^== (?P<room>.*) ==").unwrap(),
            entry_regex: Regex::new(r"- (?P<entry>.*)").unwrap(),
            password_regex: Regex::new(r"typing (?P<password>\d+)").unwrap(),
            forbiden_items: vec![
                "molten lava",
                "photons",
                "infinite loop",
                "giant electromagnet",
                "escape pod",
            ],
            rooms: RefCell::new(vec![String::from("Security Checkpoint")]),
            directions: vec!["north", "west", "south", "east"],
            pressure_room: 0,
            items: RefCell::new(Vec::new()),
            take: "take ",
            drop: "drop ",
            droid: IntCodeComputer::new(memory, vec![]),
        }
    }

    fn get_item_index(&mut self, item: &str) -> usize {
        if let Some(index) = self.items.borrow().iter().position(|r| r == &item) {
            return index;
        }
        self.items.borrow_mut().push(String::from(item));
        self.items.borrow().len() - 1
    }

    fn get_direction_index(&self, direction: &str) -> usize {
        self.directions
            .iter()
            .position(|d| d == &direction)
            .unwrap()
    }

    fn get_room_index(&mut self, room: &str) -> usize {
        if let Some(index) = self.rooms.borrow().iter().position(|r| r == &room) {
            return index;
        }
        self.rooms.borrow_mut().push(String::from(room));
        self.rooms.borrow().len() - 1
    }

    fn parse_room_output(&mut self, output: &str) -> (usize, Vec<usize>, Vec<String>) {
        let mut stage = 0;
        let mut room = 0;
        let mut doors = Vec::new();
        let mut items = Vec::new();
        for line in output.split("\n") {
            match stage {
                0 => {
                    if let Some(cap) = self.room_regex.captures(line) {
                        room = self.get_room_index(cap.name("room").unwrap().as_str());
                        stage = 1;
                    }
                }
                1 => {
                    if line.starts_with("Doors") {
                        stage = 2;
                    }
                }
                2 => {
                    if let Some(cap) = self.entry_regex.captures(line) {
                        doors.push(self.get_direction_index(cap.name("entry").unwrap().as_str()));
                    } else {
                        stage = 3;
                    }
                }
                3 => {
                    if line.starts_with("Items") {
                        stage = 4;
                    }
                }
                4 => {
                    if let Some(cap) = self.entry_regex.captures(line) {
                        items.push(String::from(cap.name("entry").unwrap().as_str()));
                    } else {
                        break;
                    }
                }
                _ => (),
            }
        }
        (room, doors, items)
    }

    fn run_command(&mut self, command: &str) -> String {
        if !command.is_empty() {
            for c in command.chars() {
                self.droid.add_input(c as i64);
            }
            self.droid.add_input(10);
        }
        self.droid.run_until_paused();
        let mut output = String::default();
        while let Some(c) = self.droid.get_output() {
            output.push((c as u8) as char);
        }
        output
    }

    // use to play manually
    fn _manual_scout(&mut self) {
        println!("Scouting");
        let mut command = String::default();
        while command != String::from("quit") && self.droid.running {
            let output = self.run_command(&command);
            println!("{:?}", self.parse_room_output(&output));
            print!("$ ");
            std::io::stdin()
                .read_line(&mut command)
                .expect("Error reading input");
        }
    }

    fn create_take_command(&mut self, item: usize) -> String {
        let mut result = String::from(self.take);
        result.push_str(&self.items.borrow()[item]);
        result
    }

    fn create_drop_command(&mut self, item: usize) -> String {
        let mut result = String::from(self.drop);
        result.push_str(&self.items.borrow()[item]);
        result
    }

    fn navigate_rooms(
        &mut self,
        command: &str,
        destination: usize,
        pickup_items: bool,
    ) -> (String, Vec<String>, String) {
        let mut command = String::from(command);
        let mut visited: Vec<(usize, usize)> = Vec::new();
        let mut way_in = HashMap::new();
        let mut last_direction = 5;
        let mut pressure_room_way_in = String::default();
        let mut inventory = Vec::new();
        while self.droid.running {
            let output = self.run_command(&command);
            let (room, doors, items) = self.parse_room_output(&output);
            if room == destination {
                break;
            }
            if room == self.pressure_room {
                pressure_room_way_in = String::from(self.directions[last_direction]);
            }
            if !way_in.contains_key(&room) {
                way_in.insert(room, last_direction);
            }
            if pickup_items {
                for item in items.iter() {
                    if !self.forbiden_items.contains(&item.as_str()) {
                        let item_index = self.get_item_index(&item);
                        let command = self.create_take_command(item_index);
                        self.run_command(&command);
                        inventory.push(item.clone());
                    }
                }
            }
            let mut new_door = false;
            for door in doors.iter() {
                let room_door_pair = (room, *door);
                if !visited.contains(&room_door_pair) {
                    if *door == (*way_in.get(&room).unwrap() + 2) % 4 {
                        continue;
                    }
                    new_door = true;
                    visited.push(room_door_pair);
                    last_direction = door.clone();
                    command = String::from(self.directions[last_direction]);
                    break;
                }
            }
            if !new_door {
                if *way_in.get(&room).unwrap() == 5 {
                    // assume that first room only has 1 door
                    command = String::from(self.directions[doors[0]]);
                    break;
                }
                command = String::from(self.directions[(*way_in.get(&room).unwrap() + 2) % 4]);
            }
        }
        (command, inventory, pressure_room_way_in)
    }

    fn find_password(&mut self) -> String {
        // navigate all rooms and pickup non-forbiden items
        let (command, inventory, pressure_room_way_in) = self.navigate_rooms("", 1000, true);
        let inventory: Vec<usize> = inventory
            .iter()
            .map(|item| self.get_item_index(&item))
            .collect();
        // go to Security Checkpoint
        self.navigate_rooms(&command, 0, false);
        // test combinations of items
        let mut current_inventory = inventory.clone();
        let combinations: Vec<Vec<usize>> = inventory.into_iter().combinations(4).collect();
        for new_inventory in combinations {
            for item in new_inventory.iter() {
                if !current_inventory.contains(&item) {
                    let command = self.create_take_command(*item);
                    self.run_command(&command);
                }
            }
            for item in current_inventory.iter() {
                if !new_inventory.contains(&item) {
                    let command = self.create_drop_command(*item);
                    self.run_command(&command);
                }
            }
            let output = self.run_command(&pressure_room_way_in);
            if let Some(cap) = self.password_regex.captures(&output) {
                return String::from(cap.name("password").unwrap().as_str());
            }
            current_inventory = new_inventory.iter().map(|i| *i).collect();
        }
        panic!("Password not found")
    }
}


fn solve(memory: &Vec<i64>) -> (String, String) {
    let mut crawler = Crawler::new(memory);
    (crawler.find_password(), String::default())
}

fn get_input(file_path: &String) -> Vec<i64> {
    std::fs::read_to_string(file_path)
        .expect("Error reading input file!")
        .split(',')
        .map(|i| i.trim().parse().unwrap())
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
    println!("Time: {:.7}", now.elapsed().as_secs_f32());
}
