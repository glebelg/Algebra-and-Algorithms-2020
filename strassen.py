import math


M = 9


def read_matrix():
    matrix = [list(map(int, input().split()))]
    n = len(matrix[0])
    bais = 2 ** math.ceil(math.log2(n)) - n
    for _ in range(n - 1):
        matrix.append(list(map(int, input().split())) + [0] * bais)
    matrix[0] += [0] * bais
    for _ in range(bais):
        matrix.append([0] * (n + bais))
    return matrix, n


def split_matrix(matrix):
    matrix11, matrix12, matrix21, matrix22 = [], [], [], []
    for i in range(len(matrix[0]) // 2):
        matrix11.append(matrix[i][:len(matrix[0]) // 2])
        matrix12.append(matrix[i][len(matrix[0]) // 2:])
        matrix21.append(matrix[i + len(matrix[0]) // 2][:len(matrix[0]) // 2])
        matrix22.append(matrix[i + len(matrix[0]) // 2][len(matrix[0]) // 2:])
    return matrix11, matrix12, matrix21, matrix22


def sum_matrix(A, B):
    return [[(A[i][j] + B[i][j]) % M for j in range(len(A[0]))] for i in range(len(A[0]))]


def diff_matrix(A, B):
    return [[(A[i][j] - B[i][j]) % M for j in range(len(A[0]))] for i in range(len(A[0]))]


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

    c1, c2 = [], []
    for i in range(len(c11)):
        c1.append(c11[i] + c12[i])
        c2.append(c21[i] + c22[i])
    return c1 + c2


def power(matrix, n):
    if n == 1:
        return matrix
    if n % 2:
        return strassen(power(matrix, n // 2), power(matrix, n // 2 + 1))
    return strassen(power(matrix, n // 2), power(matrix, n // 2))


matrix, n = read_matrix()
matrix = power(matrix, n)

for i in range(n):
    print(*matrix[i][:n])
