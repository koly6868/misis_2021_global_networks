def distance(p1, p2):
    assert len(p1) == len(p2)
    return sum([abs(e1 - e2) for e1, e2 in zip(p1, p2)]) / len(p1)


def sec_distance(z, p):
    return sum([0 if e[0] < p[i] < e[1] else min([abs(p[i] - pe) for pe in e])
                for i, e in enumerate(z)])


def centr(z):
    return [sum(e) / len(e) for e in z]


def is_neighbours(z1, z2, eps=10e-15):
    t = [intersection(e1, e2) for e1, e2 in zip(z1, z2)]
    one_zero = sum([1 if abs(e) < eps else 0 for e in t]) == 1
    all_non_negative = all([e >= 0 for e in t])
    if one_zero and all_non_negative:
        return True

    return False


def intersection(i1, i2):
    i1, i2 = sorted([i1, i2], key=lambda x: x[0])
    if i1[1] > i2[0]:
        if i1[1] > i2[1]:
            return i1[1] - i1[0]
        return i1[1] - i2[0]
    else:
        return -(i2[0] - i1[1])


def find_shortest(graph, node, tnode):
    cp = []
    sp = None
    used = set([node])
    q = [node]

    layer_rest = 1
    next_layer_rest = 0
    l = 0
    while q:
        cn = q[0]
        q = q[1:]
        layer_rest -= 1

        if cn == tnode:
            return l

        for n in graph[cn]:
            if n in used:
                continue
            used.add(n)
            q.append(n)
            next_layer_rest += 1
        
        if layer_rest == 0:
            l +=1
            layer_rest = next_layer_rest
            next_layer_rest = 0