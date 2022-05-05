class Element:
    def __init__(self, value, data):
        self.value = value
        self.data = data

    def __lt__(self, other):
        val1 = self.value
        val2 = other.value
        return val1 < val2

    def __gt__(self, other):
        val1 = self.value
        val2 = other.value
        return val1 > val2

    def __str__(self):
        return str(self.value)


class Sort:
    def __init__(self):
        self.tab = []

    def insert(self, val, data):
        element = Element(val, data)
        self.tab.append(element)

    def swap_sort(self):
        for i in range(len(self.tab)):
            m = i
            for j in range(i, len(self.tab)):
                if self.tab[j] < self.tab[m]:
                    m = j
            self.tab[i], self.tab[m] = self.tab[m], self.tab[i]

    def shift_sort(self):
        for i in range(1, len(self.tab)):
            t = self.tab[i]
            j = i - 1
            while j >= 0 and self.tab[j] > t:
                self.tab[j + 1], self.tab[j] = self.tab[j], self.tab[j+1]
                j -= 1
            self.tab[j+1] = t

    def print_tab(self):
        tab_ = []
        for el in self.tab:
            tab_.append((el.value, el.data))
        print(tab_)


def main():
    # tablica wejściowa
    tab = [(5, 'A'), (5, 'B'), (7, 'C'), (2, 'D'), (5, 'E'), (1, 'F'), (7, 'G'), (5, 'H'), (1, 'I'), (2, 'J')]

    # sortowanie przez wybieranie (z zamianami)
    sort1 = Sort()
    for el in tab:
        sort1.insert(el[0], el[1])

    # wykonujemy sortowanie
    sort1.swap_sort()
    print("Wyświetlamy tablicę posortowaną za pomocą metody wykorzystującej zamianę miejscami:")
    sort1.print_tab()


    # sortowanie z przesunięciami (sortowanie przez wstawianie)
    sort2 = Sort()
    for el in tab:
        sort2.insert(el[0], el[1])

    # wykonujemy sortowanie
    sort2.shift_sort()
    print("\nWyświetlamy tablicę posortowaną za pomocą metody wykorzystującej przesunięcia:")
    sort2.print_tab()


if __name__ == "__main__":
    main()
