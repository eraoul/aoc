from copy import copy, deepcopy
from collections import defaultdict
from math import lcm

DEBUG = False


def log(*args, **kwargs):
    print(*args, **kwargs, flush=True) if DEBUG else None


def flatten(x):
    return [item for sublist in x for item in sublist]


with open('12.in') as f:
    lines = f.readlines()
    lines = [line.strip()[1:-1] for line in lines]
    lines = [line.split(', ') for line in lines]
    lines = [[int(x.split('=')[1]) for x in line] for line in lines]
    data = [line + [0, 0, 0] for line in lines]

log(data)
N = len(data)

STEPS = 1000  # 1000


def compute_gravity(a, b):
    a1, a2, a3, a4, a5, a6 = a
    b1, b2, b3, b4, b5, b6 = b

    d1, d2, d3 = b1-a1, b2-a2, b3-a3

    g1 = g2 = g3 = 0
    h1 = h2 = h3 = 0

    if d1 > 0:
        g1 += 1
        h1 -= 1
    elif d1 < 0:
        g1 -= 1
        h1 += 1

    if d2 > 0:
        g2 += 1
        h2 -= 1
    elif d2 < 0:
        g2 -= 1
        h2 += 1

    if d3 > 0:
        g3 += 1
        h3 -= 1
    elif d3 < 0:
        g3 -= 1
        h3 += 1

    return (g1, g2, g3), (h1, h2, h3)


def apply_velocity(a):
    a1, a2, a3, a4, a5, a6 = a
    a1 += a4
    a2 += a5
    a3 += a6
    return [a1, a2, a3, a4, a5, a6]


def part1(data, part2=False):
    global STEPS
    data = deepcopy(data)

    print(data)

    if part2:
        STEPS = 9999999999999
        histories = [tuple(data[i]) for i in range(N)]
        # periods = [[0 for i in range(3)] for i in range(N)]
        periods = [0 for i in range(3)]
        print(histories)

    for s in range(STEPS):
        deltas = [[0 for i in range(3)] for j in range(N)]
        for a in range(N):
            for b in range(a+1, N):
                ga, gb = compute_gravity(data[a], data[b])
                for i in range(3):
                    deltas[a][i] += ga[i]
                    deltas[b][i] += gb[i]
        # apply gravity
        for a in range(N):
            for i in range(3):
                data[a][3+i] += deltas[a][i]

        # apply velocity
        for a in range(N):
            data[a] = apply_velocity(data[a])
            # print(s, histories, tda, periods)

        if s >= 0 and part2:
            for axis in range(3):
                per = periods[axis]
                if per > 0:
                    continue

                same = True
                for a in range(N):
                    tda = tuple(data[a])
                    if tda[axis] != histories[a][axis] or tda[axis+3] != 0:
                        same = False
                        break
                if not same:
                    continue

                periods[axis] = s + 1
                # periods[a][0] = s + 1
                #     print(s, histories, tda, periods)

                if all(periods):
                    return periods

        log(f'After {s+1} steps:')
        for a in range(N):
            log(data[a])

    return data


data1 = part1(data)
# print(data1)

ans = 0
for a in data1:
    ep = sum(abs(x) for x in a[:3])
    ek = sum(abs(x) for x in a[3:])
    e = ep * ek
    print(e)
    ans += e

print('part 1:', ans)

# part 2


def part2(data):
    periods = part1(data, True)

    print(periods)
    # print(flatten(periods))
    # print(lcm(*flatten(periods)))

    # print(list(zip(*periods)))
    # print([lcm(*p)for p in zip(*periods)])
    # print(lcm(*[lcm(*p)for p in zip(*periods)]))
    # print(lcm(*(max(p) for p in zip(*periods))))

    # return lcm(*(lcm(*x) for x in periods))

    return lcm(*periods)


ans = part2(data)

print('part 2:', ans)
