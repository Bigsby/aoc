use regex::Regex;
use std::collections::HashMap;

type Point = num::Complex<i64>;
type PointPair = (Point, Point);

const CHARACTER_WIDTH: i64 = 6;
const CHARACTER_PADDING: i64 = 2;
const CHARACTER_HEIGHT: i64 = 10;

struct LetterMap {
    letters: HashMap<i64, char>,
}

impl LetterMap {
    fn get(&self, code: i64) -> Option<&char> {
        self.letters.get(&code)
    }

    fn new() -> LetterMap {
        LetterMap {
            letters: vec![
                (
                      (0b001100 << CHARACTER_WIDTH * 0)
                    + (0b010010 << CHARACTER_WIDTH * 1)
                    + (0b100001 << CHARACTER_WIDTH * 2)
                    + (0b100001 << CHARACTER_WIDTH * 3)
                    + (0b100001 << CHARACTER_WIDTH * 4)
                    + (0b111111 << CHARACTER_WIDTH * 5)
                    + (0b100001 << CHARACTER_WIDTH * 6)
                    + (0b100001 << CHARACTER_WIDTH * 7)
                    + (0b100001 << CHARACTER_WIDTH * 8)
                    + (0b100001 << CHARACTER_WIDTH * 9),
                    'A',
                ),
                (
                      (0b111110 << CHARACTER_WIDTH * 0)
                    + (0b100001 << CHARACTER_WIDTH * 1)
                    + (0b100001 << CHARACTER_WIDTH * 2)
                    + (0b100001 << CHARACTER_WIDTH * 3)
                    + (0b111110 << CHARACTER_WIDTH * 4)
                    + (0b100001 << CHARACTER_WIDTH * 5)
                    + (0b100001 << CHARACTER_WIDTH * 6)
                    + (0b100001 << CHARACTER_WIDTH * 7)
                    + (0b100001 << CHARACTER_WIDTH * 8)
                    + (0b111110 << CHARACTER_WIDTH * 9),
                    'B',
                ),
                (
                      (0b011110 << CHARACTER_WIDTH * 0)
                    + (0b100001 << CHARACTER_WIDTH * 1)
                    + (0b100000 << CHARACTER_WIDTH * 2)
                    + (0b100000 << CHARACTER_WIDTH * 3)
                    + (0b100000 << CHARACTER_WIDTH * 4)
                    + (0b100000 << CHARACTER_WIDTH * 5)
                    + (0b100000 << CHARACTER_WIDTH * 6)
                    + (0b100000 << CHARACTER_WIDTH * 7)
                    + (0b100001 << CHARACTER_WIDTH * 8)
                    + (0b011110 << CHARACTER_WIDTH * 9),
                    'C',
                ),
                (
                      (0b111110 << CHARACTER_WIDTH * 0)
                    + (0b100001 << CHARACTER_WIDTH * 1)
                    + (0b100001 << CHARACTER_WIDTH * 2)
                    + (0b100001 << CHARACTER_WIDTH * 3)
                    + (0b100001 << CHARACTER_WIDTH * 4)
                    + (0b100001 << CHARACTER_WIDTH * 5)
                    + (0b100001 << CHARACTER_WIDTH * 6)
                    + (0b100001 << CHARACTER_WIDTH * 7)
                    + (0b100001 << CHARACTER_WIDTH * 8)
                    + (0b111110 << CHARACTER_WIDTH * 9),
                    'D',
                ),
                (
                      (0b111111 << CHARACTER_WIDTH * 0)
                    + (0b100000 << CHARACTER_WIDTH * 1)
                    + (0b100000 << CHARACTER_WIDTH * 2)
                    + (0b100000 << CHARACTER_WIDTH * 3)
                    + (0b111110 << CHARACTER_WIDTH * 4)
                    + (0b100000 << CHARACTER_WIDTH * 5)
                    + (0b100000 << CHARACTER_WIDTH * 6)
                    + (0b100000 << CHARACTER_WIDTH * 7)
                    + (0b100000 << CHARACTER_WIDTH * 8)
                    + (0b111111 << CHARACTER_WIDTH * 9),
                    'E',
                ),
                (
                      (0b111111 << CHARACTER_WIDTH * 0)
                    + (0b100000 << CHARACTER_WIDTH * 1)
                    + (0b100000 << CHARACTER_WIDTH * 2)
                    + (0b100000 << CHARACTER_WIDTH * 3)
                    + (0b111110 << CHARACTER_WIDTH * 4)
                    + (0b100000 << CHARACTER_WIDTH * 5)
                    + (0b100000 << CHARACTER_WIDTH * 6)
                    + (0b100000 << CHARACTER_WIDTH * 7)
                    + (0b100000 << CHARACTER_WIDTH * 8)
                    + (0b100000 << CHARACTER_WIDTH * 9),
                    'F',
                ),
                (
                      (0b011110 << CHARACTER_WIDTH * 0)
                    + (0b100001 << CHARACTER_WIDTH * 1)
                    + (0b100000 << CHARACTER_WIDTH * 2)
                    + (0b100000 << CHARACTER_WIDTH * 3)
                    + (0b100000 << CHARACTER_WIDTH * 4)
                    + (0b100111 << CHARACTER_WIDTH * 5)
                    + (0b100001 << CHARACTER_WIDTH * 6)
                    + (0b100001 << CHARACTER_WIDTH * 7)
                    + (0b100011 << CHARACTER_WIDTH * 8)
                    + (0b011101 << CHARACTER_WIDTH * 9),
                    'G',
                ),
                (
                      (0b100001 << CHARACTER_WIDTH * 0)
                    + (0b100001 << CHARACTER_WIDTH * 1)
                    + (0b100001 << CHARACTER_WIDTH * 2)
                    + (0b100001 << CHARACTER_WIDTH * 3)
                    + (0b111111 << CHARACTER_WIDTH * 4)
                    + (0b100001 << CHARACTER_WIDTH * 5)
                    + (0b100001 << CHARACTER_WIDTH * 6)
                    + (0b100001 << CHARACTER_WIDTH * 7)
                    + (0b100001 << CHARACTER_WIDTH * 8)
                    + (0b100001 << CHARACTER_WIDTH * 9),
                    'H',
                ),
                (
                      (0b111000 << CHARACTER_WIDTH * 0)
                    + (0b010000 << CHARACTER_WIDTH * 1)
                    + (0b010000 << CHARACTER_WIDTH * 2)
                    + (0b010000 << CHARACTER_WIDTH * 3)
                    + (0b010000 << CHARACTER_WIDTH * 4)
                    + (0b010000 << CHARACTER_WIDTH * 5)
                    + (0b010000 << CHARACTER_WIDTH * 6)
                    + (0b010000 << CHARACTER_WIDTH * 7)
                    + (0b010000 << CHARACTER_WIDTH * 8)
                    + (0b111000 << CHARACTER_WIDTH * 9),
                    'I',
                ), // Not sure
                (
                      (0b000111 << CHARACTER_WIDTH * 0)
                    + (0b000010 << CHARACTER_WIDTH * 1)
                    + (0b000010 << CHARACTER_WIDTH * 2)
                    + (0b000010 << CHARACTER_WIDTH * 3)
                    + (0b000010 << CHARACTER_WIDTH * 4)
                    + (0b000010 << CHARACTER_WIDTH * 5)
                    + (0b000010 << CHARACTER_WIDTH * 6)
                    + (0b100010 << CHARACTER_WIDTH * 7)
                    + (0b100010 << CHARACTER_WIDTH * 8)
                    + (0b011100 << CHARACTER_WIDTH * 9),
                    'J',
                ),
                (
                      (0b100001 << CHARACTER_WIDTH * 0)
                    + (0b100010 << CHARACTER_WIDTH * 1)
                    + (0b100100 << CHARACTER_WIDTH * 2)
                    + (0b101000 << CHARACTER_WIDTH * 3)
                    + (0b110000 << CHARACTER_WIDTH * 4)
                    + (0b110000 << CHARACTER_WIDTH * 5)
                    + (0b101000 << CHARACTER_WIDTH * 6)
                    + (0b100100 << CHARACTER_WIDTH * 7)
                    + (0b100010 << CHARACTER_WIDTH * 8)
                    + (0b100001 << CHARACTER_WIDTH * 9),
                    'K',
                ),
                (
                      (0b100000 << CHARACTER_WIDTH * 0)
                    + (0b100000 << CHARACTER_WIDTH * 1)
                    + (0b100000 << CHARACTER_WIDTH * 2)
                    + (0b100000 << CHARACTER_WIDTH * 3)
                    + (0b100000 << CHARACTER_WIDTH * 4)
                    + (0b100000 << CHARACTER_WIDTH * 5)
                    + (0b100000 << CHARACTER_WIDTH * 6)
                    + (0b100000 << CHARACTER_WIDTH * 7)
                    + (0b100000 << CHARACTER_WIDTH * 8)
                    + (0b111111 << CHARACTER_WIDTH * 9),
                    'L',
                ),
                (
                      (0b100001 << CHARACTER_WIDTH * 0)
                    + (0b110011 << CHARACTER_WIDTH * 1)
                    + (0b110011 << CHARACTER_WIDTH * 2)
                    + (0b101101 << CHARACTER_WIDTH * 3)
                    + (0b100001 << CHARACTER_WIDTH * 4)
                    + (0b100001 << CHARACTER_WIDTH * 5)
                    + (0b100001 << CHARACTER_WIDTH * 6)
                    + (0b100001 << CHARACTER_WIDTH * 7)
                    + (0b100001 << CHARACTER_WIDTH * 8)
                    + (0b100001 << CHARACTER_WIDTH * 9),
                    'M',
                ), // Not sure
                (
                      (0b100001 << CHARACTER_WIDTH * 0)
                    + (0b110001 << CHARACTER_WIDTH * 1)
                    + (0b110001 << CHARACTER_WIDTH * 2)
                    + (0b101001 << CHARACTER_WIDTH * 3)
                    + (0b101001 << CHARACTER_WIDTH * 4)
                    + (0b100101 << CHARACTER_WIDTH * 5)
                    + (0b100101 << CHARACTER_WIDTH * 6)
                    + (0b100011 << CHARACTER_WIDTH * 7)
                    + (0b100011 << CHARACTER_WIDTH * 8)
                    + (0b100001 << CHARACTER_WIDTH * 9),
                    'N',
                ),
                (
                      (0b011110 << CHARACTER_WIDTH * 0)
                    + (0b100001 << CHARACTER_WIDTH * 1)
                    + (0b100001 << CHARACTER_WIDTH * 2)
                    + (0b100001 << CHARACTER_WIDTH * 3)
                    + (0b100001 << CHARACTER_WIDTH * 4)
                    + (0b100001 << CHARACTER_WIDTH * 5)
                    + (0b100001 << CHARACTER_WIDTH * 6)
                    + (0b100001 << CHARACTER_WIDTH * 7)
                    + (0b100001 << CHARACTER_WIDTH * 8)
                    + (0b011110 << CHARACTER_WIDTH * 9),
                    'O',
                ),
                (
                      (0b111110 << CHARACTER_WIDTH * 0)
                    + (0b100001 << CHARACTER_WIDTH * 1)
                    + (0b100001 << CHARACTER_WIDTH * 2)
                    + (0b100001 << CHARACTER_WIDTH * 3)
                    + (0b111110 << CHARACTER_WIDTH * 4)
                    + (0b100000 << CHARACTER_WIDTH * 5)
                    + (0b100000 << CHARACTER_WIDTH * 6)
                    + (0b100000 << CHARACTER_WIDTH * 7)
                    + (0b100000 << CHARACTER_WIDTH * 8)
                    + (0b100000 << CHARACTER_WIDTH * 9),
                    'P',
                ),
                (
                      (0b011110 << CHARACTER_WIDTH * 0)
                    + (0b100001 << CHARACTER_WIDTH * 1)
                    + (0b100001 << CHARACTER_WIDTH * 2)
                    + (0b100001 << CHARACTER_WIDTH * 3)
                    + (0b100001 << CHARACTER_WIDTH * 4)
                    + (0b100001 << CHARACTER_WIDTH * 5)
                    + (0b100001 << CHARACTER_WIDTH * 6)
                    + (0b100101 << CHARACTER_WIDTH * 7)
                    + (0b100110 << CHARACTER_WIDTH * 8)
                    + (0b011001 << CHARACTER_WIDTH * 9),
                    'Q',
                ), // Not sure
                (
                      (0b111110 << CHARACTER_WIDTH * 0)
                    + (0b100001 << CHARACTER_WIDTH * 1)
                    + (0b100001 << CHARACTER_WIDTH * 2)
                    + (0b100001 << CHARACTER_WIDTH * 3)
                    + (0b111110 << CHARACTER_WIDTH * 4)
                    + (0b100100 << CHARACTER_WIDTH * 5)
                    + (0b100010 << CHARACTER_WIDTH * 6)
                    + (0b100010 << CHARACTER_WIDTH * 7)
                    + (0b100001 << CHARACTER_WIDTH * 8)
                    + (0b100001 << CHARACTER_WIDTH * 9),
                    'R',
                ),
                (
                      (0b011110 << CHARACTER_WIDTH * 0)
                    + (0b100001 << CHARACTER_WIDTH * 1)
                    + (0b100000 << CHARACTER_WIDTH * 2)
                    + (0b100000 << CHARACTER_WIDTH * 3)
                    + (0b011110 << CHARACTER_WIDTH * 4)
                    + (0b000001 << CHARACTER_WIDTH * 5)
                    + (0b000001 << CHARACTER_WIDTH * 6)
                    + (0b000001 << CHARACTER_WIDTH * 7)
                    + (0b100001 << CHARACTER_WIDTH * 8)
                    + (0b011110 << CHARACTER_WIDTH * 9),
                    'S',
                ),
                (
                      (0b111110 << CHARACTER_WIDTH * 0)
                    + (0b001000 << CHARACTER_WIDTH * 1)
                    + (0b001000 << CHARACTER_WIDTH * 2)
                    + (0b001000 << CHARACTER_WIDTH * 3)
                    + (0b001000 << CHARACTER_WIDTH * 4)
                    + (0b001000 << CHARACTER_WIDTH * 5)
                    + (0b001000 << CHARACTER_WIDTH * 6)
                    + (0b001000 << CHARACTER_WIDTH * 7)
                    + (0b001000 << CHARACTER_WIDTH * 8)
                    + (0b001000 << CHARACTER_WIDTH * 9),
                    'T',
                ), // Not sure
                (
                      (0b100001 << CHARACTER_WIDTH * 0)
                    + (0b100001 << CHARACTER_WIDTH * 1)
                    + (0b100001 << CHARACTER_WIDTH * 2)
                    + (0b100001 << CHARACTER_WIDTH * 3)
                    + (0b100001 << CHARACTER_WIDTH * 4)
                    + (0b100001 << CHARACTER_WIDTH * 5)
                    + (0b100001 << CHARACTER_WIDTH * 6)
                    + (0b100001 << CHARACTER_WIDTH * 7)
                    + (0b100001 << CHARACTER_WIDTH * 8)
                    + (0b011110 << CHARACTER_WIDTH * 9),
                    'U',
                ),
                (
                      (0b100001 << CHARACTER_WIDTH * 0)
                    + (0b100001 << CHARACTER_WIDTH * 1)
                    + (0b100001 << CHARACTER_WIDTH * 2)
                    + (0b100001 << CHARACTER_WIDTH * 3)
                    + (0b100001 << CHARACTER_WIDTH * 4)
                    + (0b100001 << CHARACTER_WIDTH * 5)
                    + (0b100001 << CHARACTER_WIDTH * 6)
                    + (0b010010 << CHARACTER_WIDTH * 7)
                    + (0b010010 << CHARACTER_WIDTH * 8)
                    + (0b001100 << CHARACTER_WIDTH * 9),
                    'V',
                ), // Not sure
                (
                      (0b100001 << CHARACTER_WIDTH * 0)
                    + (0b100001 << CHARACTER_WIDTH * 1)
                    + (0b100001 << CHARACTER_WIDTH * 2)
                    + (0b100001 << CHARACTER_WIDTH * 3)
                    + (0b100001 << CHARACTER_WIDTH * 4)
                    + (0b100001 << CHARACTER_WIDTH * 5)
                    + (0b101101 << CHARACTER_WIDTH * 6)
                    + (0b101101 << CHARACTER_WIDTH * 7)
                    + (0b110011 << CHARACTER_WIDTH * 8)
                    + (0b100001 << CHARACTER_WIDTH * 9),
                    'W',
                ), // Not sure
                (
                      (0b100001 << CHARACTER_WIDTH * 0)
                    + (0b100001 << CHARACTER_WIDTH * 1)
                    + (0b010010 << CHARACTER_WIDTH * 2)
                    + (0b010010 << CHARACTER_WIDTH * 3)
                    + (0b001100 << CHARACTER_WIDTH * 4)
                    + (0b001100 << CHARACTER_WIDTH * 5)
                    + (0b010010 << CHARACTER_WIDTH * 6)
                    + (0b010010 << CHARACTER_WIDTH * 7)
                    + (0b100001 << CHARACTER_WIDTH * 8)
                    + (0b100001 << CHARACTER_WIDTH * 9),
                    'X',
                ),
                (
                      (0b100010 << CHARACTER_WIDTH * 0)
                    + (0b100010 << CHARACTER_WIDTH * 1)
                    + (0b010100 << CHARACTER_WIDTH * 2)
                    + (0b010100 << CHARACTER_WIDTH * 3)
                    + (0b001000 << CHARACTER_WIDTH * 4)
                    + (0b001000 << CHARACTER_WIDTH * 5)
                    + (0b001000 << CHARACTER_WIDTH * 6)
                    + (0b001000 << CHARACTER_WIDTH * 7)
                    + (0b001000 << CHARACTER_WIDTH * 8)
                    + (0b001000 << CHARACTER_WIDTH * 9),
                    'Y',
                ), // Not sure
                (
                      (0b111111 << CHARACTER_WIDTH * 0)
                    + (0b000001 << CHARACTER_WIDTH * 1)
                    + (0b000001 << CHARACTER_WIDTH * 2)
                    + (0b000010 << CHARACTER_WIDTH * 3)
                    + (0b000100 << CHARACTER_WIDTH * 4)
                    + (0b001000 << CHARACTER_WIDTH * 5)
                    + (0b010000 << CHARACTER_WIDTH * 6)
                    + (0b100000 << CHARACTER_WIDTH * 7)
                    + (0b100000 << CHARACTER_WIDTH * 8)
                    + (0b111111 << CHARACTER_WIDTH * 9),
                    'Z',
                ),
            ]
            .into_iter()
            .collect::<HashMap<i64, char>>(),
        }
    }
}

