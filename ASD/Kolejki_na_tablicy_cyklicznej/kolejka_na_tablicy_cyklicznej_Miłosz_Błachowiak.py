def realloc(tab, size):
    oldSize = len(tab)
    return [tab[i] if i < oldSize else None for i in range(size)]


class Queue:

    def __init__(self):
        self.size = 5
        self.tab = [None for i in range(self.size)]
        self.save_index = 0
        self.read_index = 0

    def is_empty(self):
        return self.save_index == self.read_index

    def peek(self):
        return self.tab[self.read_index]

    def dequeue(self):
        if self.is_empty():
            return None
        else:
            el = self.tab[self.read_index]
            self.read_index += 1
            if self.read_index >= self.size:
                self.read_index = 0
            return el

    def enqueue(self, el):
        self.tab[self.save_index] = el
        self.save_index += 1
        if self.save_index >= self.size:
            self.save_index = 0
        if self.save_index == self.read_index:    # realokacja, przesuwanie elementów i indeksów
            self.read_index += self.size
            self.save_index = self.read_index - self.size
            self.tab = realloc(self.tab, 2 * self.size)
            for i in range(self.save_index, self.size):
                self.tab[i], self.tab[i + self.size] = self.tab[i + self.size], self.tab[i]
            self.size = 2 * self.size

    def print_tab(self):
        print(self.tab)

    def print_queue(self):
        queue = []
        curr_index = self.read_index
        while curr_index != self.save_index:
            if self.tab[curr_index] is not None:
                queue.append(self.tab[curr_index])
            curr_index += 1
            if curr_index >= self.size:
                curr_index = 0
        print(queue)





def main():
    # pusta kolejka
    kolejka = Queue()

    # dodanie 4 kolejnych liczb
    kolejka.enqueue(1)
    kolejka.enqueue(2)
    kolejka.enqueue(3)
    kolejka.enqueue(4)

    print("Kolejka po wpisaniu 4 elementów:")
    kolejka.print_queue()

    print("\nOdczyt pierwszej wpisanej danej i 'wyciągnięcie' jej z kolejki")
    print(kolejka.dequeue())

    print("\nOdczyt drugiej wpisanej danej")
    print(kolejka.peek())

    # wypisanie aktualnego stanu kolejki
    print("\nObecny stan kolejki:")
    kolejka.print_queue()

    # użycie enqueue do wpisania kolejki kolejnych 4 danych
    kolejka.enqueue(5)
    kolejka.enqueue(6)
    kolejka.enqueue(7)
    kolejka.enqueue(8)

    # testowe wypisanie aktualnego stanu tablicy
    print("\nObecny stan tablicy (po dodaniu kolejnych 4 liczb):")
    kolejka.print_tab()

    print("\nOpróżnienie kolejki i wypisanie danych w pętli")
    while not kolejka.is_empty():
        print(kolejka.dequeue())

    print("\nSprawdzenie czy kolejka została poprawnie opróżniona (metoda is_empty()):")
    print(kolejka.is_empty())


if __name__ == "__main__":
    main()
