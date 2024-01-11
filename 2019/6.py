from copy import copy, deepcopy
from collections import defaultdict

with open('6.in') as f:
    lines = f.readlines()
    data = [line.strip().split(')') for line in lines]


print(data)
result = []

G = defaultdict(str)  # map child string to parent string

for p, c in data:
    G[c] = p

total = 0
for child in G.keys():
    while G[child] != 'COM':
        total += 1
        child = G[child]
    total += 1

# print(result)

print(f'Part 1: {total}')

# part 2

# compute sum of distnaces from YOU and SAN to nearest common ancestor
# find ancestor

ancestors = []
child = 'SAN'
while G[child] != 'COM':
    p = G[child]
    ancestors.append(p)
    child = p
ancestors.append('COM')

dist_from_you = 0
child = 'YOU'
while G[child] != 'COM':
    p = G[child]
    dist_from_you += 1
    child = p
    if p in ancestors:
        break

dist_from_san = ancestors.index(p)

print(dist_from_you, dist_from_san)
print('Part 2:', dist_from_you + dist_from_san - 1)
