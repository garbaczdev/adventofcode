#!/bin/sh
mkdir $1
cat ./template.py > $1/solve.py
touch $1/input.txt
touch $1/sample_input.txt

# Arch Specific - Automated input downloading
source /disk/linux/python3-venvs/aoc-env/bin/activate
aocd $1 2023 > $1/input.txt
