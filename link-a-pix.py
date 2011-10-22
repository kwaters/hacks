#!/usr/bin/env python

# Link-a-pix solver.  Not pretty.

grid = [
    '....22...1..4..8A..B',
    '..9.9.....4...A.....',
    '4..4..22.....E..5.5.',
    '322.1......8........',
    '.....1....22.6......',
    '3.3.1....3.3...6....',
    '7123..........E....B',
    '..2..5....3.3..1...4',
    '7...1....13.....9...',
    '.............3.3.94.',
    '....5.3...344......2',
    '..4..344...4..4..642',
    '.8.4....1....6..4...',
    '.8..3...............',
    '4.4...4....6....6...',
    '4..43.43..4....6.525',
    '.3.3.3.33....4..4.2.',
    '9...1..1....6....1.4',
    '.22..22..24..4..4.6.',
    '....9..1.2.1..6...4.',
]

def walk(grid, path, length):
    rows, cols = len(grid), len(grid[0])
    r, c = path[-1]

    if path[-1] in path[:-1]:
        return

    if len(path) == length:
        if grid[path[0][0]][path[0][1]] == grid[r][c] and path[0] < path[-1]:
            yield path
        else:
            return
    if len(path) > 1 and grid[r][c] != '.':
        return

    if r > 0:
        for w in walk(grid, path + [(r - 1, c)], length):
            yield w
    if r < rows - 1:
        for w in walk(grid, path + [(r + 1, c)], length):
            yield w
    if c > 0:
        for w in walk(grid, path + [(r, c - 1)], length):
            yield w
    if c < cols - 1:
        for w in walk(grid, path + [(r, c + 1)], length):
            yield w

def show(grid, path):
    out = list(list(c for c in row) for row in grid)
    for r, c in path:
        out[r][c] = '#'
    for row in out:
        print ''.join(row)

def go(grid, start):
    for w in walk(grid, [start], int(grid[start[0]][start[1]], 36)):
        yield w

def parts(grid):
    m = []

    for r, row in enumerate(grid):
        for c, value in enumerate(row):
            if value == '.':
                m.append([(r, c)])
                continue
            for w in go(grid, (r, c)):
                m.append(w)

    return m

m = parts(grid)

def sol(grid, cover):
    out = list(list(c for c in row) for row in grid)
    for path in cover:
        v = grid[path[0][0]][path[0][1]]
        for r, c in path:
            out[r][c] = v
    for row in out:
        print ''.join(row)




import exactcover
for cover in exactcover.Coverings(m):
    sol(grid, cover)
    print
