from copy import copy, deepcopy
from collections import defaultdict, Counter
from math import gcd, atan2, pi
from time import sleep


with open('10.in') as f:
    lines = f.readlines()
    data = [line.strip() for line in lines]
    data = [[x for x in line] for line in data]


def pp(data):
    print()
    for r in data:
        print(''.join(r))


pp(data)

R = len(data)
C = len(data[0])


def atan2_n(y, x):
    """North is 0, east is 90, south is 180, west is 270"""
    ang = atan2(x, -y)
    if ang < 0:
        ang += 2 * pi
    return ang


def compute_dirs(r, c):
    dirs = set()
    for dy in range(-r, R-r):
        for dx in range(-c, C-c):
            if dy == 0 and dx == 0:
                continue
            div = gcd(abs(dy), abs(dx))
            dirs.add((dy//div, dx//div))

    # print(dirs)
    return sorted(list(dirs), key=lambda x: atan2_n(x[0], x[1]))


# ans = []
best = float('-inf')
argmax = None
for rr in range(R):
    for cc in range(C):
        count = 0
        if data[rr][cc] != '#':
            continue

        dirs = compute_dirs(rr, cc)

        for dr, dc in dirs:
            r, c = rr, cc
            while 0 <= r+dr < R and 0 <= c+dc < C:
                r += dr
                c += dc
                if data[r][c] == '#':
                    count += 1
                    break

        # ans.append(count)
        if count > best:
            best = count
            argmax = rr, cc

print('Part 1:', best, argmax)


def flatten(x):
    return [item for sublist in x for item in sublist]


rr, cc = argmax
data[rr][cc] = 'X'

i = 0
dirs = list(compute_dirs(rr, cc))
result = None
while '#' in flatten(data):
    for dr, dc in dirs:
        r, c = rr, cc
        while 0 <= r+dr < R and 0 <= c+dc < C:
            r += dr
            c += dc
            if data[r][c] == '#':
                data[r][c] = '.'
                i += 1
                pp(data)
                sleep(.01)
                break
        if i == 200:
            result = r, c
            # print('Part 2:', r + c * 100, c, r)
            # exit()

r, c = result
print('Part 2:', r, c, r + c * 100)
