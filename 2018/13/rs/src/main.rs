use num::complex::Complex;
use std::collections::HashMap;

type Position = Complex<i32>;
type Direction = Complex<i32>;
type Map = HashMap<Position, MapItem>;

#[derive(Copy, Clone)]
enum Orientation {
    Horizontal,
    Vertical,
}

enum MapItem {
    Straight(Orientation),
    Turn(Direction, Direction),
    Intersection,
}

struct Train {
    position: Position,
    direction: Direction,
    next_turn: Direction,
}

impl Train {
    fn new(position: Position, direction: Direction) -> Train {
        Train {
            position,
            direction,
            next_turn: Direction::new(0, 1),
        }
    }

    fn tick(&mut self) {
        self.position += self.direction;
    }

    fn turn(&mut self) {
        self.direction *= self.next_turn;
        let pair = (self.next_turn.re, self.next_turn.im);
        self.next_turn = match pair {
            (0, 1) => Direction::new(1, 0),
            (1, 0) => Direction::new(0, -1),
            (0, -1) => Direction::new(0, 1),
            _ => {
                panic!("Unexpected direction {}", self.direction)
            }
        }
    }

    fn clone(&self) -> Train {
        Train {
            position: self.position,
            direction: self.direction,
            next_turn: self.next_turn,
        }
    }
}

fn _show_map_area(map_items: &Map, start: Position, end: Position, trains: &Vec<&Train>) {
    println!("area {}, {}", start, end);
    let train_char: HashMap<Direction, char> = vec![
        (Direction::new(1, 0), '>'),
        (Direction::new(-1, 0), '<'),
        (Direction::new(0, 1), '^'),
        (Direction::new(0, -1), 'v'),
    ]
    .into_iter()
    .collect();
    let turn_char: HashMap<(Direction, Direction), char> = vec![
        ((Direction::new(1, 0), Direction::new(0, 1)), '\\'),
        ((Direction::new(1, 0), Direction::new(0, -1)), '/'),
        ((Direction::new(-1, 0), Direction::new(0, 1)), '/'),
        ((Direction::new(-1, 0), Direction::new(0, -1)), '\\'),
    ]
    .into_iter()
    .collect();
    for y in start.im..end.im {
        for x in start.re..end.re {
            let position = Complex::new(x, -y);
            let mut c = ' ';
            match map_items.get(&position) {
                Some(MapItem::Straight(orientation)) => {
                    c = match orientation {
                        Orientation::Horizontal => '-',
                        Orientation::Vertical => '|',
                    }
                }
                Some(MapItem::Intersection) => c = '+',
                Some(MapItem::Turn(horizontal, vertical)) => {
                    c = turn_char[&(*horizontal, *vertical)]
                }
                _ => {}
            }
            if let Some(train) = trains
                .iter()
                .filter(|train| train.position == position)
                .next()
            {
                c = train_char[&train.direction];
            }
            print!("{}", c);
        }
        println!();
    }
    println!();
}

fn _show_train(map_items: &Map, train: &Train, trains: &Vec<&Train>) {
    println!("train {}", train.position);
    let offset = 40;
    let max_x = map_items.keys().map(|p| p.re).max().unwrap();
    let max_y = map_items.keys().map(|p| -p.im).max().unwrap();
    let start_x = 0_i32.max(train.position.re - offset);
    let end_x = max_x.max(train.position.re + offset);
    let start_y = 0_i32.max(-train.position.im - offset);
    let end_y = max_y.max(-train.position.im + offset);
    _show_map_area(
        map_items,
        Position::new(start_x, start_y),
        Position::new(end_x, end_y),
        trains,
    );
}

fn _pause() {
    let mut input: String = String::new();
    std::io::stdin()
        .read_line(&mut input)
        .expect("error inputing");
}

fn position_to_string(position: &Position) -> String {
    String::from(format!("{},{}", position.re.abs(), position.im.abs()))
}

