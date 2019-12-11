PIXEL_WHITE = 1
PIXEL_BLACK = 0
PIXEL_TRANSPARENT = 2

def image_parse_data(image_data)
    image_data.strip().split('').map {|x| x.strip().to_i}
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

            zeroes != 0 && zeroes < current.first \
                ? [zeroes, product]
                : current
        }.last
end

def image_merge(layers_flattened, column, image=[])
    if layers_flattened.empty?
        result = image.each_slice(column).to_a
    else
        result = image_merge(
            layers_flattened[0, layers_flattened.size - 1],
            column,
            image.empty? \
                ? layers_flattened.last
                : image.map.with_index {|pixel, idx| 
                    layers_flattened.last[idx] != PIXEL_TRANSPARENT \
                        ? layers_flattened.last[idx]
                        : pixel
                })
    end
end

def image_merge_layers(image_raw, column, row)
    image_merge(
        image_build(image_parse_data(image_raw), column, row).map {|x| x.flatten},
        column)
end