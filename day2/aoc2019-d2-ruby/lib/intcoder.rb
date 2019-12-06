def code_ref_value(code, reference_pointer)
    code[code[reference_pointer]]
end

def input_parse(input)
    input \
        .split(',')
        .map{|x| x.to_i}
end

def input_eval(code, pointer=0)
    result = []

    if code[pointer] == 99
        result = code
    elsif code[pointer] == 1
        result = input_eval(
            input_eval_addition(code, pointer),
            pointer + 4)
    elsif code[pointer] == 2
        result = input_eval(
            input_eval_multiplication(code, pointer),
            pointer + 4)
    end

    result
end

def input_eval_addition(code, pointer)
    code.map.with_index{|x, i|
        i == code[pointer + 3] \
            ? code_ref_value(code, pointer + 1) + code_ref_value(code, pointer + 2)
            : x
    }
end

def input_eval_multiplication(code, pointer)
    code.map.with_index{|x, i|
        i == code[pointer + 3] \
            ? code_ref_value(code, pointer + 1) * code_ref_value(code, pointer + 2)
            : x
    }
end

def intcode_compute(input)
    input_eval(input_parse(input))
end