fn get_dimensions(points: &Vec<PointPair>) -> ((i64, i64), i64, i64, i64, i64) {
    let min_x = points.into_iter().map(|point| point.0.re).min().unwrap();
    let max_x = points.into_iter().map(|point| point.0.re).max().unwrap();
    let min_y = points.into_iter().map(|point| point.0.im).min().unwrap();
    let max_y = points.into_iter().map(|point| point.0.im).max().unwrap();
    return (
        (i64::abs(max_x - min_x + 1), i64::abs(max_y - min_y + 1)),
        min_x,
        max_x,
        min_y,
        max_y,
    );
}

fn get_character(
    min_x: i64,
    min_y: i64,
    index: i64,
    character_width: i64,
    points: &Vec<Point>,
    letter_map: &LetterMap,
) -> Option<char> {
    let mut screen_value = 0;
    for x in 0..character_width {
        for y in 0..CHARACTER_HEIGHT {
            if points.contains(&Point::new(character_width * index + x + min_x, y + min_y)) {
                screen_value +=
                    i64::pow(2, (CHARACTER_WIDTH - 1 - x) as u32) << (y * CHARACTER_WIDTH);
            }
        }
    }
    if let Some(character) = letter_map.get(screen_value) {
        Some(*character)
    } else {
        None
    }
}

