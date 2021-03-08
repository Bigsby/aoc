use num::complex::Complex;
use std::collections::HashMap;

const IMAGE_WIDTH: u32 = 25;
const IMAGE_HEIGHT: u32 = 6;
const CHARACTER_WIDTH: u32 = 5;
const PIXELS_PER_LAYER: u32 = IMAGE_WIDTH * IMAGE_HEIGHT;

struct LetterMap {
    letters: HashMap<u32, char>,
}

impl LetterMap {
    fn new() -> LetterMap {
        LetterMap {
            letters: vec![
                (
                      (0b01100 << CHARACTER_WIDTH * 0)
                    + (0b10010 << CHARACTER_WIDTH * 1)
                    + (0b10010 << CHARACTER_WIDTH * 2)
                    + (0b11110 << CHARACTER_WIDTH * 3)
                    + (0b10010 << CHARACTER_WIDTH * 4)
                    + (0b10010 << CHARACTER_WIDTH * 5),
                    'A',
                ),
                (
                      (0b11100 << CHARACTER_WIDTH * 0)
                    + (0b10010 << CHARACTER_WIDTH * 1)
                    + (0b11100 << CHARACTER_WIDTH * 2)
                    + (0b10010 << CHARACTER_WIDTH * 3)
                    + (0b10010 << CHARACTER_WIDTH * 4)
                    + (0b11100 << CHARACTER_WIDTH * 5),
                    'B',
                ),
                (
                      (0b01100 << CHARACTER_WIDTH * 0)
                    + (0b10010 << CHARACTER_WIDTH * 1)
                    + (0b10000 << CHARACTER_WIDTH * 2)
                    + (0b10000 << CHARACTER_WIDTH * 3)
                    + (0b10010 << CHARACTER_WIDTH * 4)
                    + (0b01100 << CHARACTER_WIDTH * 5),
                    'C',
                ),
                (
                      (0b11100 << CHARACTER_WIDTH * 0)
                    + (0b10010 << CHARACTER_WIDTH * 1)
                    + (0b10010 << CHARACTER_WIDTH * 2)
                    + (0b10010 << CHARACTER_WIDTH * 3)
                    + (0b10010 << CHARACTER_WIDTH * 4)
                    + (0b11100 << CHARACTER_WIDTH * 5),
                    'D',
                ),
                (
                      (0b11110 << CHARACTER_WIDTH * 0)
                    + (0b10000 << CHARACTER_WIDTH * 1)
                    + (0b11100 << CHARACTER_WIDTH * 2)
                    + (0b10000 << CHARACTER_WIDTH * 3)
                    + (0b10000 << CHARACTER_WIDTH * 4)
                    + (0b11110 << CHARACTER_WIDTH * 5),
                    'E',
                ),
                (
                      (0b11110 << CHARACTER_WIDTH * 0)
                    + (0b10000 << CHARACTER_WIDTH * 1)
                    + (0b11100 << CHARACTER_WIDTH * 2)
                    + (0b10000 << CHARACTER_WIDTH * 3)
                    + (0b10000 << CHARACTER_WIDTH * 4)
                    + (0b10000 << CHARACTER_WIDTH * 5),
                    'F',
                ),
                (
                      (0b01100 << CHARACTER_WIDTH * 0)
                    + (0b10010 << CHARACTER_WIDTH * 1)
                    + (0b10000 << CHARACTER_WIDTH * 2)
                    + (0b10110 << CHARACTER_WIDTH * 3)
                    + (0b10010 << CHARACTER_WIDTH * 4)
                    + (0b01110 << CHARACTER_WIDTH * 5),
                    'G',
                ),
                (
                      (0b10010 << CHARACTER_WIDTH * 0)
                    + (0b10010 << CHARACTER_WIDTH * 1)
                    + (0b11110 << CHARACTER_WIDTH * 2)
                    + (0b10010 << CHARACTER_WIDTH * 3)
                    + (0b10010 << CHARACTER_WIDTH * 4)
                    + (0b10010 << CHARACTER_WIDTH * 5),
                    'H',
                ),
                (
                      (0b01110 << CHARACTER_WIDTH * 0)
                    + (0b00100 << CHARACTER_WIDTH * 1)
                    + (0b00100 << CHARACTER_WIDTH * 2)
                    + (0b00100 << CHARACTER_WIDTH * 3)
                    + (0b00100 << CHARACTER_WIDTH * 4)
                    + (0b01110 << CHARACTER_WIDTH * 5),
                    'I',
                ),
                (
                      (0b00110 << CHARACTER_WIDTH * 0)
                    + (0b00010 << CHARACTER_WIDTH * 1)
                    + (0b00010 << CHARACTER_WIDTH * 2)
                    + (0b00010 << CHARACTER_WIDTH * 3)
                    + (0b10010 << CHARACTER_WIDTH * 4)
                    + (0b01100 << CHARACTER_WIDTH * 5),
                    'J',
                ),
                (
                      (0b10010 << CHARACTER_WIDTH * 0)
                    + (0b10100 << CHARACTER_WIDTH * 1)
                    + (0b11000 << CHARACTER_WIDTH * 2)
                    + (0b10100 << CHARACTER_WIDTH * 3)
                    + (0b10100 << CHARACTER_WIDTH * 4)
                    + (0b10010 << CHARACTER_WIDTH * 5),
                    'K',
                ),
                (
                      (0b10000 << CHARACTER_WIDTH * 0)
                    + (0b10000 << CHARACTER_WIDTH * 1)
                    + (0b10000 << CHARACTER_WIDTH * 2)
                    + (0b10000 << CHARACTER_WIDTH * 3)
                    + (0b10000 << CHARACTER_WIDTH * 4)
                    + (0b11110 << CHARACTER_WIDTH * 5),
                    'L',
                ),
                (
                      (0b01100 << CHARACTER_WIDTH * 0)
                    + (0b10010 << CHARACTER_WIDTH * 1)
                    + (0b10010 << CHARACTER_WIDTH * 2)
                    + (0b10010 << CHARACTER_WIDTH * 3)
                    + (0b10010 << CHARACTER_WIDTH * 4)
                    + (0b01100 << CHARACTER_WIDTH * 5),
                    'O',
                ),
                (
                      (0b11100 << CHARACTER_WIDTH * 0)
                    + (0b10010 << CHARACTER_WIDTH * 1)
                    + (0b10010 << CHARACTER_WIDTH * 2)
                    + (0b11100 << CHARACTER_WIDTH * 3)
                    + (0b10000 << CHARACTER_WIDTH * 4)
                    + (0b10000 << CHARACTER_WIDTH * 5),
                    'P',
                ),
                (
                      (0b11100 << CHARACTER_WIDTH * 0)
                    + (0b10010 << CHARACTER_WIDTH * 1)
                    + (0b10010 << CHARACTER_WIDTH * 2)
                    + (0b11100 << CHARACTER_WIDTH * 3)
                    + (0b10100 << CHARACTER_WIDTH * 4)
                    + (0b10010 << CHARACTER_WIDTH * 5),
                    'R',
                ),
                (
                      (0b01110 << CHARACTER_WIDTH * 0)
                    + (0b10000 << CHARACTER_WIDTH * 1)
                    + (0b10000 << CHARACTER_WIDTH * 2)
                    + (0b01100 << CHARACTER_WIDTH * 3)
                    + (0b00010 << CHARACTER_WIDTH * 4)
                    + (0b11100 << CHARACTER_WIDTH * 5),
                    'S',
                ),
                (
                      (0b10010 << CHARACTER_WIDTH * 0)
                    + (0b10010 << CHARACTER_WIDTH * 1)
                    + (0b10010 << CHARACTER_WIDTH * 2)
                    + (0b10010 << CHARACTER_WIDTH * 3)
                    + (0b10010 << CHARACTER_WIDTH * 4)
                    + (0b01100 << CHARACTER_WIDTH * 5),
                    'U',
                ),
                (
                      (0b10001 << CHARACTER_WIDTH * 0)
                    + (0b10001 << CHARACTER_WIDTH * 1)
                    + (0b01010 << CHARACTER_WIDTH * 2)
                    + (0b00100 << CHARACTER_WIDTH * 3)
                    + (0b00100 << CHARACTER_WIDTH * 4)
                    + (0b00100 << CHARACTER_WIDTH * 5),
                    'Y',
                ),
                (
                      (0b11110 << CHARACTER_WIDTH * 0)
                    + (0b00010 << CHARACTER_WIDTH * 1)
                    + (0b00100 << CHARACTER_WIDTH * 2)
                    + (0b01000 << CHARACTER_WIDTH * 3)
                    + (0b10000 << CHARACTER_WIDTH * 4)
                    + (0b11110 << CHARACTER_WIDTH * 5),
                    'Z',
                ),
            ]
            .into_iter()
            .collect::<HashMap<u32, char>>(),
        }
    }
    fn get(&self, code: u32) -> char {
        *self.letters.get(&code).unwrap()
    }
}