fn solve(data: &(Map, Vec<Train>)) -> (String, String) {
    let (map_items, trains) = data;
    let mut train_locations: HashMap<Position, Train> = trains
        .into_iter()
        .map(|train| (train.position, train.clone()))
        .collect();
    let mut part1_result = String::default();
    loop {
        let mut next_positions: Vec<Position> =
            train_locations.keys().map(|position| *position).collect();
        next_positions.sort_by_key(|position| (-position.im, position.re));
        for position in next_positions {
            if let Some(train) = train_locations.remove(&position) {
                let mut train = train;
                train.tick();
                match map_items.get(&train.position) {
                    Some(MapItem::Intersection) => train.turn(),
                    Some(MapItem::Turn(horizontal, vertical)) => {
                        train.direction = if train.direction.re != 0 {
                            *vertical
                        } else {
                            *horizontal
                        };
                    }
                    _ => {}
                }
                if train_locations.contains_key(&train.position) {
                    if part1_result == String::default() {
                        part1_result = position_to_string(&train.position);
                    }
                    train_locations.remove_entry(&train.position);
                } else {
                    train_locations.insert(train.position, train);
                }
            }
        }
        if train_locations.len() == 1 {
            return (
                part1_result,
                position_to_string(&train_locations.keys().next().unwrap()),
            );
        }
    }
}

fn get_input(file_path: &String) -> (Map, Vec<Train>) {
    let intersection = '+';
    let trains_chars: HashMap<char, Direction> = vec![
        ('>', Direction::new(1, 0)),
        ('<', Direction::new(-1, 0)),
        ('^', Direction::new(0, 1)),
        ('v', Direction::new(0, -1)),
    ]
    .into_iter()
    .collect();
    let turns = vec!['/', '\\'];
    let turns_directions: HashMap<String, (Direction, Direction)> = vec![
        (
            String::from(" /"),
            (Direction::new(1, 0), Direction::new(0, -1)),
        ),
        (
            String::from("-/"),
            (Direction::new(-1, 0), Direction::new(0, 1)),
        ),
        (
            String::from("+/"),
            (Direction::new(-1, 0), Direction::new(0, 1)),
        ),
        (
            String::from("-\\"),
            (Direction::new(-1, 0), Direction::new(0, -1)),
        ),
        (
            String::from("+\\"),
            (Direction::new(-1, 0), Direction::new(0, -1)),
        ),
        (
            String::from(" \\"),
            (Direction::new(1, 0), Direction::new(0, 1)),
        ),
    ]
    .into_iter()
    .collect();
    let straights: HashMap<char, Orientation> =
        vec![('-', Orientation::Horizontal), ('|', Orientation::Vertical)]
            .into_iter()
            .collect();
    let mut map = Map::new();
    let mut trains: Vec<Train> = Vec::new();
    let mut previous_c = ' ';
    let mut train_position_to_fill_in = Vec::new();
    for (y, line) in std::fs::read_to_string(file_path)
        .expect("Error reading input file!")
        .lines()
        .enumerate()
    {
        for (x, c) in line.chars().enumerate() {
            let position = Position::new(x as i32, -(y as i32));
            if c == intersection {
                map.insert(position, MapItem::Intersection);
            } else if let Some(orientation) = straights.get(&c) {
                map.insert(position, MapItem::Straight(*orientation));
            } else if turns.contains(&c) {
                if previous_c != '-' && previous_c != '+' {
                    previous_c = ' ';
                }
                let directions = turns_directions
                    .get(&format!("{}{}", previous_c, c))
                    .unwrap();
                map.insert(position, MapItem::Turn(directions.0, directions.1));
            } else if let Some(direction) = trains_chars.get(&c) {
                trains.push(Train::new(position, *direction));
                train_position_to_fill_in.push(position);
            }
            previous_c = c;
        }
    }
    let mut inserts = Vec::new();
    for position in train_position_to_fill_in {
        for direction in trains_chars.values() {
            match map.get(&(position + direction)) {
                Some(MapItem::Straight(orientation)) => {
                    inserts.push((position, MapItem::Straight(*orientation)))
                }
                Some(MapItem::Intersection) => inserts.push((
                    position,
                    MapItem::Straight(if direction.re > 0 {
                        Orientation::Horizontal
                    } else {
                        Orientation::Vertical
                    }),
                )),
                _ => {}
            }
        }
    }
    for (position, map_item) in inserts {
        map.insert(position, map_item);
    }
    (map, trains)
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
