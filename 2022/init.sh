#!/bin/sh

# create ./dayN
mkdir -p "day$1"

cd "day$1"
cp ../day1/Makefile .

# create ./dayN/aoc2022-dN-python
poetry new --src "aoc2022-d$1-python"

cd "aoc2022-d$1-python"
cp ../../day1/aoc2022-d1-python/Makefile .
poetry config virtualenvs.in-project true --local
poetry add --group=dev black prospector pylint=2.15.5 typing-extensions pytest
poetry install

# back to original folder
cd ../../
