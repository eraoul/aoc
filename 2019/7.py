from copy import copy, deepcopy
from itertools import permutations

DEBUG = False


def log(*args, **kwargs):
    print(*args, **kwargs, flush=True) if DEBUG else None


with open('7.in') as f:
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
        assert m in [0, 1]

    return modes


def intcode(program, machine_id=0):
    MAX_ARGS = 3
    data = deepcopy(program)
    data.extend([0] * MAX_ARGS)
    # output = []

    ip = 0

    while read_opcode(data[ip]) != 99:  # halt on code 99
        # log(data)
        zz = data[ip]
        op = read_opcode(zz)
        modes = read_modes(zz)

        arg1 = data[ip + 1]
        arg2 = data[ip + 2]
        arg3 = data[ip + 3]
        log(
            f'\nip={ip}, opcode {op}, modes {modes[:3]}, args {arg1}, {arg2}, {arg3}')

        val1 = data[arg1] if modes[0] == 0 and arg1 < len(data) else arg1
        val2 = data[arg2] if modes[1] == 0 and arg2 < len(data) else arg2
        val3 = data[arg3] if modes[2] == 0 and arg3 < len(data) else arg3

        log(f'vals {val1}, {val2}, {val3}')

        if op == 1:  # add and store
            log(f'Store {val1 + val2} in {arg3}'),
            data[arg3] = val1 + val2
            assert modes[2] == 0
            ip += 4

        elif op == 2:  # multiply and store
            log(f'Store {val1 * val2} in {arg3}'),
            data[arg3] = val1 * val2
            assert modes[2] == 0
            ip += 4

        elif op == 3:  # input and store
            # data[arg1] = inputs.pop(0)
            log(f'[{machine_id=}] Reading input...waiting...')
            data[arg1] = yield
            log(f'[{machine_id=}] Read input {data[arg1]} and store in {arg1}')
            assert modes[0] == 0
            ip += 2

        elif op == 4:  # output value
            log(f'Output {val1}'),
            # output.append(val1)
            yield val1
            log(f'[{machine_id=}] continuing after Output {val1}')
            ip += 2

        elif op == 5:  # jump if true
            if val1 != 0:
                ip = val2
            else:
                ip += 3

        elif op == 6:  # jump if false
            if val1 == 0:
                ip = val2
            else:
                ip += 3

        elif op == 7:  # <
            assert modes[2] == 0
            data[arg3] = 1 if val1 < val2 else 0
            ip += 4

        elif op == 8:  # ==
            assert modes[2] == 0
            data[arg3] = 1 if val1 == val2 else 0
            ip += 4

        else:
            # unknown opcode
            log('Unknown opcode', op)
            return None
    # log(data)
    # return output
    log(f'Machine {machine_id} halted')


def part1():
    p = permutations([0, 1, 2, 3, 4], 5)

    best = float('-inf')
    for phases in p:
        next_input = 0
        log(f'\npermutation: {phases}')
        for phase in phases:
            output = intcode(program, [phase, next_input])[0]
            log(output)
            next_input = output
        best = max(best, next_input)
    return best


def part2():
    p = permutations([5, 6, 7, 8, 9], 5)
    # p = [(9, 8, 7, 6, 5)]
    first = True
    best = float('-inf')
    final_output = -1
    for phases in p:
        log(f'\npermutation: {phases}')
        running = True

        # set up the machines.
        machines = []
        for i, phase in enumerate(phases):
            log(f'Creating machine {i} with phase {phase}')
            m = intcode(program, machine_id=i)
            m.send(None)  # start the generator
            m.send(phase)  # set the phase for each machine.
            machines.append(m)

        next_input = 0
        i = 0
        while running:
            log(f'loop {i}')
            i += 1
            for m_idx, m in enumerate(machines):
                log(f'\nmachine {m_idx} continuing with {next_input=}')
                # next(m)
                if i > 1:
                    try:
                        next(m)
                    except StopIteration:
                        running = False
                        break
                output = m.send(next_input)
                # output = next(m)
                log(f'[machine {m_idx}] {output=}')
                next_input = output
                # print(output)
            if output:
                final_output = next_input
            else:
                running = False
        if final_output > best:
            print('new best=', final_output, phases)
        best = max(best, final_output)
    return best


# # part 1:
# print('Part 1:', part1())

# # part 2:
print('Part 2:', part2())
