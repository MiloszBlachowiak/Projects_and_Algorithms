import numpy as np
import time

# ciąg Fibonacciego


# a) rekurencja
def fib_r(n: int):
    if n == 0:
        return 0
    if n == 1:
        return 1
    return fib_r(n-1) + fib_r(n-2)


def fib_r_n_elements(n):
    fib = []
    for i in range(n+1):
        fib.append(fib_r(i))
    return fib


# b) z pamięcią podręczną (cache)
MAXN = 45
UNKNOWN = -1
f = [None for i in range(MAXN+1)]


def fib_c(n: int):
    global f
    if f[n] == UNKNOWN:
        f[n] = fib_c(n-1) + fib_c(n-2)
    return f[n]


def fib_c_driver(n: int):
    global f
    f[0] = 0
    f[1] = 1
    for i in range(2, n+1):
        f[i] = UNKNOWN

    fib = []
    for i in range(n+1):
        fib.append(fib_c(i))
    return fib


# c) wariant PD
def fib_pd(n: int):
    f = [None for i in range(MAXN+1)]
    f[0] = 0
    f[1] = 1
    for i in range(2, n+1):
        f[i] = f[i-1] + f[i-2]
    return f[:n+1]


# d) wariant PD 2.0
def fib_pd_2_0(n: int):
    if n == 0:
        return 0

    f1 = 0
    f2 = 1
    for i in range(2, n + 1):
        f1, f2 = f2, f1 + f2
    return f2


def fib_pd_2_0_n_elems(n: int):
    fib = []
    for i in range(n+1):
        fib.append(fib_pd_2_0(i))
    return fib


# Aproksymowane dopasowanie ciągu znakowego
# a) wariant rekurencyjny
MATCH = 0
INSERT = 1
DELETE = 2


def indel(c):
    return 1


def match(c, d):
    if c == d:
        return 0
    return 1


def string_compare(s, t, i, j):
    opt = [None for i in range(3)]

    if i == 0:
        return j * indel(' ')
    if j == 0:
        return i * indel(' ')
    opt[MATCH] = string_compare(s, t, i-1, j-1) + match(s[i], t[j])
    opt[INSERT] = string_compare(s, t, i, j-1) + indel(t[j])
    opt[DELETE] = string_compare(s, t, i-1, j) + indel(s[i])

    lowest_cost = opt[MATCH]

    for k in range(INSERT, DELETE+1):
        if opt[k] < lowest_cost:
            lowest_cost = opt[k]
    return lowest_cost


# b) wariant PD

MAXLEN = 45


class cell:
    def __init(self):
        self.cost = 0
        self.parent = -1


m = [[cell() for x in range(MAXLEN + 1)] for y in range(MAXLEN + 1)]


def row_init(i):
    global m
    m[0][i].cost = i
    if i > 0:
        m[0][i].parent = INSERT
    else:
        m[0][i].parent = -1


def column_init(i):
    global m
    m[i][0].cost = i
    if i > 0:
        m[i][0].parent = DELETE
    else:
        m[i][0].parent = -1


def string_compare_pd(s, t, i, j):
    global m
    opt = [0 for i in range(3)]

    for i in range(MAXLEN):
        row_init(i)
        column_init(i)

    for i in range(1, len(s)):
        for j in range(1, len(t)):
            opt[MATCH] = m[i-1][j-1].cost + match(s[i], t[j])
            opt[INSERT] = m[i][j-1].cost + indel(t[j])
            opt[DELETE] = m[i-1][j].cost + indel(s[i])

            m[i][j].cost = opt[MATCH]
            m[i][j].parent = MATCH
            for k in range(INSERT, DELETE+1):
                if opt[k] < m[i][j].cost:
                    m[i][j].cost = opt[k]
                    m[i][j].parent = k

    return m[i][j].cost


# c) odtwarzanie ścieżki
def match_out(s, t, i, j):
    if s[i] == t[j]:
        print("M", end="")
    else:
        print("S", end="")


def insert_out(t, j):
    print("I", end="")


def delete_out(s, i):
    print("D", end="")


def reconstruct_path(s, t, i, j):
    if m[i][j].parent == -1:
        return
    if m[i][j].parent == MATCH:
        reconstruct_path(s, t, i-1, j-1)
        match_out(s, t, i, j)
        return
    if m[i][j].parent == INSERT:
        reconstruct_path(s, t, i, j-1)
        insert_out(t, j)
        return
    if m[i][j].parent == DELETE:
        reconstruct_path(s, t, i-1, j)
        delete_out(s, i)
        return


def string_compare_path(s, t, i, j):
    global m
    opt = [0 for i in range(3)]

    for i in range(MAXLEN):
        row_init(i)
        column_init(i)

    for i in range(1, len(s)):
        for j in range(1, len(t)):
            opt[MATCH] = m[i-1][j-1].cost + match(s[i], t[j])
            opt[INSERT] = m[i][j-1].cost + indel(t[j])
            opt[DELETE] = m[i-1][j].cost + indel(s[i])

            m[i][j].cost = opt[MATCH]
            m[i][j].parent = MATCH
            for k in range(INSERT, DELETE+1):
                if opt[k] < m[i][j].cost:
                    m[i][j].cost = opt[k]
                    m[i][j].parent = k

    print("Odtworzona ścieżka:")
    reconstruct_path(s, t, i, j)
    print("\n")
    return m[i][j].cost


# d) dopasowanie podciągów
def row_init_2(i):
    global m
    m[0][i].cost = 0
    m[0][i].parent = -1


