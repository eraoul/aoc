from copy import copy, deepcopy
from collections import defaultdict

with open('9.in') as f:
    lines = f.readlines()
    line = lines[0]
    program = [int(x) for x in line.split(",")]


print(program)
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


def intcode(program, inputs=[]):
    MAX_ARGS = 3
    # data = deepcopy(program)
    # data.extend([0] * MAX_ARGS)

    data = defaultdict(int)
    for i, n in enumerate(program):
        data[i] = n

    output = []

    ip = 0
    rb = 0   # relative base

    while read_opcode(data[ip]) != 99:  # halt on code 99
        # print(data)
        zz = data[ip]
        op = read_opcode(zz)
        modes = read_modes(zz)

        arg1 = data[ip + 1]
        arg2 = data[ip + 2]
        arg3 = data[ip + 3]

        arg_idx1 = get_arg_index_with_mode(modes[0], arg1, rb)
        arg_idx2 = get_arg_index_with_mode(modes[1], arg2, rb)
        arg_idx3 = get_arg_index_with_mode(modes[2], arg3, rb)

        print(
            f'\nip={ip}, opcode {op}, modes {modes[:3]}, args {arg1}, {arg2}, {arg3}')
        args = [arg1, arg2, arg3]

        vals = []
        for i in range(3):
            vals.append(get_arg_with_mode(modes[i], args[i], data, rb))
        val1, val2, val3 = vals

        print(f'vals {val1}, {val2}, {val3}')

        if op == 1:  # add and store
            print(f'Store {val1 + val2} in {arg_idx3}'),
            data[arg_idx3] = val1 + val2
            assert modes[2] != 1
            ip += 4

        elif op == 2:  # multiply and store
            print(f'Store {val1 * val2} in {arg_idx3}'),
            data[arg_idx3] = val1 * val2
            assert modes[2] != 1
            ip += 4

        elif op == 3:  # input and store
            data[arg_idx1] = inputs.pop(0)
            print(f'Read input {data[arg_idx1]} and store in {arg_idx1}')
            assert modes[0] != 1
            ip += 2

        elif op == 4:  # output value
            print(f'Output {val1}'),
            output.append(val1)
            ip += 2

        elif op == 5:  # jump if true
            print(f'Jump if {val1} != 0 to {val2}')
            if val1 != 0:
                ip = val2
            else:
                ip += 3

        elif op == 6:  # jump if false
            print(f'Jump if {val1} == 0 to {val2}')
            if val1 == 0:
                ip = val2
            else:
                ip += 3

        elif op == 7:  # <
            print(
                f'Store less-than comparison of {val1} and {val2} in {arg_idx3}'),
            assert modes[2] != 1
            data[arg_idx3] = 1 if val1 < val2 else 0
            ip += 4

        elif op == 8:  # ==
            print(
                f'Store equals comparison of {val1} and {val2} in {arg_idx3}')
            assert modes[2] != 1
            data[arg_idx3] = 1 if val1 == val2 else 0
            ip += 4

        elif op == 9:  # adjust relative base
            print(f'Adjust relative base by {val1}'),
            rb += val1
            ip += 2

        else:
            # unknown opcode
            print('Unknown opcode', op)
            return None
    # print(data)
    return output


# part 1:
print(intcode(program, [1]))

# part 2:
print(intcode(program, [2]))
