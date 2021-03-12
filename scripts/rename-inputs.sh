for year in {2015..2020}
do
    for day in {1..25}
    do
        input="../$year/`printf %02d $day`/input.txt"
        input2="../$year/`printf %02d $day`/input2.txt"
        if [[ -f "$input" ]]; then
            git mv "$input" "../$year/`printf %02d $day`/input0.txt"
        fi
        if [[ -f "$input2" ]]; then
            git mv "$input2" "../$year/`printf %02d $day`/input1.txt"
        fi
    done
done
