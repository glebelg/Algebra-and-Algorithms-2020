import math

n = int(input())
A = [list(range(n))] + [[0] * n for i in range(int(math.log2(n)) + 1)]

gate = n
for d in range(int(math.log2(n)) + 1):
    for i in range(n):
        if i < 2 ** d:
            A[d + 1][i] = A[d][i]
        else:
            A[d + 1][i] = gate
            print(f'GATE {gate} OR {A[d][i - 2**d]} {A[d][i]}')
            gate += 1

for out in range(n):
    print(f'OUTPUT {out} {A[-1][out]}')
