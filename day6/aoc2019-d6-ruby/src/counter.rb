def destination_found(candidates, destination)
    candidates.select {|incoming|
        incoming.last.include? destination
    }.size > 0
end

def map_build_tree(map)
    result = {}

    map.each{|parent, child|
        result[parent] = result.fetch(parent, []) << child
    }

    result
end

def map_find_path(tree_hash, find_indirect, path=['COM'], paths=[])
    result = paths

    if tree_hash.key?(path.last) == false
        result = paths
    else
        result = tree_hash[path.last]
            .reduce(paths) {|current, incoming|
                current \
                + (find_indirect \
                    ? path.map {|origin| [origin, incoming]}
                    : [[path.last, incoming]]) \
                + map_find_path(
                    tree_hash,
                    find_indirect,
                    path + [incoming],
                    [])
            }
    end

    return result
end

def map_find_route(paths, origin, destination, candidates=[])
    result = []

    if destination_found(candidates, destination)
        candidates_new = candidates.select{|route|
            route.last.include? destination
        }
        shortest = candidates_new.map {|route| route.size}.min

        result = candidates_new.select{|route| route.size == shortest}.first[1, shortest - 2]
    else
        candidates_new = []

        if candidates.empty?
            candidates_new = paths.select {|incoming|
                    incoming.include? origin
                }
                .reduce(candidates) {|current, incoming|
                    current + [[(incoming.first == origin \
                        ? incoming
                        : incoming.reverse)]]
                }
        else
            candidates_new = candidates.reduce([]) {|current, route|
                current + paths.select {|incoming|
                        (incoming.include? route.last.last) \
                            && !(incoming.include? route.last.first)
                    }
                    .map {|incoming|
                        route + [(incoming.first == route.last.last \
                            ? incoming
                            : incoming.reverse)]
                    }
            }
        end

        result = map_find_route(paths, origin, destination, candidates_new)

    end

    result
end

def map_parse(map_raw)
    map_build_tree(map_raw.map {|line|
        line.strip()
            .split(')')
    })
end

def orbit_count(map_raw)
    orbit_paths(map_parse(map_raw)).size
end

def orbit_count_hops(map_raw, origin, dest)
    map_find_route(orbit_paths(map_parse(map_raw), false), origin, dest).size
end

def orbit_paths(tree_hash, find_indirect=true)
    map_find_path(tree_hash, find_indirect)
end