fn get_message(points: &Vec<PointPair>, letter_map: &LetterMap) -> Option<String> {
    let ((width, _), min_x, _, min_y, _) = get_dimensions(&points);
    let points: Vec<Point> = points.into_iter().map(|pair| pair.0).collect();
    let character_width = CHARACTER_WIDTH + CHARACTER_PADDING;

    let mut message = String::from("");
    for index in 0..(width / character_width) + 1 {
        if let Some(character) =
            get_character(min_x, min_y, index, character_width, &points, letter_map)
        {
            message.push(character);
        } else {
            return None;
        }
    }
    Some(message)
}

fn get_next_state(points: Vec<PointPair>) -> Vec<PointPair> {
    let mut new_state = Vec::new();
    for (point, velocity) in points {
        new_state.push((point + velocity, velocity));
    }
    new_state
}

fn _print_points(points: &Vec<PointPair>) {
    let (_, min_x, max_x, min_y, max_y) = get_dimensions(points);
    let points: Vec<Point> = points.into_iter().map(|pair| pair.0).collect();
    for y in min_y..max_y + 1 {
        for x in min_x..max_x + 1 {
            if points.contains(&Point::new(x, y)) {
                print!("#")
            } else {
                print!(".")
            }
        }
        println!("")
    }
    println!("")
}

