from collections import defaultdict
from copy import copy, deepcopy

data = []

with open('3.in') as f:
    lines = f.readlines()
    x = [line.split(',') for line in lines]
    for d in x:
        w = []
        for val in d:
            l, r = val[0], int(val[1:])
            w.append((l, r))
        data.append(w)


print(data)

dirs = {'U', 'D', 'L', 'R'}

dir_to_x = {
    'U': 0,
    'D': 0,
    'L': -1,
    'R': 1
}
dir_to_y = {
    'U': 1,
    'D': -1,
    'L': 0,
    'R': 0
}

result = []

pos_to_steps = defaultdict(list)
pos_to_wires = defaultdict(set)
intersections = set()

for i, w in enumerate(data):
    x, y = 0, 0
    step = 0
    for dir, n in w:
        for _ in range(n):
            x += dir_to_x[dir]
            y += dir_to_y[dir]
            step += 1
            pos = (x, y)
            if i not in pos_to_wires[pos]:
                # only add step at first time we fisit pos per wire
                pos_to_steps[pos].append(step)
                pos_to_wires[pos].add(i)

            if len(pos_to_wires[pos]) == 2:
                intersections.add(pos)


print('\nPart 1:')
print(intersections)
x, y = sorted(intersections, key=lambda z: abs(z[0]) + abs(z[1]))[0]

print(abs(x)+abs(y))

print('\nPart 2:')
for pos in intersections:
    result.append(sum(pos_to_steps[pos]))
print(min(result))
