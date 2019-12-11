INSTRUCTION_CODE_HALT = '99'
INSTRUCTION_CODE_ADD = '01' 
INSTRUCTION_CODE_MULTIPLY = '02'
INSTRUCTION_CODE_INPUT = '03'
INSTRUCTION_CODE_OUTPUT = '04'
INSTRUCTION_CODE_JUMP_IF_TRUE = '05'
INSTRUCTION_CODE_JUMP_IF_FALSE = '06'
INSTRUCTION_CODE_LESS_THAN = '07'
INSTRUCTION_CODE_EQUALS = '08'
INSTRUCTION_CODE_ADJUST_RELATIVE_BASE = '09'

MODE_POSITION = '0'
MODE_IMMEDIATE = '1'
MODE_RELATIVE = '2'

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
            incoming.map.with_index {|input, idx|
                idx == 0 \
                    ? [input, 0]
                    : [input]
            },
            incoming.map {|_| []},
            incoming.map {|_| 0},
            incoming.map {|_| 0})

        signal > current.last \
            ? [incoming, signal]
            : current
    }
end

def amplifier_eval(memory, phase_settings, output_prev=[])
    result = false

    if phase_settings.empty?
        result = output_prev.last
    else
        result = amplifier_eval(
            memory,
            phase_settings[1, phase_settings.size - 1],
            memory_eval(memory, [phase_settings.first, output_prev.last]).last)
    end

    result
end

def amplifier_eval_feedback_loop(memory_states, input_states, output_states, base_states, pointer_states, n=0)
    result = false

    if pointer_states.select {|x| x == false}.size == pointer_states.size
        result = output_states.last.last
    elsif pointer_states[n] == false
        result = amplifier_eval_feedback_loop(
            memory_states,
            input_states,
            output_states,
            base_states,
            pointer_states,
            (n + 1) % pointer_states.size)
    else
        memory, input, output, base, pointer = memory_eval_looper_stepper(
            memory_states[n],
            input_states[n],
            output_states[n],
            base_states[n],
            pointer_states[n])
        result = amplifier_eval_feedback_loop(
            memory_states.map.with_index {|x, idx| idx == n ? memory : x},
            input_states.map.with_index {|x, idx|
                if idx == n 
                    input
                elsif idx == (n + 1) % pointer_states.size
                    x + [output.last]
                else
                    x
                end
            },
            output_states.map.with_index {|x, idx| idx == n ? output : x},
            base_states.map.with_index {|x, idx| idx == n ? base : x},
            pointer_states.map.with_index {|x, idx| idx == n ? pointer : x},
            (n + 1) % pointer_states.size)
    end

    result
end

def input_parse(input)
    input \
        .split(',')
        .reduce([{}, 0]) {|current, incoming|
            current.first[current.last] = incoming.strip()

            [current.first, current.last + 1]
        }
        .first
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

def memory_check_writable(parameter_mode)
    raise "Mode is not writable" unless (parameter_mode == MODE_POSITION || parameter_mode == MODE_RELATIVE)
end

def memory_get_address(memory, relative_base, address, parameter_mode)
    result = false

    if parameter_mode == MODE_POSITION
        result = memory.fetch(address, 0).to_i
    elsif parameter_MODE == MODE_RELATIVE
        result = relative_base + memory.fetch(address, 0).to_i
    end

    result
end

def memory_get_value(memory, relative_base, address, parameter_mode=MODE_IMMEDIATE)
    result = false

    if parameter_mode == MODE_POSITION
        result = memory.fetch(memory_get_value(memory, relative_base, address), 0).to_i
    elsif parameter_mode == MODE_IMMEDIATE
        result = memory.fetch(address, 0).to_i
    elsif parameter_mode == MODE_RELATIVE
        result = memory.fetch(relative_base + memory_get_value(memory, relative_base, address), 0).to_i
    end

    result
end

