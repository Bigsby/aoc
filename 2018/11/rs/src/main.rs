type Grid = [i32; GRID_SIZE * GRID_SIZE];

const GRID_SIZE: usize = 300;

fn get_index(x: usize, y: usize) -> usize {
    y * GRID_SIZE + x
}
// def get_index(x: int, y: int) -> int:
//     return y * GRID_SIZE + x

fn calculate_power_level(x: usize, y: usize, serial_number: i32) -> i32 {
    let x = x as i32;
    let y = y as i32;
    let rack_id = x + 10;
    let mut power_level = rack_id * y;
    power_level += serial_number;
    power_level *= rack_id;
    power_level = power_level % 1000 / 100;
    power_level - 5
}
// def calculate_power_level(x: int, y: int, serial_number: int) -> int:
//     rack_id = x + 10
//     power_level = rack_id * y
//     power_level += serial_number
//     power_level *= rack_id
//     power_level = power_level % 1000 // 100
//     return power_level - 5

// def build_grid(serial_number: int) -> Grid:
//     return [calculate_power_level(x + 1, y + 1, serial_number)
//         for x, y in product(range(GRID_SIZE), range(GRID_SIZE))]

fn build_grid(serial_number: i32) -> Grid {
    let mut grid = [0; GRID_SIZE * GRID_SIZE];
    for y in 0..GRID_SIZE {
        for x in 0..GRID_SIZE {
            grid[get_index(x, y)] = calculate_power_level(x + 1, y + 1, serial_number);
        }
    }
    grid
}

// def build_summed_area_table(grid: Grid) -> Grid:
//     for y in range(GRID_SIZE):
//         for x in range(GRID_SIZE):
//             grid[get_index(x, y)] = \
//                   grid[get_index(x    , y    )] + \
//                 ( grid[get_index(x - 1, y    )] if x > 0 else 0) + \
//                 ( grid[get_index(x    , y - 1)] if y > 0 else 0) + \
//                 (-grid[get_index(x - 1, y - 1)] if x > 0 and y > 0 else 0)
//     return grid

fn build_summed_area_table(grid: Grid) -> Grid {
    let mut grid = grid.clone();
    for x in 0..GRID_SIZE {
        for y in 0..GRID_SIZE {
            grid[get_index(x, y)] = 
                              grid[get_index(x    , y    )]
                + (if x > 0 { grid[get_index(x - 1, y    )] } else { 0 })
                + (if y > 0 { grid[get_index(x    , y - 1)] } else { 0 })
                + (if x > 0 && y > 0 {
                             -grid[get_index(x - 1, y - 1)]
                } else {
                    0
                })
        }
    }
    grid
}

fn sum_from_area_table(grid: &Grid, x: usize, y: usize, size: usize) -> i32 {
          grid[get_index(x - 1       , y - 1)]
        - grid[get_index(x - 1 + size, y - 1)]
        - grid[get_index(x - 1       , y - 1 + size)]
        + grid[get_index(x - 1 + size, y - 1 + size)]
}

// def sum_from_area_table(grid: Grid, x: int, y: int, size: int) -> int:
//     return grid[get_index(x - 1       , y - 1       )] \
//          - grid[get_index(x - 1 + size, y - 1       )] \
//          - grid[get_index(x - 1       , y - 1 + size)] \
//          + grid[get_index(x - 1 + size, y - 1 + size)]

// def solve(serial_number: int) -> Tuple[str, str]:
//     grid = build_grid(serial_number)
//     summed_area_table = build_summed_area_table(grid)
//     max_fuel = max_size = 0
//     max_cell = (-1, -1)
//     max3_cell = (-1, -1)
//     max3_fuel = 0
//     for size in range(1, GRID_SIZE):
//         for y, x in product(range(1, GRID_SIZE - size), range(1, GRID_SIZE - size)):
//             fuel = sum_from_area_table(summed_area_table, x, y, size)
//             if fuel > max_fuel:
//                 max_fuel = fuel
//                 max_cell = x + 1, y + 1
//                 max_size = size
//             if size == 3 and fuel > max3_fuel:
//                 max3_fuel = fuel
//                 max3_cell = x + 1, y + 1
//     return f"{max3_cell[0]},{max3_cell[1]}", f"{max_cell[0]},{max_cell[1]},{max_size}"


fn solve(serial_number: &i32) -> (String, String) {
    let grid = build_grid(*serial_number);
    let summed_area_table = build_summed_area_table(grid);
    let mut max_fuel = 0;
    let mut max_size = 0;
    let mut max_cell = (0, 0);
    let mut max3_cell = (0, 0);
    let mut max3_fuel = 0;
    for size in 1..GRID_SIZE {
        for x in 1..GRID_SIZE - size {
            for y in 1..GRID_SIZE - size {
                let fuel = sum_from_area_table(&summed_area_table, x, y, size);
                if fuel > max_fuel {
                    max_fuel = fuel;
                    max_cell = (x + 1, y + 1);
                    max_size = size;
                }
                if size == 3 && fuel > max3_fuel {
                    max3_fuel = fuel;
                    max3_cell = (x + 1, y + 1)
                }
            }
        }
    }
    (
        String::from(format!("{},{}", max3_cell.0, max3_cell.1)),
        String::from(format!("{},{},{}", max_cell.0, max_cell.1, max_size)),
    )
}

fn get_input(file_path: &String) -> i32 {
    std::fs::read_to_string(file_path)
        .expect("Error reading input file!")
        .trim()
        .parse()
        .unwrap()
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
