def password_is_good(password)
    password.length == 6 \
        && password_has_identical_adjacent_digits(password) \
        && password_has_increasing_digits(password)
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