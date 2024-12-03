#!/bin/sh

# create ./dayN
mkdir -p "day$1"

cd "day$1"
cp ../day1/Makefile .

# create ./dayN/aoc2022-dN-python
uv init --app aoc2024-d$1-python --package --python 3.13

cd "aoc2024-d$1-python"
cp ../../day1/aoc2024-d1-python/Makefile .

mkdir tests
touch "tests/test_day$1.py"

echo "source .venv/bin/activate" > .envrc
direnv allow .
uv add --dev pytest pytest-cov ipdb

# back to original folder
cd ../../
