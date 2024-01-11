from copy import copy, deepcopy
from collections import defaultdict, Counter


with open('8.in') as f:
    lines = f.readlines()
    line = lines[0]
    data = [int(x) for x in line]

print(data)

# C = 3
# R = 2
C = 25
R = 6

layers = []

for i, c in enumerate(data):
    if i % (C * R) == 0:
        layers.append([])
    if i % C == 0:
        layers[-1].append([])
    layers[-1][-1].append(c)


def flatten(x):
    return [item for sublist in x for item in sublist]


best = float('inf')
best_layer = None
for layer in layers:
    # count 0s.)
    c = Counter(flatten(layer))
    if c[0] < best:
        best = c[0]
        best_layer = c

print('Part 1:', best_layer[1] * best_layer[2])

# part 2:

img = layers[0]

for layer in layers[1:]:
    for r in range(R):
        for c in range(C):
            if img[r][c] == 2:
                img[r][c] = layer[r][c]

for r in img:
    print(''.join('█' if x == 1 else ' ' for x in r))
