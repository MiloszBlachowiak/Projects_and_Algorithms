from timeit import timeit
import random


def insertion_sort(table):
    tab = table[:] # kopiujemy aby nie zmieniać tablicy wejściowej
    counter = 0
    for i in range(1, len(tab)):
        t = tab[i]
        j = i - 1
        while j >= 0 and tab[j] > t:
            tab[j + 1], tab[j] = tab[j], tab[j + 1]
            counter += 1
            j -= 1
        tab[j + 1] = t
    return tab, counter


def shellsort(table):
    tab = table[:] # kopiujemy aby nie zmieniać tablicy wejściowej
    counter = 0
    size = len(tab)
    k = 0
    while (3**(k + 1) - 1)/2 < size/3:
        k += 1
    h = (3**k - 1)//2
    while h > 0:
        for i in range(h, size):
            t = tab[i]
            j = i
            while j >= h and tab[j - h] > t:
                tab[j - h], tab[j] = tab[j], tab[j - h]
                counter += 1
                j -= h
            tab[j] = t
        h //= 3
    tab, count = insertion_sort(tab)
    counter += count
    return tab, counter

# =====================================================


def hoare_median(tab):
    length = len(tab)
    i = 0
    j = length - 1
    x_index = length // 2
    x = tab[x_index]

    while i < j:
        if tab[i] < x:
            i += 1
        if i != j:
            if tab[j] > x:
                j -= 1

        if tab[i] >= x >= tab[j] and i < j:
            if tab[i] != tab[j]:
                tab[j], tab[i] = tab[i], tab[j]
                return hoare_median(tab)
            else:
                i += 1

    if i == j and j == length // 2:
        return tab[j]
    if j < length//2:
        return hoare_median(tab[j + 1:])
    if j > length//2:
        return hoare_median(tab[:j])


def divide(tab):
    subsets = []
    i = 0
    while i < len(tab):
        if i + 5 > len(tab):
            subsets.append(tab[i:])
        else:
            subsets.append((tab[i:i + 5]))
        i += 5
    return subsets


def get_pivot(subsets):
    medians = []
    for subset in subsets:
        median = hoare_median(subset)
        medians.append(median)
    if len(medians) <= 5:
        return hoare_median(medians)
    else:
        subsets = divide(medians)
        return get_pivot(subsets)


def quicksort(tab, counter=0):
    lower = []
    greater = []
    if len(tab) <= 1:
        return tab
    else:
        subsets = divide(tab)

        if counter < 3:
            print("\nZbiór podzielony na podzbiory:")
            print(subsets)
        p = get_pivot(subsets)
        if counter < 3:
            print("Element dzielący: ", p)
        index = 0
        for i in range(len(tab)):
            if tab[i] == p:
                index = i
                break
        for i in range(len(tab)):
            if i != index:
                if tab[i] < p:
                    lower.append(tab[i])
                else:
                    greater.append(tab[i])
        counter += 2
        return quicksort(lower, counter) + [p] + quicksort(greater, counter)


# tworzymy tablicę losowych liczb
losowe = []
for i in range(1000):
    losowe.append(random.randint(0, 100))

losowe_copy1 = losowe[:]
losowe_copy2 = losowe[:]


def main():
    print("METODY SHELLA I INSERTION SORT:\n")

    print("Pomiary czasu wykonywania się poszczególnych metod:")

    czas_shellsort = timeit("shellsort(losowe)", number=1, globals=globals())
    print("\nŚredni czas wykonania sortowania za pomocą metody shellsort wynosi {:.4f}s. ".format(czas_shellsort))

    sorted_tab, counter = shellsort(losowe)
    print("Liczba przesunięć w metodzie Shella: ", counter)


    czas_insertion = timeit("insertion_sort(losowe)", number=1, globals=globals())
    print("\nŚredni czas wykonania sortowania za pomocą metody insetrion wynosi {:.4f}s. ".format(czas_insertion))

    sorted_tab, counter = insertion_sort(losowe)
    print("Liczba przesunięć w metodzie insertion: ", counter)


    print("\n\nMETODA MEDIANA MEDIAN:\n")

    losowe2 = []
    for i in range(64):
        losowe2.append(random.randint(0, 100))

    print("Wygenerowany zbiór początkowy:")
    print(losowe2)

    print("\n\nPierwsze trzy podziały:")
    posortowane = quicksort(losowe2)

    print("\nPosortowany zbiór:")
    print(posortowane)


if __name__ == "__main__":
    main()
