from copy import copy, deepcopy
from collections import defaultdict, deque
from time import sleep
import random

DEBUG = False


def log(*args, **kwargs):
    print(*args, **kwargs, flush=True) if DEBUG else None


with open('15.in') as f:
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

        # arg_idx1 = get_arg_index_with_mode(modes[0], arg1, rb)
        # arg_idx2 = get_arg_index_with_mode(modes[1], arg2, rb)
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


outdata = defaultdict(lambda: ' ')


# north (1), south (2), west (3), and east (4).
dirs = ((-1, 0), (1, 0), (0, -1), (0, 1))

opposite_dir = (1, 0, 3, 2)


def run_sim():
    r, c = 0, 0
    next_dir_idx = None

    m = intcode(program)
    next(m)  # prime the generator

    # Accept a movement command via an input instruction.
    # Send the movement command to the repair droid.
    # Wait for the repair droid to finish the movement operation.
    # Report on the status of the repair droid via an output instruction.

    phase = 0  # 0==make map. 1==search map.
    to_visit = [(r, c, dir) for dir in range(4)]
    backtrack = []
    oxygen = None
    while True:
        try:
            log('\n========\nLoop start.')

            # Choose a new direction.
            if phase == 0:
                if not to_visit:
                    # phase 0 complete
                    phase = 1
                else:
                    goal_r, goal_c, goal_d = to_visit[-1]
                    # print(f'{goal_r}, {goal_c}, {goal_d}')
                    if (r, c) == (goal_r, goal_c):
                        # arrived at goal
                        to_visit.pop()
                        next_dir_idx = goal_d
                        backtrack.append(opposite_dir[goal_d])
                    else:
                        # not at goal yet. Backtrack more.
                        next_dir_idx = backtrack.pop()
                        # print('backtracking:', next_dir_idx)
            if phase == 1:
                # in phase 1.
                break

            # print(f'send', next_dir_idx+1)
            m.send(next_dir_idx + 1)
            output = None
            while output == None:
                # print('next')
                output = next(m)
            # print('got', output)
            next(m)
            dr, dc = dirs[next_dir_idx]
            nr, nc = r + dr, c + dc

            if output == 0:  # hit wall. record but don't move.
                outdata[(nr, nc)] = '█'
                # no need to backtrack since we didnt' move.
                backtrack.pop()
            elif output == 1 or output == 2:  # moved.
                r, c = nr, nc  # move to new spot
                # Add new spots to visit.
                for dir in range(4):
                    dr, dc = dirs[dir]
                    new_r, new_c = r + dr, c + dc
                    new_val = outdata[(new_r, new_c)]
                    if new_val == ' ':
                        to_visit.append((r, c, dir))
                if output == 1:
                    # explorable.
                    outdata[(nr, nc)] = '.'
                if output == 2:
                    # found oxygen.
                    outdata[(nr, nc)] = 'O'
                    oxygen = nr, nc
            else:
                raise Exception(f'output={output}')

        except StopIteration:
            break

        # draw_data(r, c)
        # sleep(.01)
    return oxygen


def draw_data(cur_r, cur_c, outdata=outdata):
    print("\033c", end="\033[A")

    maxr, maxc, minr, minc = 0, 0, 0, 0
    for r, c in outdata:
        maxr = max(maxr, r)
        maxc = max(maxc, c)
        minr = min(minr, r)
        minc = min(minc, c)

    print(minr, minc, maxr, maxc)

    for r in range(minr, maxr+1):
        for c in range(minc, maxc+1):
            if (r, c) == (cur_r, cur_c):
                print('X', end='')
            else:
                print(outdata[(r, c)], end='')

        print()


oxygen = run_sim()
draw_data(0, 0)

# Now run BFS from 0,0 to oxygen to find the shortest path.
new_map = deepcopy(outdata)


def bfs(fill_oxygen=False):
    to_visit = [(0, 0)] if not fill_oxygen else [oxygen]
    visited = []
    steps = 0
    found = False
    while True:
        # print(steps)
        new_to_visit = []
        for r, c in to_visit:
            if (r, c) in visited:
                continue
            visited.append((r, c))
            if not fill_oxygen:
                if (r, c) == oxygen:
                    found = True
                    break
            for dr, dc in dirs:
                new_r, new_c = r + dr, c + dc
                next_val = outdata[(new_r, new_c)]
                if next_val != '█':
                    new_to_visit.append((new_r, new_c))
                    if fill_oxygen:
                        new_map[(new_r, new_c)] = '░'
        if fill_oxygen:
            found = not new_to_visit
        if found:
            break
        to_visit = new_to_visit
        steps += 1
        if fill_oxygen:
            draw_data(oxygen[0], oxygen[1], new_map)
            sleep(0.08)
    return steps


steps = bfs()

print('part 1:', steps)


print('part 2:', bfs(True) - 1)  # fix off-by-one error
