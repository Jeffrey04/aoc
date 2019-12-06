def input_parse(input)
    input \
        .split(',')
        .map{|x| x.strip.to_i}
end

def memory_ref_value(memory, address)
    memory[memory[address]]
end

def memory_eval(memory, address=0)
    result = []

    if memory[address] == 99
        result = memory
    elsif memory[address] == 1
        result = memory_eval(
            memory_eval_addition(memory, address),
            address + 4)
    elsif memory[address] == 2
        result = memory_eval(
            memory_eval_multiplication(memory, address),
            address + 4)
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

def intcode_compute(input)
    memory_eval(input_parse(input))
end