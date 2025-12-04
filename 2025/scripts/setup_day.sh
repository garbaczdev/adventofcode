#!/bin/bash

# Change if needed
YEAR="2025"
COOKIE="$(cat ~/.secrets/aoc-cookie)"

if [ -z "$COOKIE" ]; then
  echo "Cookie not present. Unable to run the script"
  exit 1
fi

# Colors
RED="\033[31m"
GREEN="\033[32m"
YELLOW="\033[33m"
BLUE="\033[34m"
RESET="\033[0m"


SCRIPT_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"
ALL_DAYS_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )"/.. && pwd )"
ASCII_ART_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )"/ascii-responses && pwd )"
mkdir -p "$ASCII_ART_DIR"

fetch_input() {
  year=$1
  day=$2
  index="https://adventofcode.com/$year/day/$day"
  curl "$index/input" \
    -b "$COOKIE" \
    -H "referer: $index"
}

day=`seq 1 25 | fzf --height 20 --border --reverse`
if [ -z "$day" ]; then
  echo -e "$RED$(cat "$ASCII_ART_DIR"/directory-not-provided.txt)$RESET"
  exit 1
fi

DAY_DIR="$ALL_DAYS_DIR/$day"
if [ -d "$DAY_DIR" ]; then
  echo -e "$YELLOW$(cat "$ASCII_ART_DIR"/directory-exists.txt)$RESET"
  exit 1
fi


mkdir -p "$DAY_DIR"
cp "$SCRIPT_DIR"/template.py "$DAY_DIR/solve.py"
touch "$DAY_DIR/sample_input.txt"

fetch_input "$YEAR" "$day" > "$DAY_DIR/input.txt"

echo -e "$GREEN$(cat "$ASCII_ART_DIR"/success.txt)$RESET"
