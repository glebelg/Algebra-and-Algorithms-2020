import random


S = int(1e+6 + 1)
K = 6


def read_graph():
    n_e, n_v = int(input()), 0
    edges = []
    for _ in range(n_e):
        edge = list(map(int, input().split()))
        edges.append(edge)
        n_v = max(n_v, *edge)
    return n_v + 1, edges


def get_edmonds_matrix(n_v, edges):
    matrix = [[0] * n_v for _ in range(n_v)]
    for edge in edges:
        matrix[edge[0]][edge[1]] = random.choice(list(range(S)))
    return matrix


def deternminant(n_v, matrix):
    for i in range(n_v):
        col = [row[i] for row in matrix[i:]]
        if max(col) == 0:
            return 0
        matrix[i], matrix[col.index(max(col)) + i] = matrix[col.index(max(col)) + i], matrix[i]
        for j in range(i + 1, n_v):
            for k in range(i + 1, n_v):
                matrix[j][k] = (matrix[j][k] - matrix[i][k] // max(col) * matrix[j][i]) % S
    return 1


n_v, edges = read_graph()

dets = []
for k in range(K):
    matrix = get_edmonds_matrix(n_v, edges)
    dets.append(deternminant(n_v, matrix))

pm = 'yes' if sum(dets) else 'no'
print(pm)
