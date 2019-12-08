INSTRUCTION_CODE_HALT = '99'
INSTRUCTION_CODE_ADD = '01' 
INSTRUCTION_CODE_MULTIPLY = '02'
INSTRUCTION_CODE_INPUT = '03'
INSTRUCTION_CODE_OUTPUT = '04'

MODE_POSITION = '0'
MODE_IMMEDIATE = '1'

EXCEPTION_BAD_OUTPUT = "Error in previous output attempt"

def input_parse(input)
    input \
        .split(',')
end

def opcode_get(value)
    result = value

    if value.size > 2
        result = value[-2, value.size]
    elsif value.size <2
        result = "%02d" % [value]
    end

    result
end

def opcode_get_parameter_mode(opcode, parameter)
    opcode[-3 - parameter] || 0
end

def output_check(output)
    raise EXCEPTION_BAD_OUTPUT unless output == 0
end

def memory_get_value(memory, address, parameter_mode=MODE_IMMEDIATE)
    result = false

    if parameter_mode == MODE_POSITION
        result = memory[memory_get_value(memory, address)].to_i
    else parameter_mode == MODE_IMMEDIATE
        result = memory[address].to_i
    end

    result
end

def memory_eval(memory, input, output=0, instruction_pointer=0)
    result = []

    if opcode_get(memory[instruction_pointer]) == INSTRUCTION_CODE_HALT
        result = memory.map {|x| x.to_i}
    elsif opcode_get(memory[instruction_pointer]) == INSTRUCTION_CODE_ADD
        output_check(output)

        result, output = memory_eval(
            memory_eval_addition(memory, instruction_pointer),
            input,
            output,
            instruction_pointer + 4)
    elsif opcode_get(memory[instruction_pointer]) == INSTRUCTION_CODE_MULTIPLY
        output_check(output)

        result, output = memory_eval(
            memory_eval_multiplication(memory, instruction_pointer),
            input,
            output,
            instruction_pointer + 4)
    elsif opcode_get(memory[instruction_pointer]) == INSTRUCTION_CODE_INPUT
        output_check(output)

        result, output = memory_eval(
            memory_eval_input(memory, instruction_pointer, input),
            input,
            output,
            instruction_pointer + 2)
    elsif opcode_get(memory[instruction_pointer]) == INSTRUCTION_CODE_OUTPUT
        output_check(output)

        _memory, _output = memory_eval_output(memory, instruction_pointer)

        result, output = memory_eval(
            _memory,
            input,
            _output,
            instruction_pointer + 2)
    end

    return result, output
end

def memory_eval_addition(memory, address)
    memory.map.with_index{|frame, idx|
        idx == memory_get_value(memory, address + 3) \
            ? (memory_get_value(memory, address + 1, opcode_get_parameter_mode(memory[address], 0)) \
                + memory_get_value(memory, address + 2, opcode_get_parameter_mode(memory[address], 1))).to_s
            : frame 
    }
end

def memory_eval_input(memory, address, input)
    memory.map.with_index {|frame, idx|
        idx == memory_get_value(memory, address + 1) \
            ? input
            : frame
    }
end

def memory_eval_multiplication(memory, address)
    memory.map.with_index{|frame, idx|
        idx == memory_get_value(memory, address + 3) \
            ? (memory_get_value(memory, address + 1, opcode_get_parameter_mode(memory[address], 0)) \
                * memory_get_value(memory, address + 2, opcode_get_parameter_mode(memory[address], 1))).to_s
            : frame
    }
end

def memory_eval_output(memory, address)
    return memory, memory_get_value(memory, address + 1, MODE_POSITION)
end

# returns memory, and diagnostic_code (final output)
def intcode_compute(diagnostic_program, input)
    memory_eval(input_parse(diagnostic_program), input)
end