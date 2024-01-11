from copy import copy, deepcopy

with open('5.in') as f:
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
        assert m in [0, 1]

    return modes


def intcode(program, inputs=[]):
    MAX_ARGS = 3
    data = deepcopy(program)
    data.extend([0] * MAX_ARGS)
    output = []

    ip = 0

    while read_opcode(data[ip]) != 99:  # halt on code 99
        # print(data)
        zz = data[ip]
        op = read_opcode(zz)
        modes = read_modes(zz)

        arg1 = data[ip + 1]
        arg2 = data[ip + 2]
        arg3 = data[ip + 3]
        print(
            f'\nip={ip}, opcode {op}, modes {modes[:3]}, args {arg1}, {arg2}, {arg3}')

        val1 = data[arg1] if modes[0] == 0 and arg1 < len(data) else arg1
        val2 = data[arg2] if modes[1] == 0 and arg2 < len(data) else arg2
        val3 = data[arg3] if modes[2] == 0 and arg3 < len(data) else arg3

        print(
            f'vals {val1}, {val2}, {val3}')

        if op == 1:  # add and store
            print(f'Store {val1 + val2} in {arg3}'),
            data[arg3] = val1 + val2
            assert modes[2] == 0
            ip += 4

        elif op == 2:  # multiply and store
            print(f'Store {val1 * val2} in {arg3}'),
            data[arg3] = val1 * val2
            assert modes[2] == 0
            ip += 4

        elif op == 3:  # input and store
            data[arg1] = inputs.pop(0)
            print(f'Read input {data[arg1]} and store in {arg1}')
            assert modes[0] == 0
            ip += 2

        elif op == 4:  # output value
            print(f'Output {val1}'),
            output.append(val1)
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
            print('Unknown opcode', op)
            return None
    # print(data)
    return output


# part 1:
print(intcode(program, [1]))

# part 2:
print(intcode(program, [5]))
