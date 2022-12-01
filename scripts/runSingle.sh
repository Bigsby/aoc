languages[0]="py"
prefix[0]=""
sufix[0]="py/run.py "

languages[1]="cs"
prefix[1]="dotnet run --project"
sufix[1]="cs/run.csproj "

languages[2]="c"
prefix[2]="make -f "
sufix[2]="c/makefile INPUT="

languages[3]="js"
prefix[3]="node"
sufix[3]="js/run.js "

languages[4]="rs"
prefix[4]="cargo run --quiet --manifest-path"
sufix[4]="rs/Cargo.toml "

languages[5]="cpp"
prefix[5]="make -f "
sufix[5]="cpp/makefile INPUT="

languages[6]="go"
prefix[6]="go run"
sufix[6]="go/run.go "

languages[7]="swift"
prefix[7]="swift"
sufix[7]="swift/run.swift "

get_language_index() {
    required="$1"
    index=0
    for lang in ${languages[@]}; do
        if [ "$required" == "$lang" ]
            then
                return $index
        fi
        index=$((index+1))
    done
    return -1
}

show_usage() {
    echo "$1"
    echo "Usage:"
    echo "$0 YEAR/DAY/LANGUAGE INPUT_FILE"
}

years="2015 2016 2017 2018 2019 2020 2021 2022"
days="01 02 03 04 05 06 07 08 09 10 11 12 13 14 15 16 17 18 19 20 21 22 23 24 25"
time_execution=0

puzzle="$1"
input_file="$2"

declare -a puzzle_parts=(`echo "$puzzle" |sed 's/\\// /g'`)
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
if [[ -z "${input_file}" ]]; then
    show_usage "Input file required"
fi

get_language_index $language
language_index=$?
DIR="$( cd "$( dirname "$0" )" &> /dev/null && pwd )"
        
command_to_run="${prefix[language_index]} $DIR/../$year/$day/${sufix[language_index]}$input_file"
echo "$year/$day $language"
$command_to_run
