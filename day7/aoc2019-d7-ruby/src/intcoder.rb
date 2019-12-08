INSTRUCTION_CODE_HALT = '99'
INSTRUCTION_CODE_ADD = '01' 
INSTRUCTION_CODE_MULTIPLY = '02'
INSTRUCTION_CODE_INPUT = '03'
INSTRUCTION_CODE_OUTPUT = '04'
INSTRUCTION_CODE_JUMP_IF_TRUE = '05'
INSTRUCTION_CODE_JUMP_IF_FALSE = '06'
INSTRUCTION_CODE_LESS_THAN = '07'
INSTRUCTION_CODE_EQUALS = '08'

MODE_POSITION = '0'
MODE_IMMEDIATE = '1'

EXCEPTION_BAD_OUTPUT = "Error in previous output attempt"

def amplifier_phase_get_best(amplifier_program)
    (0..4).to_a.permutation(5).reduce([[], 0]) {|current, incoming|
        signal = amplifier_eval(input_parse(amplifier_program), incoming)

        signal > current.last \
            ? [incoming, signal]
            : current
    }
end

def amplifier_feedback_loop_phase_get_best(amplifier_program)
    (5..9).to_a.permutation(5).reduce([[], 0]) {|current, incoming|
        signal = amplifier_eval_feedback_loop(
            incoming.map {|_| input_parse(amplifier_program)},
            incoming)

        signal > current.last \
            ? [incoming, signal]
            : current
    }
end

def amplifier_eval(memory, phase_settings, output_prev=0)
    result = false

    if phase_settings.empty?
        result = output_prev
    else
        result = amplifier_eval(
            memory,
            phase_settings[1, phase_settings.size - 1],
            memory_eval(memory, [phase_settings.first, output_prev]).last)
    end

    result
end

def amplifier_eval_feedback_loop(memory_states, phase_settings, output_prev=0, n = 0)
    result = false

    if phase_settings.empty?
        die
    else
        memory, output = memory_eval(memory_states.first, [phase_settings.first, output_prev])

        result = amplifier_eval_feedback_loop(
            memory_states[1, memory_states.size - 1] + [memory],
            phase_settings[1, phase_settings.size - 1],
            output,
            n)
    end

    result
end

def input_parse(input)
    input \
        .split(',')
        .map {|x| x.strip()}
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
    opcode[-3 - parameter] || '0'
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

def memory_eval_manual(memory, input, output=0, instruction_pointer)
    result = []

    return result, output
end

def memory_eval(memory, input, output=0, instruction_pointer=0)
    result, output_new = [], 0

    if opcode_get(memory[instruction_pointer]) == INSTRUCTION_CODE_HALT
        result, output_new = memory.map {|x| x.to_i}, output
    elsif opcode_get(memory[instruction_pointer]) == INSTRUCTION_CODE_ADD
        output_check(output)

        result, output_new = memory_eval(
            memory_eval_addition(memory, instruction_pointer),
            input,
            output,
            instruction_pointer + 4)
    elsif opcode_get(memory[instruction_pointer]) == INSTRUCTION_CODE_MULTIPLY
        output_check(output)

        result, output_new = memory_eval(
            memory_eval_multiplication(memory, instruction_pointer),
            input,
            output,
            instruction_pointer + 4)
    elsif opcode_get(memory[instruction_pointer]) == INSTRUCTION_CODE_INPUT
        output_check(output)

        result, output_new = memory_eval(
            memory_eval_input(memory, instruction_pointer, input.first),
            input[1, input.size - 1],
            output,
            instruction_pointer + 2)
    elsif opcode_get(memory[instruction_pointer]) == INSTRUCTION_CODE_OUTPUT
        output_check(output)

        result, output_new = memory_eval(
            memory,
            input,
            memory_eval_output(memory, instruction_pointer),
            instruction_pointer + 2)
    elsif opcode_get(memory[instruction_pointer]) == INSTRUCTION_CODE_JUMP_IF_TRUE
        result, output_new = memory_eval(
            memory,
            input,
            output,
            memory_eval_jump_if_true(memory, instruction_pointer))
    elsif opcode_get(memory[instruction_pointer]) == INSTRUCTION_CODE_JUMP_IF_FALSE
        result, output_new = memory_eval(
            memory,
            input,
            output,
            memory_eval_jump_if_false(memory, instruction_pointer))
    elsif opcode_get(memory[instruction_pointer]) == INSTRUCTION_CODE_LESS_THAN
        result, output_new = memory_eval(
            memory_eval_less_than(memory, instruction_pointer),
            input,
            output,
            instruction_pointer + 4)
    elsif opcode_get(memory[instruction_pointer]) == INSTRUCTION_CODE_EQUALS
        result, output_new = memory_eval(
            memory_eval_equals(memory, instruction_pointer),
            input,
            output,
            instruction_pointer + 4)
    else
        raise "Bad OPCODE %s" % [memory[instruction_pointer]]
    end

    return result, output_new
end

def memory_eval_addition(memory, address)
    memory.map.with_index{|frame, idx|
        idx == memory_get_value(memory, address + 3) \
            ? (memory_get_value(memory, address + 1, opcode_get_parameter_mode(memory[address], 0)) \
                + memory_get_value(memory, address + 2, opcode_get_parameter_mode(memory[address], 1))).to_s
            : frame 
    }
end

def memory_eval_equals(memory, address)
    memory.map.with_index{|frame, idx|
        idx == memory_get_value(memory, address + 3)  \
            ? memory_eval_equals_value(memory, address) 
            : frame 
    }
end

def memory_eval_equals_value(memory, address)
    memory_get_value(memory, address + 1, opcode_get_parameter_mode(memory[address], 0)) == memory_get_value(memory, address + 2, opcode_get_parameter_mode(memory[address], 1)) \
        ? '1'
        : '0'
end

def memory_eval_input(memory, address, input)
    memory.map.with_index {|frame, idx|
        idx == memory_get_value(memory, address + 1) \
            ? input.to_s
            : frame
    }
end


def memory_eval_jump_if_false(memory, address)
    return memory_get_value(memory, address + 1, opcode_get_parameter_mode(memory[address], 0)) == 0 \
        ? memory_get_value(memory, address + 2, opcode_get_parameter_mode(memory[address], 1))
        : address + 3
end


def memory_eval_jump_if_true(memory, address)
    return memory_get_value(memory, address + 1, opcode_get_parameter_mode(memory[address], 0)) != 0 \
        ? memory_get_value(memory, address + 2, opcode_get_parameter_mode(memory[address], 1))
        : address + 3
end

def memory_eval_less_than(memory, address)
    memory.map.with_index{|frame, idx|
        idx == memory_get_value(memory, address + 3)  \
            ? memory_eval_less_than_value(memory, address) 
            : frame 
    }
end

def memory_eval_less_than_value(memory, address)
    memory_get_value(memory, address + 1, opcode_get_parameter_mode(memory[address], 0)) < memory_get_value(memory, address + 2, opcode_get_parameter_mode(memory[address], 1)) \
        ? '1'
        : '0'
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
    return memory_get_value(memory, address + 1, opcode_get_parameter_mode(memory[address], 0))
end

# returns memory, and diagnostic_code (final output)
def intcode_compute(diagnostic_program, input)
    memory_eval(input_parse(diagnostic_program), [input])
end