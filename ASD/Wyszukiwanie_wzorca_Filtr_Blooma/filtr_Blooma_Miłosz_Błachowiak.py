import time
import math


def h1(val, prime):
    if isinstance(val, str):
        val_sum = 0
        for l in val:
            val_sum += ord(l)
        val = val_sum
    return val % prime


def h2(val, prime):
    if isinstance(val, str):
        val_sum = 0
        for l in val:
            val_sum += ord(l)
        val = val_sum
    return (2*val + 3) % prime


def Rabin_Karp(text, subs, N, n=20, prime=5):
    start_time = time.time()

    S = text.lower()
    W = [pattern.lower() for pattern in subs]
    starting_indices = {sub: [] for sub in W}

    M = len(S)

    P = 0.001
    b = int(-n * math.log(P) / ((math.log(2))**2))
    k = int(b / n * math.log(2))

    hsubs = [0 for i in range(b)]

    # inserting
    for sub in W:
        h_1 = h1(sub, prime)
        h_2 = h2(sub, prime)

        for i in range(k):
            g = h_1 + i * h_2
            hsubs[g] = 1

    hs_tab = []
    for i in range(k):
        hs_tab.append(h1(S[:N], prime) + i * h2(S[:N], prime))

    false_positive = 0
    for m in range(M-N+1):
        present = True
        for hs in hs_tab:
            if hsubs[hs] == 0:
                present = False
        if present:
            if S[m:m+N] in W:
                starting_indices[S[m:m+N]].append(m)
            else:

                if false_positive % 10000 == 0:
                    print("Wybrana detekcja fałszywie pozytywna: ", S[m:m+N])
                false_positive += 1

        hs_tab = []
        for i in range(k):
            hs_tab.append(h1(S[m+1:m+N+1], prime) + i * h2(S[m+1:m+N+1], prime))

    print("\n--- %s seconds ---" % (time.time() - start_time))
    print("Liczba detekcji fałszywie pozytywnych: ", false_positive)
    return starting_indices


def print_dict(dict):
    print("{")
    for key in dict.keys():
        print(key, ": ", dict[key])
    print("}")


def main():

    # wczytanie dołączonego tekstu "lotr.txt"
    with open("lotr.txt", encoding='utf-8') as f:
        text = f.readlines()
    S = ' '.join(text)

    short = "There is nothing like looking, if you want to find something. " \
            "You certainly usually find something, if you look, but it is not always " \
            "quite the something you were after."

    patterns = ['gandalf', 'looking', 'blocked', 'comment', 'pouring', 'finally', 'hundred', 'hobbits', 'however',
                'popular', 'nothing', 'enjoyed', 'stuffed', 'relaxed', 'himself', 'present', 'deliver', 'welcome',
                'baggins', 'further']

    print("Testy dla tekstu dłuższego - lotr.txt\n")
    print("====Test dla dwudziestu wzorców====")
    starting_indices = Rabin_Karp(S, patterns, 7, prime=31)
    print("Dopasowania:")
    print_dict(starting_indices)
    print("\n")

    print("====Test dla jednego wzorca====")
    patterns = ['blocked']
    starting_indices = Rabin_Karp(S, patterns, 7, 1, prime=2)
    print("Dopasowania:")
    print_dict(starting_indices)


    print("Testy dla prostego tekstu\n")
    print("====Test dla trzech wzorców====")
    patterns = ['nothing', 'looking', 'usually']
    starting_indices = Rabin_Karp(short, patterns, 7, 3)
    print("Dopasowania:")
    print_dict(starting_indices)
    print("\n")

    print("====Test dla jednego wzorca====")
    patterns = ['nothing']
    starting_indices = Rabin_Karp(short, patterns, 7, 1, prime=2)
    print("Dopasowania:")
    print_dict(starting_indices)

    # czas przeszukiwania tylko niewiele wzrósł po zwiększeniu liczby wyszukiwanych wzorców

if __name__ == "__main__":
    main()
