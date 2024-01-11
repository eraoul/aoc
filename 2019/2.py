from copy import copy, deepcopy

with open('2.in') as f:
    lines = f.readlines()
    line = lines[0]
    program = [int(x) for x in line.split(",")]


print(program)
result = []


def intcode(program, noun, verb):
    data = deepcopy(program)

    data[1] = noun
    data[2] = verb

    ip = 0

    while data[ip] != 99:  # halt on code 99
        op = data[ip]
        arg1 = data[ip + 1]
        arg2 = data[ip + 2]
        arg3 = data[ip + 3]

        ref1 = data[arg1] if arg1 < len(data) else None
        ref2 = data[arg2] if arg2 < len(data) else None
        ref3 = data[arg3] if arg3 < len(data) else None

        if op == 1:
            data[arg3] = ref1 + ref2
            ip += 4

        elif op == 2:
            data[arg3] = ref1 * ref2
            ip += 4

        else:
            # print("unknown op", op)
            return None
    return data[0]


# part 1:
print(intcode(program, 12, 2))

# part 2:

for noun in range(100):
    for verb in range(100):
        if intcode(program, noun, verb) == 19690720:
            print(noun, verb)
            print(100 * noun + verb)
            break
