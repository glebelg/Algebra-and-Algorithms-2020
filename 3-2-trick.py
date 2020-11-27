def trick(g, i, j, k):
    # lvl 1
    print(f'GATE {g + 1} AND {i} {j}')
    print(f'GATE {g + 2} AND {i} {k}')
    print(f'GATE {g + 3} AND {j} {k}')

    print(f'GATE {g + 4} OR {i} {j}')

    # lvl 2
    print(f'GATE {g + 5} OR {g + 1} {g + 2}')
    print(f'GATE {g + 6} OR {k} {g + 4}')

    # lvl 3
    print(f'GATE {g + 7} OR {g + 3} {g + 5}')

    # lvl 4
    print(f'GATE {g + 8} NOT {g + 7}')

    # lvl 5
    print(f'GATE {g + 9} AND {g + 6} {g + 8}')
    print(f'GATE {g + 10} AND {i} {g + 3}')

    # lvl 6
    print(f'GATE {g + 11} OR {g + 9} {g + 10}')

    return g + 11, g + 7


n = int(input())

x, y = [], []
g = 3 * n - 1

for i in range(n):
    x_i, y_i = trick(g, i, i + n, i + 2 * n)
    x.append(x_i)
    y.append(y_i)
    g = x_i

print(f'GATE {g + 1} NOT {0}')
print(f'GATE {g + 2} AND {0} {g + 1}')

for i in range(n):
    print(f'OUTPUT {i} {x[i]}')
print(f'OUTPUT {n} {g + 2}')

print(f'OUTPUT {n + 1} {g + 2}')
for i in range(n):
    print(f'OUTPUT {i + n + 2} {y[i]}')
