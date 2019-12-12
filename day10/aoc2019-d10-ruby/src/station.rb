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
    Math.sqrt((pair.last.first - pair.first.first) ** 2 + (pair.last.last - pair.first.last) ** 2).round(7) \
    == (Math.sqrt((asteroid.first - pair.first.first) ** 2 + (asteroid.last - pair.first.last) ** 2) \
        + Math.sqrt((asteroid.first - pair.last.first) ** 2 + (asteroid.last - pair.last.last) ** 2)).round(7)
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

def station_find_best(map_raw)
    asteroids = map_parse(map_raw)
    pairs = asteroids_pair_find_middle(asteroids)

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