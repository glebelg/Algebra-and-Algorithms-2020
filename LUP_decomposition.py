import math


M = 2


def add_zero_padding(matrix, new_size):
    matrix = [row + [0] * (new_size - len(matrix[0])) for row in matrix]
    return matrix + [[0] * new_size for _ in range(len(matrix[0]) - len(matrix))]


def cut_padding(matrix, shape):
    return [row[:shape[1]] for row in matrix[:shape[0]]]


def up_size(size):
    return 2 ** math.ceil(math.log2(size))


def read_matrix():
    matrix = [list(map(int, input().split()))]
    for _ in range(len(matrix[0]) - 1):
        matrix.append(list(map(int, input().split())))
    return matrix, len(matrix)


def split_matrix(matrix):
    matrix11, matrix12, matrix21, matrix22 = [], [], [], []
    for i in range(len(matrix[0]) // 2):
        matrix11.append(matrix[i][:len(matrix[0]) // 2])
        matrix12.append(matrix[i][len(matrix[0]) // 2:])
        matrix21.append(matrix[i + len(matrix[0]) // 2][:len(matrix[0]) // 2])
        matrix22.append(matrix[i + len(matrix[0]) // 2][len(matrix[0]) // 2:])
    return matrix11, matrix12, matrix21, matrix22


def sum_matrix(A, B):
    return [[(A[i][j] + B[i][j]) % M for j in range(len(A[0]))] for i in range(len(A))]


def diff_matrix(A, B):
    return [[(A[i][j] - B[i][j]) % M for j in range(len(A[0]))] for i in range(len(A))]


def strassen(A, B):
    if len(A[0]) == 1:
        return [[(A[0][0] * B[0][0]) % M]]

    A11, A12, A21, A22 = split_matrix(A)
    B11, B12, B21, B22 = split_matrix(B)

    p1 = strassen(sum_matrix(A11, A22), sum_matrix(B11, B22))
    p2 = strassen(sum_matrix(A21, A22), B11)
    p3 = strassen(A11, diff_matrix(B12, B22))
    p4 = strassen(A22, diff_matrix(B21, B11))
    p5 = strassen(sum_matrix(A11, A12), B22)
    p6 = strassen(diff_matrix(A21, A11), sum_matrix(B11, B12))
    p7 = strassen(diff_matrix(A12, A22), sum_matrix(B21, B22))

    c11 = sum_matrix(diff_matrix(sum_matrix(p1, p4), p5), p7)
    c12 = sum_matrix(p3, p5)
    c21 = sum_matrix(p2, p4)
    c22 = sum_matrix(sum_matrix(diff_matrix(p1, p2), p3), p6)

    return [row1 + row2 for row1, row2 in zip(c11 + c21, c12 + c22)]


def inverse_P(matrix):
    matrix = [[matrix[i][j] for j in range(len(matrix))] for i in range(len(matrix))]
    for i in range(len(matrix)):
        for j in range(i + 1, len(matrix[0])):
            matrix[i][j], matrix[j][i] = matrix[j][i], matrix[i][j]
    return matrix


def inverse_U(matrix):
    if len(matrix) == 1:
        return [[1]]

    A11, A12, A21, A22 = split_matrix(matrix)

    B11 = inverse_U(A11)
    B22 = inverse_U(A22)
    B12 = strassen(strassen(B11, A12), B22)
    B21 = A21

    return [row1 + row2 for row1, row2 in zip(B11 + B21, B12 + B22)]


def LUP_decomposition(A):
    m, p = len(A), len(A[0])

    if m == 1:
        P = [[int(i == j != 0) for j in range((p))] for i in range(p)]
        for i in range(len(A[0])):
            if A[0][i]:
                P[i][i], P[0][i],  P[i][0] = 0, 1, 1
                break

        L = [[1]]
        U = cut_padding(
                         strassen(add_zero_padding(A, up_size(len(P[0]))),
                                  add_zero_padding(P, up_size(len(P[0])))),
                         (len(A), len(P[0]))
                        )
        return L, U, P

    B, C = A[:m//2], A[m//2:]

    L1, U1, P1 = LUP_decomposition(B)

    P1_inv = inverse_P(P1.copy())
    D = cut_padding(
                     strassen(add_zero_padding(C, up_size(len(P1_inv[0]))),
                              add_zero_padding(P1_inv,  up_size(len(P1_inv[0])))),
                     (len(C), len(P1_inv[0]))
                    )

    E, F = [row[:m//2] for row in U1], [row[:m//2] for row in D]

    E_inv = cut_padding(inverse_U(add_zero_padding(E, up_size(len(E)))), (len(E), len(E[0])))
    FE_inv = cut_padding(
                          strassen(add_zero_padding(F, up_size(len(E_inv[0]))),
                                   add_zero_padding(E_inv,  up_size(len(E_inv[0])))),
                          (len(F), len(E_inv[0]))
                         )

    G = diff_matrix(D, cut_padding(
                                    strassen(add_zero_padding(FE_inv, up_size(len(U1[0]))),
                                             add_zero_padding(U1,  up_size(len(U1[0])))),
                                    (len(FE_inv), len(U1[0]))
                                   ))


    L2, U2, P2 = LUP_decomposition([row[m//2:] for row in G])

    P3 = [[int(i == j) for j in range((p))] for i in range(m // 2)] + [[0] * (m // 2) + row for row in P2]

    P3_inv = inverse_P(P3.copy())
    H = cut_padding(
                     strassen(add_zero_padding(U1, up_size(len(P3_inv[0]))),
                              add_zero_padding(P3_inv,  up_size(len(P3_inv[0])))),
                     (len(U1), len(P3_inv[0]))
                    )

    L = [row1 + row2 for row1, row2 in zip(L1 + FE_inv, [[0] * len(L2[0]) for i in range(len(L2[0]))] + L2)]
    U = H + [[0] * (m // 2) + row for row in U2]
    P = cut_padding(
                     strassen(add_zero_padding(P3, up_size(len(P1[0]))),
                              add_zero_padding(P1,  up_size(len(P1[0])))),
                     (len(P3), len(P1[0]))
                    )
    return L, U, P


if __name__ == '__main__':
    A, n = read_matrix()
    L, U, P = LUP_decomposition(add_zero_padding(A, up_size(n)))

    for row in cut_padding(L, (n, n)):
        print(*row)
    for row in cut_padding(U, (n, n)):
        print(*row)
    for row in cut_padding(P, (n, n)):
        print(*row)
