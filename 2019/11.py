from copy import copy, deepcopy
from collections import defaultdict

DEBUG = False


def log(*args, **kwargs):
    print(*args, **kwargs, flush=True) if DEBUG else None


with open('11.in') as f:
    lines = f.readlines()
    line = lines[0]
    program = [int(x) for x in line.split(",")]


log(program)
result = []


def read_opcode(x):
    return x % 100


def read_modes(x):
    modes = [0] * 10
    i = 0
    x //= 100
    while x > 0:
        modes[i] = x % 10
        x //= 10
        i += 1

    for m in modes:
        assert m in [0, 1, 2]

    return modes


def get_arg_index_with_mode(mode, arg, rb):
    if mode == 2:
        return arg + rb
    return arg


def get_arg_with_mode(mode, arg, data, rb):
    arg_idx = get_arg_index_with_mode(mode, arg, rb)
    if mode == 0:  # position mode
        return data[arg_idx]
    elif mode == 1:  # immediate mode
        return arg
    elif mode == 2:  # relative mode
        return data[arg_idx]
    else:
        assert False


def intcode(program, machine_id=0):
    data = defaultdict(int)
    for i, n in enumerate(program):
        data[i] = n

    ip = 0
    rb = 0   # relative base

    while read_opcode(data[ip]) != 99:  # halt on code 99
        # log(data)
        zz = data[ip]
        op = read_opcode(zz)
        modes = read_modes(zz)

        arg1 = data[ip + 1]
        arg2 = data[ip + 2]
        arg3 = data[ip + 3]

        arg_idx1 = get_arg_index_with_mode(modes[0], arg1, rb)
        arg_idx2 = get_arg_index_with_mode(modes[1], arg2, rb)
        arg_idx3 = get_arg_index_with_mode(modes[2], arg3, rb)

        log(
            f'\nip={ip}, opcode {op}, modes {modes[:3]}, args {arg1}, {arg2}, {arg3}')
        args = [arg1, arg2, arg3]

        vals = []
        for i in range(3):
            vals.append(get_arg_with_mode(modes[i], args[i], data, rb))
        val1, val2, val3 = vals

        log(f'vals {val1}, {val2}, {val3}')

        if op == 1:  # add and store
            log(f'Store {val1 + val2} in {arg_idx3}'),
            data[arg_idx3] = val1 + val2
            assert modes[2] != 1
            ip += 4

        elif op == 2:  # multiply and store
            log(f'Store {val1 * val2} in {arg_idx3}'),
            data[arg_idx3] = val1 * val2
            assert modes[2] != 1
            ip += 4

        elif op == 3:  # input and store
            log(f'[{machine_id=}] Reading input...waiting...')
            data[arg1] = yield
            log(f'[{machine_id=}] Read input {data[arg1]} and store in {arg1}')
            assert modes[0] != 1
            ip += 2

        elif op == 4:  # output value
            log(f'Output {val1}'),
            yield val1
            log(f'[{machine_id=}] continuing after Output {val1}')
            ip += 2

        elif op == 5:  # jump if true
            log(f'Jump if {val1} != 0 to {val2}')
            if val1 != 0:
                ip = val2
            else:
                ip += 3

        elif op == 6:  # jump if false
            log(f'Jump if {val1} == 0 to {val2}')
            if val1 == 0:
                ip = val2
            else:
                ip += 3

        elif op == 7:  # <
            log(
                f'Store less-than comparison of {val1} and {val2} in {arg_idx3}'),
            assert modes[2] != 1
            data[arg_idx3] = 1 if val1 < val2 else 0
            ip += 4

        elif op == 8:  # ==
            log(
                f'Store equals comparison of {val1} and {val2} in {arg_idx3}')
            assert modes[2] != 1
            data[arg_idx3] = 1 if val1 == val2 else 0
            ip += 4

        elif op == 9:  # adjust relative base
            log(f'Adjust relative base by {val1}'),
            rb += val1
            ip += 2

        else:
            # unknown opcode
            log('Unknown opcode', op)
            return None
    # log(data)
    # return output
    log(f'Machine {machine_id} halted')


# part 1:
# R = 5
# C = 5

# data = [['.' for _ in range(C)] for _ in range(R)]

data = defaultdict(lambda: 0)


# def pp():
#     for r in data:
#         print(''.join(r))


# pp()

dirs = ((-1, 0), (0, 1), (1, 0), (0, -1))


def run_paintbot():
    r, c = 0, 0
    dir_idx = 0

    m = intcode(program)
    next(m)

    while True:
        color = m.send(data[(r, c)])

        data[(r, c)] = color
        try:
            turn = next(m)
            next(m)
        except StopIteration:
            break

        dir_idx = (dir_idx + (1 if turn == 1 else -1)) % 4
        dr, dc = dirs[dir_idx]
        r, c = r + dr, c + dc
        # print(r, c, dir_idx, color)
        # print(dir_idx)


def draw_data():
    maxr, maxc, minr, minc = 0, 0, 0, 0
    for r, c in data:
        maxr = max(maxr, r)
        maxc = max(maxc, c)
        minr = min(minr, r)
        minc = min(minc, c)

    print(minr, minc, maxr, maxc)

    for r in range(minr, maxr+1):
        for c in range(minc, maxc+1):
            if (r, c) in data and data[(r, c)] == 1:
                print('█', end='')
            else:
                print(' ', end='')
        print()


run_paintbot()
draw_data()

print('part 1:', len(data))

# part 2:
data = defaultdict(lambda: 0)
data[(0, 0)] = 1

print('part 2:')
run_paintbot()
draw_data()
