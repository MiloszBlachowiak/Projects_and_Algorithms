from random import random


def randomLevel(p, maxLevel):
    lvl = 1
    while random() < p and lvl < maxLevel:
        lvl = lvl + 1
    return lvl


class Element:
    def __init__(self, key, val, lvls):
        self.key = key
        self.val = val
        self.lvls = lvls
        self.next = [None for i in range(lvls)]


class SkipList:

    def __init__(self, max_lvl):
        self.head = Element(None, None, max_lvl)
        self.max_lvl = max_lvl

    def search(self, key):
        curr = self.head

        for i in range(self.max_lvl-1, -1, -1):
            while curr.next[i] and curr.next[i].key < key:
                curr = curr.next[i]
        if curr.next[0] and curr.next[0].key == key:
            return curr.next[0].val
        else:
            return None

    def insert(self, key, val):
        curr = self.head
        prev_nodes = [None for i in range(self.max_lvl)]

        for i in range(self.max_lvl-1, -1, -1):
            while curr.next[i] and curr.next[i].key < key:
                curr = curr.next[i]
            if curr is None:
                prev_nodes[i] = self.head
            else:
                prev_nodes[i] = curr

        curr = curr.next[0]

        if curr is None or curr.key != key:
            level = randomLevel(0.5, self.max_lvl)
            new_el = Element(key, val, level)
            for i in range(level):
                new_el.next[i] = prev_nodes[i].next[i]
                prev_nodes[i].next[i] = new_el
        else:
            curr.val = val

    def remove(self, key):
        curr = self.head
        prev_nodes = [None for i in range(self.max_lvl)]

        for i in range(self.max_lvl - 1, -1, -1):
            while curr.next[i] and curr.next[i].key < key:
                curr = curr.next[i]
            if curr is None:
                prev_nodes[i] = self.head
            else:
                prev_nodes[i] = curr

        curr = curr.next[0]

        if curr and curr.key == key:
            for i in range(curr.lvls):
                prev_nodes[i].next[i] = curr.next[i]

    def __str__(self):
        node = self.head.next[0]
        list_str = "["
        while node and node.next[0]:
            list_str += "(" + str(node.key) + ": " + str(node.val) + "), "
            node = node.next[0]
        if node:
            list_str += "(" + str(node.key) + ": " + str(node.val) + ")"
        list_str += "]"
        return list_str

    def displayList_(self):
        node = self.head.next[0]  # pierwszy element na poziomie 0
        keys = []  # lista kluczy na tym poziomie
        while node is not None:
            keys.append(node.key)
            node = node.next[0]

        for lvl in range(self.max_lvl - 1, -1, -1):
            print("{}: ".format(lvl), end=" ")
            node = self.head.next[lvl]
            idx = 0
            while node is not None:
                while node.key > keys[idx]:
                    print("  ", end=" ")
                    idx += 1
                idx += 1
                print("{:2d}".format(node.key), end=" ")
                node = node.next[lvl]
            print("")


def main():
    # tworzymy pustą listę o maksymalnej wysokości wynoszącej 5
    lista = SkipList(5)

    letter = 65
    # wstawiamy 15 elementów
    for i in range(1, 16):
        lista.insert(i, chr(letter))
        letter += 1

    print("Wypisanie listy po dodaniu 15 danych:")
    lista.displayList_()

    print("\nWyszukana dana o kluczu 2: ", lista.search(2))

    # nadpisujemy wartość dla klucza 2
    lista.insert(2, chr(letter))
    letter += 1

    print("Wyszukana dana o kluczu 2 po nadpisaniu jej wartości: ", lista.search(2))

    # usuwamy dane o kluczach 5, 6 i 7
    lista.remove(5)
    lista.remove(6)
    lista.remove(7)

    print("\nWypisanie tablicy (poziomu 0 listy) po usunięciu wartości dla kluczy 5, 6 i 7")
    print(lista)

    # wstawiamy daną o kluczu 6
    lista.insert(6, chr(letter))

    print("\nWypisanie tablicy (poziomu 0 listy) po wstawieniu wartości o kluczu 6.")
    print(lista)

    print("\nWypisanie stanu listy:")
    lista.displayList_()

    lista2 = SkipList(5)
    letter = 65
    # wstawiamy 15 elementów
    for i in range(15, 0, -1):
        lista2.insert(i, chr(letter))
        letter += 1

    print("\nWypisanie listy po wstawieniu 15 danych w odwrotnej kolejności (od 15 do 1):")
    lista2.displayList_()

    print("\nWypisanie tablicy (poziomu 0 listy).")
    print(lista2)


if __name__ == "__main__":
    main()
