def image_parse_data(image_data)
    image_data.split('').map {|x| x.strip().to_i}
end

def image_build(image_data, column, row, layers=[])
    result = false

    if image_data.empty?
        result = layers
    else
        result = image_build(
            image_data[column * row,image_data.size - (column * row)],
            column,
            row,
            layers + [image_data[0, column * row].each_slice(column).to_a])
    end

    result
end

def image_check_corruption(image_raw, column, row)
    image_build(image_parse_data(image_raw), column, row)
        .reduce([Float::INFINITY, 0]) {|current, incoming|
            zeroes = incoming.flatten.select {|x| x == 0}.size
            product = incoming.flatten.select {|x| x == 1}.size \
                * incoming.flatten.select{|x| x == 2}.size

            zeroes != 0 && 0 < current.first \
                ? [zeroes, product]
                : current
        }.last
end