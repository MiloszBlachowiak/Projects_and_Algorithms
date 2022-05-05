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


def main():
    # utworzenie pustej kolejki
    queue = PriorityQueue()

    # wstawienie kolejnych elementów
    word = "algorytm"
    keys = [4, 7, 2, 5, 7, 6, 2, 1]

    i = 0
    for letter in word:
        queue.enqueue(letter, keys[i])
        i += 1

    print("Aktualny stan kolejki po dodaniu elementów w pętli:")
    queue.print_as_heap()

    print("Pierwsza dana z 'wyciągnięta' kolejki przez metodę dequeue: ", queue.dequeue())

    print("\nDana o obecnie największym priorytecie uzyskana przez metodę peek: ", queue.peek())

    print("Aktualny stan kolejki w postaci tablicy:")
    queue.print_as_tab()

    print("\nOpróżnienie kolejki i wypisanie 'wyciaganych' elementów")
    while queue.tab:
        print(queue.dequeue(), end=" ")
    print("\n")

    print("Próba wypisania opróżnionej kolejki w postaci kopca:")
    queue.print_as_heap()


if __name__ == "__main__":
    main()