fn solve(points: &Vec<PointPair>) -> (String, usize) {
    let mut iterations = 0;
    let mut points = points.clone();
    let letter_map = LetterMap::new();
    loop {
        let ((_, height), _, _, _, _) = get_dimensions(&points);
        if height == CHARACTER_HEIGHT {
            if let Some(message) = get_message(&points, &letter_map) {
                return (message, iterations);
            }
        }
        iterations += 1;
        points = get_next_state(points);
    }
}

fn get_input(file_path: &String) -> Vec<PointPair> {
    let line_regex = Regex::new(
        r"^position=<\s?(?P<positionX>-?\d+),\s+(?P<positionY>-?\d+)>\svelocity=<\s?(?P<velocityX>-?\d+),\s+?(?P<velocityY>-?\d+)>$").unwrap();
    std::fs::read_to_string(file_path)
        .expect("Error reading input file!")
        .lines()
        .map(|line| {
            line_regex
                .captures(line)
                .map(|cap| {
                    (
                        Point::new(
                            cap.name("positionX").unwrap().as_str().parse().unwrap(),
                            cap.name("positionY").unwrap().as_str().parse().unwrap(),
                        ),
                        Point::new(
                            cap.name("velocityX").unwrap().as_str().parse().unwrap(),
                            cap.name("velocityY").unwrap().as_str().parse().unwrap(),
                        ),
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
    println!("P2: {}", part2_result);
    println!();
    println!("Time: {:.7}", end);
}
