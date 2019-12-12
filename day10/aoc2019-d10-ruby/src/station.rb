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
            map_raw[y][x] == '#' \
                ? asteroids + [[x, y]]
                : asteroids)
    end

    result
end

def pair_find_between(pair, asteroids)
    [pair, asteroids.select{|incoming|
            result = false

            if (pair.last.first - pair.first.first) != 0
                # m = (y2 - y1) / (x2 - x1)
                m = (pair.last.last - pair.first.last).to_f / (pair.last.first - pair.first.first).to_f

                # m(X - x1) + y1
                y = m * (incoming.first - pair.first.first) + pair.first.last

                result = pair.include?(incoming) == false \
                    && incoming.last == y \
                    && asteroid_is_between_pair(incoming, pair)
            else
                result = pair.include?(incoming) == false \
                    && (incoming.first == pair.first.first) \
                    && incoming.last.between?(*[pair.first.last, pair.last.last].sort)
            end

            result
        }]
end

def asteroid_is_between_pair(asteroid, pair)
    Math.sqrt((pair.last.first - pair.first.first) ** 2 + (pair.last.last - pair.first.last) ** 2).round(10) \
    == (Math.sqrt((asteroid.first - pair.first.first) ** 2 + (asteroid.last - pair.first.last) ** 2) \
        + Math.sqrt((asteroid.first - pair.last.first) ** 2 + (asteroid.last - pair.last.last) ** 2)).round(10)
end

def asteroids_pair_find_middle(asteroids)
    Parallel.map(asteroids.combination(2)) {|pair|
            pair_find_between(pair, asteroids)
        }
        .select {|incoming| incoming.last.size > 0}
end

def asteroids_pair_has_obstacle(origin, target, pairs)
    pairs.select {|pair, _|
        pair.include?(origin) && pair.include?(target)
    }.size > 0
end

def station_find_best(map_raw)
    asteroids = map_parse(map_raw)
    pairs = asteroids_pair_find_middle(asteroids)

    Parallel.map(asteroids) {|asteroid|
            [asteroid,
             asteroids
                .select {|x| x != asteroid}
                .select {|target|
                    asteroids_pair_has_obstacle(asteroid, target, pairs) == false
                }]
        }
        .reduce([[], 0]) {|current, incoming|

            incoming.last.size > current.last \
                ? [incoming.first, incoming.last.size]
                : current
        }
end