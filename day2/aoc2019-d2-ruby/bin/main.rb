require 'intcoder'

def compute_puzzle1()
    intcode_compute(
        File.readlines(ENV['PUZZLE_INPUT']).join(''),
        12,
        2)[0]
end

def pair_search(input, noun=0, verb=0)
    result = false

    if noun <= 99
        # do the test
        memory = intcode_compute(input, noun, verb)

        if memory[0] == 19690720
            result = 100 * noun + verb
        else
            if verb >= 99
                result = pair_search(input, noun + 1, 0)
            else
                result = pair_search(input, noun, verb + 1)
            end
        end
    end

    result
end

def compute_puzzle2()
    pair_search(File.readlines(ENV['PUZZLE_INPUT']).join(''))
end

puts "Answer for puzzle 1 is #{compute_puzzle1}"
puts "Answer for puzzle 2 is #{compute_puzzle2}"