def memory_eval_looper_stepper(memory, input, output=[], relative_base=0, instruction_pointer=0)
    result, input_new, output_new, base, pointer = [], [], 0, 0, 0

    # p memory.sort.to_h
    # p "BASE #{relative_base} POINTER #{instruction_pointer} OPCODE #{opcode_get(memory[instruction_pointer])} INPUT #{input} OUTPUT #{output}"
    if opcode_get(memory[instruction_pointer]) == INSTRUCTION_CODE_HALT
        result = (0..memory.keys.max).map {|idx| memory_get_value(memory, relative_base, idx)}
        input_new = input
        output_new = output
        base = relative_base
        pointer = false
    elsif opcode_get(memory[instruction_pointer]) == INSTRUCTION_CODE_ADD
        result, input_new, output_new, base, pointer = memory_eval_looper_stepper(
            memory_eval_addition(memory, relative_base, instruction_pointer),
            input,
            output,
            relative_base,
            instruction_pointer + 4)
    elsif opcode_get(memory[instruction_pointer]) == INSTRUCTION_CODE_MULTIPLY
        result, input_new, output_new, base, pointer = memory_eval_looper_stepper(
            memory_eval_multiplication(memory, relative_base, instruction_pointer),
            input,
            output,
            relative_base,
            instruction_pointer + 4)
    elsif opcode_get(memory[instruction_pointer]) == INSTRUCTION_CODE_INPUT
        raise ArgumentError unless !(input.empty?)

        result, input_new, output_new, base, pointer = memory_eval_looper_stepper(
            memory_eval_input(memory, relative_base, instruction_pointer, input.first),
            input[1, input.size - 1],
            output,
            relative_base,
            instruction_pointer + 2)
    elsif opcode_get(memory[instruction_pointer]) == INSTRUCTION_CODE_OUTPUT
        result = memory
        input_new = input
        output_new = output + [memory_eval_output(memory, relative_base, instruction_pointer)]
        base = relative_base
        pointer = instruction_pointer + 2
    elsif opcode_get(memory[instruction_pointer]) == INSTRUCTION_CODE_JUMP_IF_TRUE
        result, input_new, output_new, base, pointer = memory_eval_looper_stepper(
            memory,
            input,
            output,
            relative_base,
            memory_eval_jump_if_true(memory, relative_base, instruction_pointer))
    elsif opcode_get(memory[instruction_pointer]) == INSTRUCTION_CODE_JUMP_IF_FALSE
        result, input_new, output_new, base, pointer = memory_eval_looper_stepper(
            memory,
            input,
            output,
            relative_base,
            memory_eval_jump_if_false(memory, relative_base, instruction_pointer))
    elsif opcode_get(memory[instruction_pointer]) == INSTRUCTION_CODE_LESS_THAN
        result, input_new, output_new, base, pointer = memory_eval_looper_stepper(
            memory_eval_less_than(memory, relative_base, instruction_pointer),
            input,
            output,
            relative_base,
            instruction_pointer + 4)
    elsif opcode_get(memory[instruction_pointer]) == INSTRUCTION_CODE_EQUALS
        result, input_new, output_new, base, pointer = memory_eval_looper_stepper(
            memory_eval_equals(memory, relative_base, instruction_pointer),
            input,
            output,
            relative_base,
            instruction_pointer + 4)
    elsif opcode_get(memory[instruction_pointer]) == INSTRUCTION_CODE_ADJUST_RELATIVE_BASE
        result, input_new, output_new, base, pointer = memory_eval_looper_stepper(
            memory,
            input,
            output,
            relative_base + memory_get_value(
                memory,
                relative_base,
                instruction_pointer + 1,
                opcode_get_parameter_mode(memory[instruction_pointer], 0)),
            instruction_pointer + 2)
    else
        raise "Bad OPCODE %s" % [memory[instruction_pointer]]
    end

    return result, input_new, output_new, base, pointer
end

def memory_eval(memory, input, output=[], relative_base=0, instruction_pointer=0)
    result, output_new = [], []

    # p memory.sort.to_h
    # p "BASE #{relative_base} POINTER #{instruction_pointer} OPCODE #{opcode_get(memory[instruction_pointer])} INPUT #{input} OUTPUT #{output}"
    if opcode_get(memory[instruction_pointer]) == INSTRUCTION_CODE_HALT
        result = (0..memory.keys.max).map {|idx| memory_get_value(memory, relative_base, idx)}
        output_new = output
    elsif opcode_get(memory[instruction_pointer]) == INSTRUCTION_CODE_ADD
        result, output_new = memory_eval(
            memory_eval_addition(memory, relative_base, instruction_pointer),
            input,
            output,
            relative_base,
            instruction_pointer + 4)
    elsif opcode_get(memory[instruction_pointer]) == INSTRUCTION_CODE_MULTIPLY
        result, output_new = memory_eval(
            memory_eval_multiplication(memory, relative_base, instruction_pointer),
            input,
            output,
            relative_base,
            instruction_pointer + 4)
    elsif opcode_get(memory[instruction_pointer]) == INSTRUCTION_CODE_INPUT
        result, output_new = memory_eval(
            memory_eval_input(memory, relative_base, instruction_pointer, input.first),
            input[1, input.size - 1],
            output,
            relative_base,
            instruction_pointer + 2)
    elsif opcode_get(memory[instruction_pointer]) == INSTRUCTION_CODE_OUTPUT
        result, output_new = memory_eval(
            memory,
            input,
            output + [memory_eval_output(memory, relative_base, instruction_pointer)],
            relative_base,
            instruction_pointer + 2)
    elsif opcode_get(memory[instruction_pointer]) == INSTRUCTION_CODE_JUMP_IF_TRUE
        result, output_new = memory_eval(
            memory,
            input,
            output,
            relative_base,
            memory_eval_jump_if_true(memory, relative_base, instruction_pointer))
    elsif opcode_get(memory[instruction_pointer]) == INSTRUCTION_CODE_JUMP_IF_FALSE
        result, output_new = memory_eval(
            memory,
            input,
            output,
            relative_base,
            memory_eval_jump_if_false(memory, relative_base, instruction_pointer))
    elsif opcode_get(memory[instruction_pointer]) == INSTRUCTION_CODE_LESS_THAN
        result, output_new = memory_eval(
            memory_eval_less_than(memory, relative_base, instruction_pointer),
            input,
            output,
            relative_base,
            instruction_pointer + 4)
    elsif opcode_get(memory[instruction_pointer]) == INSTRUCTION_CODE_EQUALS
        result, output_new = memory_eval(
            memory_eval_equals(memory, relative_base, instruction_pointer),
            input,
            output,
            relative_base,
            instruction_pointer + 4)
    elsif opcode_get(memory[instruction_pointer]) == INSTRUCTION_CODE_ADJUST_RELATIVE_BASE
        result, output_new = memory_eval(
            memory,
            input,
            output,
            relative_base + memory_get_value(
                memory,
                relative_base,
                instruction_pointer + 1,
                opcode_get_parameter_mode(memory[instruction_pointer], 0)),
            instruction_pointer + 2)
    else
        raise "Bad OPCODE %s" % [memory[instruction_pointer]]
    end

    return result, output_new
