def map_build_tree(map)
    result = {}

    map.each{|parent, child|
        result[parent] = result.fetch(parent, []) << child
    }

    result
end

def map_find_path(tree_hash, path=['COM'], paths=[], depth=0)
    result = paths

    if tree_hash.key?(path.last) == false
        result = paths
    else
        result = tree_hash[path.last]
            .reduce(paths) {|current, incoming|
                current \
                + path.map {|origin|
                    [origin, incoming]
                } \
                + map_find_path(
                    tree_hash,
                    path + [incoming],
                    [],
                    depth + 1)
            }
    end

    return result
end

def map_parse(map_raw)
    map_build_tree(map_raw.map {|line|
        line.strip()
            .split(')')
    })
end

def orbit_count(map_raw)
    map_find_path(map_parse(map_raw)).size
end