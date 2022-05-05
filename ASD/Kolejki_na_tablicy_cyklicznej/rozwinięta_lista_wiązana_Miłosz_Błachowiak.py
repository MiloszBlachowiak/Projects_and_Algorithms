size = 6


class Element:

    def __init__(self):
        global size
        self.size = size
        self.tab = [None for i in range(self.size)]
        self.nr_of_elements = 0
        self.next = None

    def add(self, val, index):
        if index > self.nr_of_elements:
            index = self.nr_of_elements
        if self.tab[index] is None:
            self.tab[index] = val
        else:
            curr_el = self.tab[index]
            self.tab[index] = val
            while curr_el:
                next_el = self.tab[index+1]
                self.tab[index+1] = curr_el
                curr_el = next_el
                index += 1
        self.nr_of_elements += 1

    def remove(self, index):
        if index > self.nr_of_elements:
            index = self.nr_of_elements - 1
        if self.tab[index] is not None:
            self.tab[index] = None
            i = index + 1
            curr_el = self.tab[i]
            while curr_el:
                self.tab[i - 1] = curr_el
                if i + 1 < self.size:
                    curr_el = self.tab[i + 1]
                else:
                    curr_el = None
                i += 1
            self.tab[i-1] = None
            self.nr_of_elements -= 1


class UnrolledLinkedList:

    def __init__(self):
        self.list = Element()

    def get(self, index):
        node = self.list
        while index >= node.nr_of_elements:
            index -= node.nr_of_elements
            node = node.next
        return node.tab[index]

    def insert(self, val, index):
        node = self.list
        while node is not None:
            if node.next is None:
                if node.nr_of_elements < node.size:
                    node.add(val, index)
                    node = None
                else:
                    if index >= node.size:
                        node.next = Element()
                        node.next.add(val, 0)
                        node = None
                    else:
                        node.next = Element()
                        half_size = round(node.size / 2)
                        for i in range(half_size, node.size):
                            node.next.add(node.tab[half_size], i - half_size)
                            node.remove(half_size)
                        if index <= half_size:
                            node.add(val, index)
                        else:
                            node.next.add(val, index - half_size)
                        node = None
            else:
                if index > node.nr_of_elements:
                    index -= node.nr_of_elements
                    node = node.next
                else:
                    if node.nr_of_elements < node.size:
                        node.add(val, index)
                    else:
                        next_el = node.next
                        node.next = Element()
                        node.next.next = next_el
                        half_size = round(node.size / 2)
                        for i in range(half_size, node.size):
                            node.next.add(node.tab[half_size], i - half_size)
                            node.remove(half_size)
                        if index <= half_size:
                            node.add(val, index)
                        else:
                            node.next.add(val, index - half_size)
                    node = None

    def delete(self, index):
        node = self.list
        half_size = round(node.size / 2)
        while index >= node.nr_of_elements:
            index -= node.nr_of_elements
            node = node.next
        node.remove(index)
        if node.nr_of_elements < half_size and node.next is not None:
            node.add(node.next.tab[0], node.nr_of_elements)
            node.next.remove(0)
            if node.next.nr_of_elements < half_size:
                for el in node.next.tab:
                    if el is not None:
                        node.add(el, node.nr_of_elements)
                if node.next.next is not None:
                    node.next = node.next.next

    def print_list(self):
        node = self.list
        list_str = "[ "
        while node is not None:
            for i in range(node.size):
                if node.tab[i] is not None:
                    list_str += str(node.tab[i])
                    if node.next is None and (i+1 == node.size or node.tab[i+1] is None):
                        list_str += "]"
                    else:
                        list_str += ", "
            node = node.next
        print(list_str)


def main():
    # utworzenie pustej listy
    list = UnrolledLinkedList()

    # wstawienie do listy kolejnych 9-ciu elementów w pętli
    for i in range(9):
        list.insert(i+1, i)


    print("Wypisanie 4. elementu z listy 9-kolejnych liczb:")
    print(list.get(3))

    # wstawienie 2-ch danych pod indeksy 1 i 8
    list.insert(10, 1)
    list.insert(11, 8)

    print("Wypisanie stanu listy po wstawieniu dwóch danych (liczb 10 i 11) pod indeksy 1 i 8:")
    list.print_list()

    # usunięcie danych spod indeksów 1 i 2
    list.delete(1)
    list.delete(2)

    print("Wypisanie stanu listy po usunięciu dwóch danych spod indeksów 1 i 2:")
    list.print_list()


if __name__ == "__main__":
    main()