end

def memory_eval_addition(memory, relative_base, address)
    memory_check_writable(opcode_get_parameter_mode(memory[address], 2))

    memory_eval_changes(
        memory,
        memory_get_address(memory, relative_base, address + 3, opcode_get_parameter_mode(memory[address], 2)),
        (memory_get_value(memory, relative_base, address + 1, opcode_get_parameter_mode(memory[address], 0)) \
            + memory_get_value(memory, relative_base, address + 2, opcode_get_parameter_mode(memory[address], 1))).to_s)
end

def memory_eval_changes(memory, address, value)
    memory.each
        .to_a
        .reduce({address => value}) {|current, incoming|
            if current.key?(incoming.first) == false
                current[incoming.first] = incoming.last
            end

            current
        }
end

def memory_eval_equals(memory, relative_base, address)
    memory_check_writable(opcode_get_parameter_mode(memory[address], 2))

    memory_eval_changes(
        memory,
        memory_get_address(memory, relative_base, address + 3, opcode_get_parameter_mode(memory[address], 2)),
        memory_get_value(memory, relative_base, address + 1, opcode_get_parameter_mode(memory[address], 0)) \
            == memory_get_value(memory, relative_base, address + 2, opcode_get_parameter_mode(memory[address], 1)) \
            ? '1'
            : '0')
end

def memory_eval_input(memory, relative_base, address, input)
    memory_check_writable(opcode_get_parameter_mode(memory[address], 0))

    memory_eval_changes(
        memory,
        memory_get_address(memory, relative_base, address + 1, opcode_get_parameter_mode(memory[address], 0)),
        input.to_s)
end


def memory_eval_jump_if_false(memory, relative_base, address)
    return memory_get_value(memory, relative_base, address + 1, opcode_get_parameter_mode(memory[address], 0)) == 0 \
        ? memory_get_value(memory, relative_base, address + 2, opcode_get_parameter_mode(memory[address], 1))
        : address + 3
end


def memory_eval_jump_if_true(memory, relative_base, address)
    return memory_get_value(memory, relative_base, address + 1, opcode_get_parameter_mode(memory[address], 0)) != 0 \
        ? memory_get_value(memory, relative_base, address + 2, opcode_get_parameter_mode(memory[address], 1))
        : address + 3
end

def memory_eval_less_than(memory, relative_base, address)
    memory_check_writable(opcode_get_parameter_mode(memory[address], 2))

    memory_eval_changes(
        memory,
        memory_get_address(memory, relative_base, address + 3, opcode_get_parameter_mode(memory[address], 2)),
        memory_get_value(memory, relative_base, address + 1, opcode_get_parameter_mode(memory[address], 0)) \
            < memory_get_value(memory, relative_base, address + 2, opcode_get_parameter_mode(memory[address], 1)) \
            ? '1'
            : '0')
end

def memory_eval_multiplication(memory, relative_base, address)
    memory_check_writable(opcode_get_parameter_mode(memory[address], 2))

    memory_eval_changes(
        memory,
        memory_get_address(memory, relative_base, address + 3, opcode_get_parameter_mode(memory[address], 2)),
        (memory_get_value(memory, relative_base, address + 1, opcode_get_parameter_mode(memory[address], 0)) \
            * memory_get_value(memory, relative_base, address + 2, opcode_get_parameter_mode(memory[address], 1))).to_s
    )
end

def memory_eval_output(memory, relative_base, address)
    return memory_get_value(memory, relative_base, address + 1, opcode_get_parameter_mode(memory[address], 0))
end

# returns memory, and diagnostic_code (final output)
def intcode_compute(diagnostic_program, input=nil)
    memory_eval(
        input_parse(diagnostic_program),
        input != nil ? [input] : [])
end