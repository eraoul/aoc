from copy import copy, deepcopy
from collections import defaultdict
from time import sleep
DEBUG = False


def log(*args, **kwargs):
    print(*args, **kwargs, flush=True) if DEBUG else None


with open('13.in') as f:
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
            log(f'[{machine_id=}] -------------------> Reading input...waiting...')
            data[arg1] = yield
            log(
                f'[{machine_id=}]  <------ Received input {data[arg1]} and store in {arg1}')
            yield  # don't require caller to store the result of "send"
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

outdata = defaultdict(lambda: 0)


# def pp():
#     for r in data:
#         print(''.join(r))


# pp()

dirs = ((-1, 0), (0, 1), (1, 0), (0, -1))


def find_ball(outdata):
    for k, v in outdata.items():
        if v == 4:
            return k
    raise Exception("Can't find ball")


def find_paddle(outdata):
    for k, v in outdata.items():
        if v == 3:
            return k
    raise Exception("Can't find paddle")


def run_game():
    r, c = 0, 0
    dir_idx = 0

    m = intcode(program)

    initializing = True
    joystick = None
    while True:
        try:
            log('\n========\nLoop start.')
            # if joystick is not None:
            #     c = m.send(joystick)
            # else:
            #     c = next(m)
            c = next(m)
            r = next(m)
            id = next(m)
        except StopIteration:
            break

        outdata[(r, c)] = id
        # print(r, c, id)
        if (initializing and r == 0 and c == -1) or (not initializing and id == 4):
            # if id == 4 and initializing:
            #     continue
            # elif id == 4:
            #     print('ball found.')
            # next(m)
            # time to send joystick.
            initializing = False
            # if r == 0 and c == -1:
            #     print(f'r,c == (0,-1)')
            # Time to move the joystick.
            br, bc = find_ball(outdata)
            pr, pc = find_paddle(outdata)
            joystick = 0
            if bc > pc:
                joystick = 1
            elif bc < pc:
                joystick = -1
            c = next(m)
            # print(f'here4: {c=}')
            # print(f'----------> sending {joystick}...')
            draw_data()
            sleep(0.05)
            m.send(joystick)
            # print(f'here2. {br=} {bc=} {pr=} {pc=} joystick', joystick)
        # elif id == 4 and not initializing:
        #     print('Ball found.')
        #     next(m)
        #     print('HERE')


def draw_data():
    print("\033c", end="\033[A")
    # print("\033c", flush=True)
    maxr, maxc, minr, minc = 0, 0, 0, 0
    for r, c in outdata:
        maxr = max(maxr, r)
        maxc = max(maxc, c)
        minr = min(minr, r)
        minc = min(minc, c)

    print(minr, minc, maxr, maxc)

    for r in range(minr, maxr+1):
        for c in range(minc, maxc+1):
            if (r, c) not in outdata:
                print(' ', end='')
                continue
            v = outdata[(r, c)]
            if v == 0:
                print(' ', end='')
            elif v == 1:
                print('█', end='')
            elif v == 2:
                print('X', end='')
            elif v == 3:
                print('=', end='')
            elif v == 4:
                print('o', end='')
            else:
                print(f'SCORE: {v}')
        print()


# run_game()
# draw_data()

# blocks = sum(1 for r, c in data if data[(r, c)] == 2)

# print('part 1:', blocks)

# part 2:
program[0] = 2  # insert 2 quarters
outdata = defaultdict(lambda: 0)
run_game()
# draw_data()
print('Part 2: Final score', outdata[(0, -1)])