def goal_cell(s, t, i, j):
    i = len(s) - 1
    j = 0
    for k in range(1, len(t)):
        if m[i][k].cost < m[i][j].cost:
            j = k
    return i, j


def string_compare_3(s, t, i, j):
    global m
    opt = [0 for i in range(3)]

    for i in range(MAXLEN):
        row_init_2(i)
        column_init(i)

    for i in range(1, len(s)):
        for j in range(1, len(t)):
            opt[MATCH] = m[i-1][j-1].cost + match(s[i], t[j])
            opt[INSERT] = m[i][j-1].cost + indel(t[j])
            opt[DELETE] = m[i-1][j].cost + indel(s[i])

            m[i][j].cost = opt[MATCH]
            m[i][j].parent = MATCH
            for k in range(INSERT, DELETE+1):
                if opt[k] < m[i][j].cost:
                    m[i][j].cost = opt[k]
                    m[i][j].parent = k

    i, j = goal_cell(s, t, i, j)
    return j
    # return m[i][j].cost


# e) najdłuższy wspólny podciąg
def match2(c, d):
    if c == d:
        return 0
    return MAXLEN


def string_compare_4(s, t, i, j):
    global m
    opt = [0 for i in range(3)]

    for i in range(MAXLEN):
        row_init(i)
        column_init(i)

    for i in range(1, len(s)):
        for j in range(1, len(t)):
            opt[MATCH] = m[i-1][j-1].cost + match2(s[i], t[j])
            opt[INSERT] = m[i][j-1].cost + indel(t[j])
            opt[DELETE] = m[i-1][j].cost + indel(s[i])

            m[i][j].cost = opt[MATCH]
            m[i][j].parent = MATCH
            for k in range(INSERT, DELETE+1):
                if opt[k] < m[i][j].cost:
                    m[i][j].cost = opt[k]
                    m[i][j].parent = k
    return m[i][j].cost


def main():

    print("=====Ciąg fibonacciego=====")
    print("a) wariant rekurencyjny:")
    start = time.time()
    print("Czterdzieści pierwszych elementów ciągu fibonacciego:")
    print(fib_r_n_elements(40))
    print("Czas obliczenia 40 pierwszych liczb ciągu: ", time.time() - start)

    print("\nb) wariant z pamięcią podręczną:")
    start = time.time()
    print("Czterdzieści pierwszych elementów ciągu fibonacciego:")
    print(fib_c_driver(40))
    print("Czas obliczenia 40 pierwszych liczb ciągu: ", time.time() - start)

    print("\nc)wariant PD:")
    start = time.time()
    print("Czterdzieści pierwszych elementów ciągu fibonacciego:")
    print(fib_pd(40))
    print("Czas obliczenia 40 pierwszych liczb ciągu: ", time.time() - start)

    print("\nd)wariant PD 2.0:")
    start = time.time()
    print("Czterdzieści pierwszych elementów ciągu fibonacciego:")
    print(fib_pd_2_0_n_elems(40))
    print("Czas obliczenia 40 pierwszych liczb ciągu: ", time.time() - start)

    print("\n=====Aproksymowane dopasowanie ciągu znakowego=====")
    print("a) wariant rekurencyjny:")
    start = time.time()
    S = ' kot'
    T = ' kon'
    print("Wartość kosztu dla dwóch ciągów:", S," i ", T)
    print(string_compare(S, T, 3, 3))
    print("Czas obliczeń: ", time.time() - start)

    start = time.time()
    S = ' kot'
    T = ' pies'
    print("\nWartość kosztu dla dwóch ciągów:", S, " i ", T)
    print(string_compare(S, T, 3, 4))
    print("Czas obliczeń: ", time.time() - start)

    print("\nb) wariant PD:")
    start = time.time()
    S = ' kot'
    T = ' kon'
    print("Wartość kosztu dla dwóch ciągów:", S, " i ", T)
    print(string_compare_pd(S, T, 3, 3))
    print("Czas obliczeń: ", time.time() - start)

    start = time.time()
    S = ' kot'
    T = ' pies'
    print("\nWartość kosztu dla dwóch ciągów:", S, " i ", T)
    print(string_compare_pd(S, T, 3, 4))
    print("Czas obliczeń: ", time.time() - start)

    print("\nc) odtwarzanie ścieżki:")
    S = ' thou shalt not'
    T = ' you should not'
    cost = string_compare_path(S, T, 14, 14)
    print("Wartość kosztu dla dwóch ciągów:", S, " i ", T)
    print(cost)

    print("\nd) dopasowanie podciągów:")
    S = ' ban'
    T = ' mokeyssbanana'
    cost = string_compare_3(S, T, 3, 17)
    print("Wartość kosztu dla dwóch ciągów:", S, " i ", T)
    print(cost)

    # funkcja zwraca indeks występowania ostatniego znaku ze wzorca S w tekście T

    print("\ne) najdłuższy wspólny podciąg:")
    S = ' democrat'
    T = ' republican'
    cost = string_compare_4(S, T, 8, 10)
    print("Wartość kosztu dla dwóch ciągów:", S, " i ", T)
    print(cost)


    print("\nf) najdłuższy podciąg monotoniczny:")
    T = ' 243517698'
    S = sorted(T)
    cost = string_compare_4(S, T, 9, 9)
    print("Wartość kosztu dla dwóch ciągów:", S, " i ", T)
    print(cost)

    T = ' 45246127'
    S = sorted(T)
    cost = string_compare_4(S, T, 8, 8)
    print("Wartość kosztu dla dwóch ciągów:", S, " i ", T)
    print(cost)


if __name__ == "__main__":
    main()
