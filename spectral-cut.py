import numpy as np


def read_graph():
    n_e, n_v = int(input()), 0
    edges = []
    for _ in range(n_e):
        edge = list(map(int, input().split()))
        edges.append(edge)
        n_v = max(n_v, *edge)
    return n_v + 1, edges


def laplacian_matrix(n_v, edges):
    matrix = np.zeros((n_v, n_v), dtype=int)
    for edge in edges:
        matrix[edge[0], edge[1]] = -1
        matrix[edge[1], edge[0]] = -1
        matrix[edge[0], edge[0]] += 1
        matrix[edge[1], edge[1]] += 1
    return matrix


def min_cut_component(order, laplacian):
    phis = []
    for k in range(1, n_v):
        phi = 0
        for v1 in range(k):
            for v2 in range(k, n_v):
                if laplacian[order[v1], order[v2]] == -1:
                    phi += 1
        phis.append(phi / (k * (n_v - k)))

    k_list = [i + 1 for i, phi in enumerate(phis) if phi == min(phis)]
    component = order[:k_list[0]] if k_list[0] <= n_v // 2 else order[k_list[0]:]
    for k in k_list[1:]:
        if order[:k] if k <= n_v // 2 else order[k:] < component:
            component = order[:k] if k <= n_v // 2 else order[k:]
    return component


if __name__ == "__main__":
    n_v, edges = read_graph()
    laplacian = laplacian_matrix(n_v, edges)
    eigenvector = np.linalg.eigh(laplacian)[1][:,1]
    order = np.flip(np.argsort(eigenvector), axis=0)
    component = min_cut_component(order, laplacian)
    print(*component)
