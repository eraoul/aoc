start, end = 165432, 707912


def run(PART2):
    count = 0
    for n in range(start, end+1):
        s = str(n)

        # has double:
        for c1, c2 in zip(s, s[1:]):
            if c1 == c2:
                break
        else:
            continue

        if PART2:
            found = False
            c = None
            cnt = 0
            for i in range(len(s)):
                c_cur = s[i]
                if not c:
                    c = c_cur
                    cnt = 1
                elif c_cur == c:
                    cnt += 1
                    if cnt == 2:
                        # have double
                        found = True
                    if cnt == 3:
                        # have triple.
                        found = False
                else:
                    if cnt == 2:
                        break
                    c = c_cur
                    cnt = 1

            if not found:
                continue

        prev = -1
        nondecreasing = True
        for c in s:
            i = int(c)
            if i < prev:
                nondecreasing = False
                break
            prev = i
        if nondecreasing:
            print(n)
            count += 1
    return count


print('Part 1:', run(False))
print('Part 2:', run(True))
