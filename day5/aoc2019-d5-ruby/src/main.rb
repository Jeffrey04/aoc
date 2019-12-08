require 'intcoder'

def compute_puzzle1()
    _, diagnostic_code = intcode_compute(
        File.readlines(ENV['PUZZLE_INPUT']).join(''),
        '1')

    diagnostic_code
end

def compute_puzzle2()
end

puts("RUBY:\t#{compute_puzzle1}\t#{compute_puzzle2}")