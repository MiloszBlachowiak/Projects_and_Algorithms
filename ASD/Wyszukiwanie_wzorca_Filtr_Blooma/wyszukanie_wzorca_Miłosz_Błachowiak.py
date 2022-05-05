import time


def naive(pattern, text):
    S = text.lower()
    W = pattern.lower()

    comparisons = 0
    start_time = time.time()

    starting_indices = []
    for m in range(len(S) - len(W) + 1):
        for i in range(len(W)):
            comparisons += 1
            if W[i] != S[m + i]:
                break
            elif W[i] == S[m + i] and i == len(W) - 1:
                starting_indices.append(m)

    print("--- %s seconds ---" % (time.time() - start_time))
    print("Znaleziono {} dopasowań".format(len(starting_indices)))
    return starting_indices, comparisons


def Rabin_Karp(text, pattern, q=101):
    start_time = time.time()

    S = text.lower()
    W = pattern.lower()
    starting_indices = []

    comparisons = 0

    M = len(S)
    N = len(W)

    d = 256

    hW = 0
    hS = 0
    h = 1

    same_hash = 0

    for i in range(N):
        hW = (d*hW + ord(W[i])) % q
        hS = (d* hS + ord(S[i])) % q

    for i in range(N - 1):
        h = (h * d) % q

    for m in range(M-N+1):
        comparisons += 1
        if hS == hW:
            comparisons += 1
            if S[m:m+N] == W:
                starting_indices.append(m)
            else:
                same_hash += 1

        if m < M - N:
            hS = (d*(hS - ord(S[m]) * h) + ord(S[m+N])) % q

            if hS < 0:
                hS += q
    print("--- %s seconds ---" % (time.time() - start_time))
    print("Znaleziono {} dopasowań".format(len(starting_indices)))
    print("Liczba sytuacji, w których ten sam skrót oznaczał różne ciągi: ", same_hash)
    return starting_indices, comparisons


def KMP_get_T(W):
    pos = 1
    cnd = 0

    N = len(W)

    T = [0 for i in range(N)]
    T[0] = -1

    while pos < N:
        if W[pos] == W[cnd]:
            T[pos] = T[cnd]
        else:
            T[pos] = cnd
            while cnd >= 0 and W[pos] != W[cnd]:
                cnd = T[cnd]
        pos += 1
        cnd += 1
    T.append(cnd)
    return T


def KMP(text, pattern):
    start_time = time.time()
    S = text.lower()
    W = pattern.lower()

    comparisons = 0
    M = len(S)
    N = len(W)

    starting_indices = []
    m = 0
    i = 0

    T = KMP_get_T(W)

    while m < M:
        comparisons += 1
        if W[i] == S[m]:
            m += 1
            i += 1
            if i == N:
                starting_indices.append(m-i)
                i = T[i]
        else:
            i = T[i]
            if i < 0:
                m += 1
                i += 1
    print("--- %s seconds ---" % (time.time() - start_time))
    print("Znaleziono {} dopasowań".format(len(starting_indices)))
    return starting_indices, comparisons


def main():
    # wczytanie dołączonego tekstu "lotr.txt"
    with open("lotr.txt", encoding='utf-8') as f:
        text = f.readlines()
    S = ' '.join(text)

    short = "There is nothing like looking, if you want to find something. " \
            "You certainly usually find something, if you look, but it is not always " \
            "quite the something you were after."


    print("Metoda naiwna\n")

    print("Testy dla tekstu dłuższego - lotr.txt\n")
    pattern = "You mean Otho and Lobelia"
    print("Szukany wzorzec: ", pattern)
    indices, comparisons = naive(pattern, S)
    print("Dopasowania: ", indices)
    print("Liczba porównań: ", comparisons)
    print("\n")

    pattern = "mantelpiece"
    print("Szukany wzorzec: ", pattern)
    indices, comparisons = naive(pattern, S)
    print("Dopasowania: ", indices)
    print("Liczba porównań: ", comparisons)
    print("\n")

    print("Testy dla prostego tekstu\n")
    pattern = "certainly"
    print("Szukany wzorzec: ", pattern)
    indices, comparisons = naive(pattern, short)
    print("Dopasowania: ", indices)
    print("Liczba porównań: ", comparisons)
    print("\n")


    print("Metoda Rabina-Karpa\n")

    print("Testy dla tekstu dłuższego - lotr.txt\n")

    pattern = "You mean Otho and Lobelia"
    print("Szukany wzorzec: ", pattern)
    indices, comparisons = Rabin_Karp(S, pattern)
    print("Dopasowania: ", indices)
    print("Liczba porównań: ", comparisons)
    print("\n")

    pattern = "mantelpiece"
    print("Szukany wzorzec: ", pattern)
    indices, comparisons = Rabin_Karp(S, pattern)
    print("Dopasowania: ", indices)
    print("Liczba porównań: ", comparisons)
    print("\n")

    print("Testy dla prostego tekstu\n")
    pattern = "certainly"
    print("Szukany wzorzec: ", pattern)
    indices, comparisons = Rabin_Karp(short, pattern)
    print("Dopasowania: ", indices)
    print("Liczba porównań: ", comparisons)
    print("\n")

    # metoda Rabina-Karpa wykonała mniej porównań od metody naiwnej, natomiast czasy wykonania
    # są podobne dla obu metod

    print("Metoda Knutha-Morrisa-Pratta\n")

    print("Testy dla tekstu dłuższego - lotr.txt\n")

    pattern = "You mean Otho and Lobelia"
    print("Szukany wzorzec: ", pattern)
    indices, comparisons = KMP(S, pattern)
    print("Dopasowania: ", indices)
    print("Liczba porównań: ", comparisons)
    print("\n")

    pattern = "relaxed"
    print("Szukany wzorzec: ", pattern)
    indices, comparisons= KMP(S, pattern)
    print("Dopasowania: ", indices)
    print("Liczba porównań: ", comparisons)
    print("\n")

    print("Testy dla prostego tekstu\n")
    pattern = "certainly"
    print("Szukany wzorzec: ", pattern)
    indices, comparisons = KMP(short, pattern)
    print("Dopasowania: ", indices)
    print("Liczba porównań: ", comparisons)
    print("\n")

    # w przypadku metody Knutha-Morrisa-Pratta liczba porównań jest zbliżona (niewiele mniejsza)
    # do liczby porównań w metodzie naiwnej, natomiast czas wykonania dla długiego tekstu zmalał
    # w porównaniu do dwóch poprzednich metod.

if __name__ == "__main__":
    main()
