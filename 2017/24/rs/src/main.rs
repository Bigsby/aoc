use std::collections::VecDeque;

type Component = (usize, usize);
// Component = Tuple[int,int]

fn connects(component: &Component, port: usize) -> bool {
    component.0 == port || component.1 == port
}

fn solve(components: &Vec<Component>) -> (usize, usize) {
    let starts: Vec<Component> = components
        .iter()
        .copied()
        .filter(|component| component.0 == 0 || component.1 == 0)
        .collect();
    let mut queue: VecDeque<(usize, usize, Vec<Component>)> = VecDeque::new();
    for component in starts {
        queue.push_back((
            if component.0 == 0 {
                component.1
            } else {
                component.0
            },
            0,
            vec![component],
        ));
    }
    let mut longest_strongest_1 = (0, 0);
    let mut longest_strongest_2 = (0, 0);
    while let Some((last_port, strength, used)) = queue.pop_front() {
        let mut continued = false;
        for component in components {
            if connects(component, last_port) && !used.contains(component) {
                continued = true;
                let next_port = if component.0 == last_port {
                    component.1
                } else {
                    component.0
                };
                let mut new_used = used.clone();
                new_used.push(*component);
                queue.push_back((next_port, strength + last_port * 2, new_used));
            }
        }
        if !continued {
            longest_strongest_1 = longest_strongest_1.max((0, strength + last_port));
            longest_strongest_2 = longest_strongest_2.max((used.len(), strength + last_port));
        }
    }
    (longest_strongest_1.1, longest_strongest_2.1)
}
// def solve(components: List[Component]) -> Tuple[int,int]:
//     starts = [ component for component in components if 0 in component ]
//     queue: List[Tuple[int,int,List[Component]]] = [ (next(port for port in start if port != 0), 0, [start])
//         for start in starts ]
//     longestStrongest1 = (0, 0)
//     longestStrongest2 = (0, 0)
//     while queue:
//         lastPort, strength, used = queue.pop(0)
//         continued = False
//         for component in components:
//             if lastPort in component and component not in used:
//                 continued = True
//                 nextPort = lastPort if component[0] == component[1] else next(port for port in component if port != lastPort)
//                 newUsed = used[:]
//                 newUsed.append(component)
//                 queue.append((nextPort, strength + lastPort * 2, newUsed))
//         if not continued:
//             longestStrongest1 = max(longestStrongest1, (0, strength + lastPort))
//             longestStrongest2 = max(longestStrongest2, (len(used), strength + lastPort))
//     return longestStrongest1[1], longestStrongest2[1]

fn get_input(file_path: &String) -> Vec<Component> {
    std::fs::read_to_string(file_path)
        .expect("Error reading input file!")
        .lines()
        .map(|line| {
            let splits: Vec<&str> = line.split("/").collect();
            (splits[0].parse().unwrap(), splits[1].parse().unwrap())
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
