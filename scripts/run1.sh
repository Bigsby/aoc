declare -A languages=(
    ["py"]="|py/run.py "
    ["cs"]="dotnet run -p|cs/run.csproj " 
    ["rs"]="cargo run --quiet --manifest-path|rs/Cargo.toml "
    ["cpp"]="make -f |cpp/makefile INPUT="
    ["js"]="node|js/run.js "
)
IFS=" "
years="2015 2016 2017 2018 2019 2020"
days="01 02 03 04 05 06 07 08 09 10 11 12 13 14 15 16 17 18 19 20 21 22 23 24 25"
unset IFS
time_execution=0
show_usage () {
    if [[ "$1" ]] ; then
        echo "ERROR: $1"
        echo ""
    fi
    echo "Usage:"
    echo "${BASH_SOURCE[0]} YEAR/DAY[/LANGUAGE] [-t] [-i INPUT]"
    echo ""
    echo "Options:"
    echo "  YEAR               $years"
    echo "  DAY                $days"
    echo "  LANGUAGE           ${!languages[@]}"
    echo "  --time, -t         time execution"
    echo "  --input, -i INPUT  alternate input file"
    exit
}

time_execution=0
input_file="input.txt"
puzzle=""
if [[ "$1" ]] ; then
    puzzle="$1"
    shift
    while [[ $# -gt 0 ]]
    do
    key="$1"
    case $key in 
        -t|--time)
        time_execution=1
        shift
        ;;
        -i|--input)
        input_file="$2"
        if [[ -z "$input_file" ]] ; then
            show_usage "No input file provided"
        fi
        shift
        shift
        ;;
    esac
    done
else
    show_usage
fi


IFS="/" read -r -a puzzle_parts <<< $puzzle
languages_to_run=${!languages[@]}
year="${puzzle_parts[0]}"
day="${puzzle_parts[1]}"
language="${puzzle_parts[2]}"
if [[ ! " ${years[@]} " =~ " ${year} " ]]; then
    show_usage "$year not a a valid YEAR. Must be one of $years"
fi
if [[ ! " ${days[@]} " =~ " ${day} " ]]; then
    show_usage "$day not a valid DAY. Must be one of $days"
fi
if [[ "$language" ]] ; then 
    if [[ -v "languages[$language]" ]] ; then
        languages_to_run=($language)
    else
        show_usage "Language not found. Options are: $languages_to_run"
    fi
fi

DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" &> /dev/null && pwd )"
for language in $languages_to_run
do
    IFS="|" read -r -a parts <<< ${languages[$language]}
    echo "$year/`printf %02d $day` $language"
    if [[ "$time_execution" == "1" ]]; then
        { time ${parts[0]} $DIR/../$year/`printf %02d $day`/${parts[1]}"$DIR/../$year/`printf %02d $day`/input.txt" ; } 2>&1
    else
        ${parts[0]} $DIR/../$year/`printf %02d $day`/${parts[1]}"$DIR/../$year/`printf %02d $day`/input.txt"
    fi
    echo ""
done
