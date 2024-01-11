with open('1.in') as f:
    lines = f.readlines()
    lines = [int(line.strip()) for line in lines]


print(lines)
result = []

for n in lines:
    s = 0
    while n > 0:
        n = n//3-2
        if n > 0:
            s += n
    result.append(s)
print(sum(result))
