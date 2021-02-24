for year in {2015..2020}
do
    for day in {1..25}
    do
        echo "$year/day_`printf %02d $day` py"
        { time ../$year/day_`printf %02d $day`/py/run.py "../$year/day_`printf %02d $day`/input.txt" ; } 2>&1
        echo "---------------------------------------"
    done
done
