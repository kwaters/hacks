#!/usr/bin/env python

def pair_iterator(l):
    if not l:
        yield []
        return
    for i, second in enumerate(l[1:]):
        # N.B. i is one less than the index
        for rest in pair_iterator(l[1:i + 1] + l[i + 2:]):
            yield [(l[0], second)] + rest

class Tile(object):
    def __init__(self, pairs):
        self.links = tuple(pairs)

    def rotate(self):
        # tile rotation group is (1 3 5 7)(2 4 6 8)
        rotated = []
        for first, second in self.links:
            first = ((first + 1) % 8) + 1
            second = ((second + 1) % 8) + 1
            if first > second:
                first, second = second, first
            rotated.append((first, second))
        rotated.sort(key=lambda x: x[0])
        return Tile(rotated)

    def __str__(self):
        return "".join("({0} {1})".format(*link) for link in self.links)

    def __lt__(lhs, rhs):
        return lhs.links < rhs.links

    def __eq__(lhs, rhs):
        if type(lhs) != type(rhs):
            return False
        return lhs.links == rhs.links
    def __ne__(lhs, rhs):
        return not (lhs == rhs)
    def __hash__(self):
        return hash(self.links)

class UnionFind(object):
    def __init__(self):
        self.nodes = {}

    def find(self, node):
        if node not in self.nodes:
            self.nodes[node] = None

        # find the node representing this object
        current = node
        while True:
            next = self.nodes[current]
            if next is None:
                break
            current = next

        # reparent the chain
        reparent = node
        while True:
            next = self.nodes[reparent]
            if next is None:
                break
            self.nodes[reparent] = current
            reparent = next

        return current

    def union(self, lhs, rhs):
        lhs = self.find(lhs)
        rhs = self.find(rhs)
        if lhs != rhs:
            self.nodes[lhs] = rhs

    def flatten(self):
        for node in self.nodes.iterkeys():
            self.find(node)

    def masters(self):
        for key, value in self.nodes.iteritems():
            if value is None:
                yield key

    def groups(self):
        self.flatten()
        for node in self.masters():
            group = [node]
            for key, value in self.nodes.iteritems():
                if value == node:
                    group.append(key)
            yield group


def main():
    uf = UnionFind()

    for tile in pair_iterator(list(range(1, 9))):
        tile = Tile(tile)
        uf.union(tile, tile.rotate())

    unique_tiles = []
    for group in uf.groups():
        group.sort()
        unique_tiles.append(group[0])

    unique_tiles.sort()
    for tile in unique_tiles:
        print tile

if __name__ == "__main__":
    main()
