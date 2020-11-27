def trick(g, i, j, k):
    # lvl 1
    print(f'GATE {g + 1} NOT {k}')  # -k

    print(f'GATE {g + 2} AND {i} {j}')  # ij
    print(f'GATE {g + 3} OR {i} {j}')  # i + j

    # lvl 2
    print(f'GATE {g + 4} NOT {g + 2}')  # -(ij)
    print(f'GATE {g + 5} NOT {g + 3}')  # -(i + j)

    print(f'GATE {g + 6} AND {k} {g + 3}')  # (i+j)k

    # lvl 3
    print(f'GATE {g + 7} OR {g + 2} {g + 6}')  # ij + (i+j)k -- y

    print(f'GATE {g + 8} AND {g + 3} {g + 4}')  # -(ij)(i + j) -- i xor j
    print(f'GATE {g + 9} OR {g + 2} {g + 5}')  # -(i + j) + ij

    # lvl 4

    print(f'GATE {g + 10} AND {g + 1} {g + 8}')  # -k(i xor j)
    print(f'GATE {g + 11} AND {k} {g + 9}')  # k(-(i + j) + ij)

    # lvl 5
    print(f'GATE {g + 12} OR {g + 10} {g + 11}')  # -k(i xor j) + k(-(i + j) + ij) -- x

    return g + 12, g + 7


n = int(input())

x, y = [], []
g = 3 * n - 1

for i in range(n):
    x_i, y_i = trick(g, i, i + n, i + 2 * n)
    x.append(x_i)
    y.append(y_i)
    g = x_i

print(f'GATE {g + 1} AND {2 * n} {3 * n}')

for i in range(n):
    print(f'OUTPUT {i} {x[i]}')
print(f'OUTPUT {n} {g + 1}')

print(f'OUTPUT {n + 1} {g + 1}')
for i in range(n):
    print(f'OUTPUT {i + n + 2} {y[i]}')
