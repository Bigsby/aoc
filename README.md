# Advent of Code

Solving the challenges in [Advent of Code](https://adventofcode.com/).

# Running

`cd` into _YEAR_/_DAY_ directory and ...

## Python
### Linux, macOS
``` sh
./py/run.py INPUT_FILE
```
### Windows
``` sh
python py/run.py INPUT_FILE
```

## C#
``` sh
dotnet run -p cs/run.csproj INPUT_FILE
```

## Rust
``` sh
cargo run --quiet --manifest-path rs/Cargo.toml INPUT_FILE
```

## Javascript
``` sh
node js/run.js INPUT_FILE
```
## C++
``` sh
make -f cpp/makefile INPUT=INPUT_FILE
```
## C
``` sh
make -f c/makefile INPUT=INPUT_FILE
```
## Go
``` sh
go run go/run.go INPUT=INPUT_FILE
```