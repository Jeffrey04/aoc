require 'enumerator'

def password_adjacent_digits_not_part_of_larger_group(password)
    password.split('')
        .each_cons(2)
        .reduce({}) {|current, incoming|
            result = current

            if incoming[0] == incoming[1]
                result[incoming.join()] = result.fetch(incoming.join(), 0) + 1
            end

            result
        }.value? 1
end

def password_get_candidates(checker, min, max)
    (min.to_i..max.to_i)
        .select {|candidate| checker.call(candidate.to_s)}
        .map {|x| x.to_s}
end

def password_is_good(password)
    password.length == 6 \
        && password_has_identical_adjacent_digits(password) \
        && password_has_increasing_digits(password)
end

def password_is_good_too(password)
    password_is_good(password) \
        && password_adjacent_digits_not_part_of_larger_group(password)
end

def password_has_identical_adjacent_digits(password)
    password[1, password.length]
        .split('')
        .reduce([password[0], false]) {|current, incoming|
            [incoming, current.first == incoming || current.last]
        }.last
end

def password_has_increasing_digits(password)
    password[1, password.length]
        .split('')
        .map {|x| x.to_i}
        .reduce([password[0].to_i, true]) {|current, incoming|
            [incoming, current.first <= incoming && current.last]
        }.last
end