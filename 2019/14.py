from copy import copy, deepcopy
from collections import defaultdict
from math import ceil, lcm

DEBUG = True


def log(*args, **kwargs):
    print(*args, **kwargs, flush=True) if DEBUG else None


def flatten(x):
    return [item for sublist in x for item in sublist]


data = {}
with open('14.in') as f:
    lines = f.readlines()
    lines = [line.strip() for line in lines]
    lines = [line.split(' => ') for line in lines]
    for line in lines:
        l, r = line
        lhs = l.split(', ')
        lhs = [x.split() for x in lhs]
        lhs = [(int(x[0]), x[1]) for x in lhs]
        rhs = r.split()
        rhs = [int(rhs[0]), rhs[1]]
        data[rhs[1]] = (rhs[0], lhs)
for d in data:
    log(d, data[d])


def fuel_to_ore(needed_fuel):
    need = defaultdict(int)
    need['FUEL'] = needed_fuel
    nonnegative_needs = ['FUEL']
    while set(nonnegative_needs) != set(['ORE']):
        new_need = deepcopy(need)
        for n, amt in need.items():
            if n == 'ORE':
                continue
            # find the entry with this item on the rhs.
            # i.e. NEED 3C
            # 1A, 2B -> 2C
            # Rewrite:
            # multiplier = 2x
            # NEED 2A, 4B, -1C

            rhs = data[n]
            rhs_amt = rhs[0]
            multiplier = int(ceil(amt / rhs_amt))
            new_need[n] -= rhs_amt * multiplier
            for lhs_amt, lhs_item in rhs[1]:
                new_need[lhs_item] += lhs_amt * multiplier
        need = new_need
        nonnegative_needs = [x for x in need if need[x] > 0]

    return need['ORE']


ore = fuel_to_ore(1)
print('Part 1:', ore)

GOAL_ORE = 1e12

fuel = 1
best_fuel = fuel
new_fuel = GOAL_ORE / ore
best_diff = abs(GOAL_ORE - fuel_to_ore(fuel))
steps = 0
while steps < 3:
    new_fuel = int(fuel * GOAL_ORE / ore)

    new_ore = fuel_to_ore(new_fuel)
    diff = abs(GOAL_ORE - new_ore)
    print(f'{new_fuel=}, {ore=}, {diff=}')

    steps += 1
    if diff < best_diff:
        best_diff = diff
        best_fuel = new_fuel
        fuel = new_fuel
        steps = 0

    if steps == 2:
        fuel += 1

    ore = new_ore


print(fuel)