fn get_image_layers(pixels: &Vec<u32>) -> Vec<Vec<u32>> {
    let pixels_per_layer = PIXELS_PER_LAYER as usize;
    let layer_count = pixels.len() / pixels_per_layer;
    (0..layer_count)
        .into_iter()
        .map(|layer_index| {
            pixels[(layer_index * pixels_per_layer)..(pixels_per_layer * (layer_index + 1))]
                .iter()
                .map(|pixel| *pixel)
                .collect()
        })
        .collect()
}

fn part1(layers: &Vec<Vec<u32>>) -> usize {
    let mut least_zeros = usize::MAX;
    let mut result = 0;
    for layer in layers {
        let zero_count = layer.iter().filter(|pixel| **pixel == 0).count();
        if zero_count < least_zeros {
            least_zeros = zero_count;
            result = layer.iter().filter(|pixel| **pixel == 1).count()
                * layer.iter().filter(|pixel| **pixel == 2).count()
        }
    }
    result
}

const _BLACK: u32 = 0;
const WHITE: u32 = 1;
const TRANSPARENT: u32 = 2;

fn get_character_in_screen(
    screen: &HashMap<Complex<u32>, u32>,
    index: u32,
    width: u32,
    height: u32,
    letter_map: &LetterMap,
) -> char {
    let mut screen_value = 0;
    for x in 0..width {
        for y in 0..height {
            if screen.get(&Complex::new(width * index + x, y)).unwrap() == &WHITE {
                screen_value += u32::pow(2, width - 1 - x) << (y * width);
            }
        }
    }
    letter_map.get(screen_value)
}

