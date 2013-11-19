#!/usr/bin/env python

import pprint
import random

class Node(object):
    def __init__(self, name):
        self.name = name
        self.outgoing = set()

    def __eq__(lhs, rhs):
        return lhs.name == rhs.name
    def __hash__(self):
        return hash(self.name)

    def __repr__(self):
        return 'Node({!r})'.format(self.name)

    def link(self, dst):
        self.outgoing.add(dst)
    def unlink(self, dst):
        self.outgoing.remove(dst)


def linked(src, dst):
    return dst in src.outgoing


def draw(nodes):
    with open('out.dot', 'w') as f:
        print >>f, 'digraph G {'
        for node in nodes:
            print >>f, '"{}";'.format(node.name)

        for node in nodes:
            for outlink in node.outgoing:
                print >>f, '"{}" -> "{}" [constraint="false"];'.format(
                    node.name, outlink.name)

        for src, dst in zip(nodes, nodes[1:]):
            print >>f, '"{}" -> "{}" [style="invis"];'.format(
                src.name, dst.name)

        print >>f, '}'


def random_graph(nodecount, linkcount, sortable=False):
    nodes = [Node('n{}'.format(i)) for i in xrange(nodecount)]

    for _ in xrange(linkcount):
        while True:
            src, dst = random.sample(nodes, 2)
            if not linked(src, dst):
                src.link(dst)
                try:
                    topo_sort(nodes)
                    break
                except UnsortableException:
                    src.unlink(dst)

    return nodes


class UnsortableException(Exception): pass


def topo_sort(nodes):
    out = []
    marks = set()
    left = set(nodes)

    def visit(node):
        if node in marks:
            raise UnsortableException(repr(marks))
        if node not in marks and node in left:
            marks.add(node)
            for outlink in node.outgoing:
                visit(outlink)
            out.append(node)
            left.remove(node)
            marks.remove(node)

    while left:
        node = left.pop()
        left.add(node)
        visit(node)

    return out[::-1]


def main():
    g = random_graph(12, 28, True)
    g = topo_sort(g)
    draw(g)


if __name__ == '__main__':
    main()
