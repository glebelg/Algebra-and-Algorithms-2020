def negation(gates):
    gates4print = [f'GATE {n + i} NOT {i}' for i in range(n)]
    gates[2 ** n // 2] += [[n + i, [j for j in range(2 ** n) if (j >> i) & 1 == 0]] for i in range(n)]
    return gates, gates4print

def conjunction(gate, gates, gates4print):
    for strong in gates[2 ** n // 2]:
        for i in range(2 ** n // 2 + 1):
            for weak in gates[i]:
                if set(strong[1]) & set(weak[1]) not in [set(k[1]) for k in gates[len(set(strong[1]) & set(weak[1]))]]:
                    gates[len(set(strong[1]) & set(weak[1]))].append([gate, list(set(strong[1]) & set(weak[1]))])
                    gates4print.append(f'GATE {gate} AND {min(strong[0], weak[0])} {max(strong[0], weak[0])}')
                    gate += 1
    return gate, gates, gates4print

def disjunction(gate, gates, gates4print):
    gates.append([])
    for strong in gates[1]:
        for i in range(2 ** n):
            for weak in gates[i]:
                if set(strong[1]) | set(weak[1]) not in [set(k[1]) for k in gates[len(set(strong[1]) | set(weak[1]))]]:
                    gates[len(set(strong[1]) | set(weak[1]))].append([gate, list(set(strong[1]) | set(weak[1]))])
                    gates4print.append(f'GATE {gate} OR {min(strong[0], weak[0])} {max(strong[0], weak[0])}')
                    gate += 1
    return gate, gates, gates4print


n = int(input())

gates = [[] for i in range(2 ** n)]
gates[2 ** n // 2] = [[i, [j for j in range(2 ** n) if (j >> i) & 1 == 1]] for i in range(n)]

gates, gates4print = negation(gates)
gate, gates, gates4print = conjunction(2 * n, gates, gates4print)
gate, gates, gates4print = disjunction(gate, gates, gates4print)

outputs4print = [f'OUTPUT {i - n} {i}' for i in range(n, 2 ** 2 ** n)]

print(*gates4print + outputs4print, sep='\n')

# with open('ans', 'w') as f:
#     f.write(str(n) + '\n' + '\n'.join(gates4print + outputs4print))