fn part2(layers: &Vec<Vec<u32>>) -> String {
    let letter_map = LetterMap::new();
    let mut image = (0..(IMAGE_WIDTH * IMAGE_HEIGHT))
        .into_iter()
        .map(|index| {
            (
                Complex::new(index % IMAGE_WIDTH, index / IMAGE_WIDTH),
                TRANSPARENT,
            )
        })
        .collect::<HashMap<Complex<u32>, u32>>();
    for layer in layers {
        for x in 0..IMAGE_WIDTH {
            for y in 0..IMAGE_HEIGHT {
                let pixel = Complex::new(x, y);
                if image.get(&pixel).unwrap() < &2 {
                    continue;
                }
                *image.get_mut(&pixel).unwrap() = layer[(x + y * IMAGE_WIDTH) as usize];
            }
        }
    }
    (0..(IMAGE_WIDTH / CHARACTER_WIDTH))
        .into_iter()
        .map(|index| {
            get_character_in_screen(&image, index, CHARACTER_WIDTH, IMAGE_HEIGHT, &letter_map)
        })
        .collect::<String>()
}

fn solve(pixels: &Vec<u32>) -> (usize, String) {
    let layers = get_image_layers(pixels);
    (part1(&layers), part2(&layers))
}

fn get_input(file_path: &String) -> Vec<u32> {
    std::fs::read_to_string(file_path)
        .expect("Error reading input file!")
        .chars()
        .map(|i| i.to_digit(10).unwrap())
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
