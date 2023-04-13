#!/bin/sh
mkdir $1
cat ./template.py > $1/solve.py
touch $1/input.txt
touch $1/sample_input.txt

