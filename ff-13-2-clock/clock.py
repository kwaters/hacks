#!/usr/bin/env python

"""Clock puzzle sover for FF XIII-2."""

import argparse
import pprint

import exactcover

def create_grid(clock):
    """Turn the clock into an exact cover problem."""
    size = len(clock)
    m = []

    # Each of the two moves from each number
    for i, v in enumerate(clock):
        m.append([(0, i), (1, (i - v) % size)])
        if v * 2 != size:
            m.append([(0, i), (1, (i + v) % size)])

    # The first and last numbers are special
    for i in xrange(size):
        m.append([2, (0, i)])
        m.append([3, (1, i)])

    return m

def print_solution(clock, covering):
    """Print the solution coresponding to a covering."""
    mapping = {}
    for source, dest in covering:
        if source == 3:
            start = dest[1]
        elif source == 2:
            end = dest[1]
        else:
            mapping[source[1]] = dest[1]

    chain = [start]
    while chain[-1] != end:
        chain.append(mapping[chain[-1]])

    # Not all coverings form a valid solution.  Some will contain an
    # unconnected cycle.
    if len(chain) != len(clock):
        return

    print ' -> '.join('{}({})'.format(i, clock[i]) for i in chain)


def main():
    args = argparse.ArgumentParser()
    args.add_argument('clock', type=int, nargs='+')
    opts = args.parse_args()

    clock = opts.clock

    m = create_grid(clock)
    for cover in exactcover.Coverings(m):
        print_solution(clock, cover)


if __name__ == '__main__':
    main()
