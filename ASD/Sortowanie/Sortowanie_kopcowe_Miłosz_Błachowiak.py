from timeit import timeit
import random


class Element:
    def __init__(self, value, priority):
        self.value = value
        self.priority = priority

    def __lt__(self, other):
        pri1 = self.priority
        pri2 = other.priority
        return pri1 < pri2

    def __gt__(self, other):
        pri1 = self.priority
        pri2 = other.priority
        return pri1 > pri2

    def __str__(self):
        return str(self.value)


class PriorityQueue:
    def __init__(self):
        self.tab = []
        self.size = 0

    def is_empty(self):
        return self.size == 0

    def peek(self):
        if self.tab:
            return self.tab[0]
        else:
            return None

    def dequeue(self):
        if self.tab:
            self.size -= 1
            return self.tab.pop(0).value
        else:
            return None

    def enqueue(self, value, priority):
        self.tab.append(Element(value, priority))
        self.size += 1
        index = self.size - 1
        while index > 0 and self.tab[index - 1] < self.tab[index]:
            self.tab[index - 1], self.tab[index] = self.tab[index], self.tab[index - 1]
            index -= 1

    def print_as_tab(self):
        tab = [el.value for el in self.tab]
        print(tab)

    def print_as_heap(self):
        print("======== KOPIEC ========")
        if self.tab:
            size = self.size - 1
            levels = 1
            el_in_lvl = 1
            while size > 0:
                levels += 1
                el_in_lvl *= 2
                size -= el_in_lvl

            index = 0
            nr = 1
            for lvl in range(levels, 0, -1):
                for n in range(nr):
                    for i in range(levels*el_in_lvl):
                        print(end=" ")
                    if index < self.size:
                        print(self.tab[index], end="")
                    for i in range(levels*el_in_lvl):
                        print(end=" ")
                    index += 1
                print("\n")
                nr *= 2
                el_in_lvl //= 2
        print("========================")
        print("\n")


# ===================================


def heapify_help(tab, idx, size):
    minimum = idx
    left = 2 * idx + 1
    right = left + 1

    if left < size and tab[left] < tab[idx]:
        minimum = left
    if right < size and tab[minimum] > tab[right]:
        minimum = right

    if minimum != idx:
        tab[idx], tab[minimum] = tab[minimum], tab[idx]
        heapify_help(tab, minimum, size)


def heapify(tab):
    size = len(tab)
    last_parent = size - ((size + 1) // 2) - 1

    for idx in range(last_parent, -1, -1):
        heapify_help(tab, idx, size)

    for idx in range(size-1, 0, -1):
        tab[0], tab[idx] = tab[idx], tab[0]
        heapify_help(tab, 0, idx)

def sortuj_heapify(lista):
    # utworzenie listy elementów (obiektów klasy Element)
    lista_elementow = []
    for el in lista:
        element = Element(el, el)
        lista_elementow.append(element)

    # utworzenie kopca za pomocą heapify
    heapify(lista_elementow)
    heapify_heap = PriorityQueue()
    heapify_heap.tab = lista_elementow
    heapify_heap.size = len(lista_elementow)


    # zdejmowanie elementów z kopca przez dequeue
    sorted_heapify = []
    for i in range(heapify_heap.size):
        sorted_heapify.insert(0, heapify_heap.dequeue())

    return sorted_heapify

def sortuj_heapify_print(lista):
    print("Początkowa tablica:")
    print(lista)
    # utworzenie listy elementów (obiektów klasy Element)
    lista_elementow = []
    for el in lista:
        element = Element(el, el)
        lista_elementow.append(element)

    # utworzenie kopca za pomocą heapify
    heapify(lista_elementow)
    heapify_heap = PriorityQueue()
    heapify_heap.tab = lista_elementow
    heapify_heap.size = len(lista_elementow)

    print("\nWypisujemy utworzony kopiec:")
    heapify_heap.print_as_heap()

    # zdejmowanie elementów z kopca przez dequeue
    sorted_heapify = []
    for i in range(heapify_heap.size):
        sorted_heapify.insert(0, heapify_heap.dequeue())
    print("Posortowana tablica:")
    print(sorted_heapify)


def sortuj_enqueue(unsorted):
    heap = PriorityQueue()
    for el in unsorted:
        heap.enqueue(el, el)
    sorted = []
    for i in range(heap.size):
        sorted.insert(0, heap.dequeue())
    return sorted


# tworzymy tablicę losowych liczb
losowe = random.sample(range(1, 10000), 1000)
losowe_copy1 = losowe[:]
losowe_copy2 = losowe[:]


def main():
    # TESTY

    # METODA HEAPIFY

    # tablica priorytetów
    priorytety = [3, 6, 1, 8, 4, 12, 7, 13, 9, 22, 15, 5, 11, 16, 18, 20, 25, 21, 27, 30]

    # wykonujemy sortowanie metodą heapify i wypisujemy wyniki
    sortuj_heapify_print(priorytety)


    # tworzymy tablicę losowych liczb
    losowe = random.sample(range(0, 10001), 1000)

    print("Pomiary czasu wykonywania się poszczególnych metod:")
    czas_heapify = timeit("sortuj_heapify(losowe_copy1)", number=1, globals=globals()) / 1
    print("\nŚredni czas wykonania sortowania za pomocą metody heapify wynosi {:.4f}s. ".format(czas_heapify))


    # METODA ENQUEUE
    czas_enqueue = timeit("sortuj_enqueue(losowe_copy2)", number=1, globals=globals()) / 1
    print("\nŚredni czas wykonania sortowania za pomocą metody enqueue wynosi {:.4f}s. ".format(czas_enqueue))

if __name__ == "__main__":
    main()
