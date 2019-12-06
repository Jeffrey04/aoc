require 'intcoder'

def fix_puzzle1_input()
    File.readlines(ENV['PUZZLE_INPUT'])
                .join('')
                .split(',')
                .map.with_index{|x, idx|
                    result = x

                    if idx == 1
                        result = '12'
                    elsif idx == 2
                        result = '2'
                    end

                    result
                }
                .join(',')
end

def compute_puzzle1()
    intcode_compute(fix_puzzle1_input)
end

puts "Answer for puzzle 1 is #{compute_puzzle1[0]}"