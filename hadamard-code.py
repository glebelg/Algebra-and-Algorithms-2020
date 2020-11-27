def legendre_symbol(a, p):
    return pow(a, (p - 1) // 2, p) if pow(a, (p - 1) // 2, p) != p - 1 else -1


def jacobsthal_matrix(q):
    jacobsthal = [[legendre_symbol(i - j, q) if i != j else -1 for j in range(q)] for i in range(q)]
    return jacobsthal


def hadamard_matrix(q):
    jacobsthal = jacobsthal_matrix(q)
    hadamard = [[1] + row for row in [[1] * q] + jacobsthal]
    return hadamard


def hadamard_code(n):
    hadamard = hadamard_matrix(n - 1)
    code = []
    for row in hadamard:
        code.append([int(a == 1) for a in row])
        code.append([int(a == 0) for a in code[-1]])
    return code


if __name__ == '__main__':
    n = int(input())

    code = hadamard_code(n)
    for row in code:
        print(''.join(map(str, row)))
