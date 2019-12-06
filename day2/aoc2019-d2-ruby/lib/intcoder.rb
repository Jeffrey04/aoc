INSTRUCTION_CODE_HALT = 99
INSTRUCTION_CODE_ADD = 1
INSTRUCTION_CODE_MULTIPLY = 2

ADDRESS_OF_NOUN = 1
ADDRESS_OF_VERB = 2

def input_parse(input, noun, verb)
    input \
        .split(',')
        .map.with_index{|x, idx|
            result = x.strip.to_i

            if idx == ADDRESS_OF_NOUN && noun
                result = noun
            elsif idx == ADDRESS_OF_VERB && noun
                result = verb
            end

            result
        }
end

def memory_ref_value(memory, address)
    memory[memory[address]]
end

def memory_eval(memory, instruction_pointer=0)
    result = []

    if memory[instruction_pointer] == INSTRUCTION_CODE_HALT
        result = memory
    elsif memory[instruction_pointer] == INSTRUCTION_CODE_ADD
        result = memory_eval(
            memory_eval_addition(memory, instruction_pointer),
            instruction_pointer + 4)
    elsif memory[instruction_pointer] == INSTRUCTION_CODE_MULTIPLY
        result = memory_eval(
            memory_eval_multiplication(memory, instruction_pointer),
            instruction_pointer + 4)
    end

    result
end

def memory_eval_addition(memory, address)
    memory.map.with_index{|x, i|
        i == memory[address + 3] \
            ? memory_ref_value(memory, address + 1) + memory_ref_value(memory, address + 2)
            : x
    }
end

def memory_eval_multiplication(memory, address)
    memory.map.with_index{|x, i|
        i == memory[address + 3] \
            ? memory_ref_value(memory, address + 1) * memory_ref_value(memory, address + 2)
            : x
    }
end

def intcode_compute(input, noun=false, verb=false)
    memory_eval(input_parse(input, noun, verb))
end