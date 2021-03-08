struct Node {
    children: Vec<Node>,
    metadata: Vec<u32>,
}

fn read_node(data: &mut Vec<u32>) -> Node {
    let children_count = data.pop().unwrap();
    let metadata_count = data.pop().unwrap();
    let mut children = Vec::new();
    let mut metadata = Vec::new();
    for _ in 0..children_count {
        children.push(read_node(data));
    }
    for _ in 0..metadata_count {
        metadata.push(data.pop().unwrap());
    }
    Node { children, metadata }
}

fn get_metadata_sum(node: &Node) -> u32 {
    node.metadata.iter().sum::<u32>()
        + node
            .children
            .iter()
            .map(|child| get_metadata_sum(child))
            .sum::<u32>()
}

fn get_value(node: &Node) -> u32 {
    let children_count = node.children.len() as u32;
    if children_count == 0 {
        node.metadata.iter().sum()
    } else {
        node.metadata
            .clone()
            .into_iter()
            .filter(|index| *index > 0 && *index <= children_count)
            .map(|index| get_value(&node.children[(index as usize) - 1]))
            .sum::<u32>()
    }
}

fn solve(data: &Vec<u32>) -> (u32, u32) {
    let mut data = data.clone();
    data.reverse();
    let root = read_node(&mut data);
    (get_metadata_sum(&root), get_value(&root))
}

fn get_input(file_path: &String) -> Vec<u32> {
    std::fs::read_to_string(file_path)
        .expect("Error reading input file!")
        .split(" ")
        .map(|split| split.parse().unwrap())
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
