require 'parallel'

def map_parse(map_raw, x=0, y=0, asteroids=[])
    result = []

    if x == map_raw.first.length && y == map_raw.size - 1
        result = asteroids
    elsif x == map_raw.first.length
        result = map_parse(map_raw, 0, y + 1, asteroids)
    else
        result = map_parse(
            map_raw,
            x + 1,
            y,
            map_raw[y][x] != '.' \
                ? asteroids + [[x, y]]
                : asteroids)
    end

    result
end

def pair_find_between(pair, asteroids)
    [pair, asteroids
        .select {|incoming| pair.include?(incoming) == false}
        .select {|incoming|
            result = false

            if pair.last.first == pair.first.first
                # straight line
                result = (incoming.first == pair.first.first) \
                    && incoming.last.between?(*[pair.first.last, pair.last.last].sort)
            elsif pair.last.last == pair.first.last
                # horizontal line
                result = (incoming.last == pair.first.last) \
                    && incoming.first.between?(*[pair.first.first, pair.last.first].sort)
            else
                # m = (y2 - y1) / (x2 - x1)
                m = (pair.last.last - pair.first.last).to_f / (pair.last.first - pair.first.first).to_f

                # m(X - x1) + y1
                y = m * (incoming.first - pair.first.first) + pair.first.last

                result = incoming.last == y \
                    && asteroid_is_between_pair(incoming, pair)
            end

            result
        }]
end

def pair_is_neighbour(alpha, beta)
    (alpha.first - beta.first).abs == 1 \
        || (alpha.last - beta.last).abs == 1
end

def asteroid_is_between_pair(asteroid, pair)
    asteroids_pair_find_distance(*pair).round(10) \
    == (asteroids_pair_find_distance(asteroid, pair.first) \
        + asteroids_pair_find_distance(asteroid, pair.last)).round(10)
end

def asteroids_pair_find_distance(alpha, beta)
    Math.sqrt((alpha.first - beta.first) ** 2 + (alpha.last - beta.last) ** 2)
end

def asteroids_pair_find_angle(alpha, beta)
    zero_point = [alpha.first, 0]
    #zero_vector = [zero_point.first - alpha.first, zero_point.last - alpha.last]
    #zero_magnitude = Math.sqrt(zero_vector.first ** 2 + zero_vector.last ** 2)

    #vector = [beta.first - alpha.first, beta.last - alpha.last]
    #magnitude = Math.sqrt(vector.first ** 2 + vector.last ** 2)

    #dot_product = zero_vector.first * vector.first + zero_vector.last * vector.last

    #angle = Math.acos(dot_product / (zero_magnitude * magnitude))

    #a = beta.first < alpha.first \
    #    ? 360 - angle
    #    : angle
    (360 + Math.atan2(beta.last - alpha.last, beta.first - alpha.first) \
        - Math.atan2(zero_point.last - alpha.last, zero_point.first - alpha.first)) \
        % 360
end

def asteroids_pair_find_middle(asteroids)
    Hash[asteroids.combination(2)
        .select {|pair| !pair_is_neighbour(*pair)}
        .map {|pair|
            pair_find_between(pair, asteroids)
        }
        .select {|incoming| incoming.last.size > 0}
        .map {|incoming|
            [asteroids_pair_hash(incoming.first.sort), incoming.last]
        }]
end

def asteroids_pair_hash(pair_sorted)
    pair_sorted.flatten.join('|')
end

def station_get_best(asteroids, pairs)
    Parallel.map(asteroids) {|asteroid|
            [asteroid,
             asteroids
                .select {|x| x != asteroid}
                .select {|target|
                    pairs.fetch(asteroids_pair_hash([asteroid, target].sort), []).size == 0
                }]
        }
        .reduce([[], 0]) {|current, incoming|
            incoming.last.size > current.last \
                ? [incoming.first, incoming.last.size]
                : current
        }
end

def station_find_best(map_raw)
    asteroids = map_parse(map_raw)

    station_get_best(asteroids, asteroids_pair_find_middle(asteroids))
end

def station_run_vaporizer(asteroids, pointer=0, angle=-1, sequence=[])
    result = []

    if asteroids.empty?
        result = sequence
    elsif asteroids[pointer].first == angle
        pointer_new = (pointer + 1) % asteroids.size
        result = station_run_vaporizer(
            asteroids,
            pointer_new,
            pointer_new == 0 ? -1 : angle,
            sequence)
    else
        pointer_new = asteroids.size == 1 \
            ? 0
            : (pointer % (asteroids.size - 1))

        result = station_run_vaporizer(
            asteroids.select.with_index {|_, idx| idx != pointer},
            pointer_new,
            asteroids[pointer].first,
            sequence + [asteroids[pointer].last])
    end

    result
end

def station_vaporize_asteroids(map_raw)
    asteroids = map_parse(map_raw)

    station = station_get_best(asteroids, asteroids_pair_find_middle(asteroids)).first

    station_run_vaporizer(asteroids.select {|x| x != station}
        .map {|asteroid|
            [asteroids_pair_find_angle(station, asteroid).round(7),
             asteroids_pair_find_distance(station, asteroid).round(7)] \
                + [asteroid]
        }
        .sort)
end