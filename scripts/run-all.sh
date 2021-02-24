for year in {2015..2020}
do
    for day in {1..25}
    do
        echo "$year/`printf %02d $day` py"
        { time ../$year/`printf %02d $day`/py/run.py "../$year/`printf %02d $day`/input.txt" ; } 2>&1
        echo "---------------------------------------"
        echo "$year/`printf %02d $day` cs"
        { time dotnet run -p ../$year/`printf %02d $day`/cs/run.csproj "../$year/`printf %02d $day`/input.txt" ; } 2>&1
        echo "---------------------------------------"
    done
done
