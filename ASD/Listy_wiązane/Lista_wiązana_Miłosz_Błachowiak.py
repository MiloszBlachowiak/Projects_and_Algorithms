class Element:

    def __init__(self, element):
        self.data = element
        self.next = None


class LinkedList:

    def __init__(self):
        self.head = None

    def destroy(self):
        self.head = None

    def add(self, element):
        if self.head is not None:
            prev_head = self.head
            self.head = Element(element)
            self.head.next = prev_head
        else:
            self.head = Element(element)

    def remove(self):
        self.head = self.head.next

    def is_empty(self):
        return self.head is None

    def length(self):
        counter = 0
        curr_el = self.head
        while curr_el is not None:
            counter += 1
            curr_el = curr_el.next
        return counter

    def get(self):
        if self.head is not None:
            return self.head.data
        else:
            return None

    def __str__(self):
        string = "[ "
        curr_el = self.head
        if curr_el is not None:
            while curr_el is not None:
                string += str(curr_el.data)
                curr_el = curr_el.next
                if curr_el is not None:
                    string += ", "
                else:
                    string += "]"
        else:
            string += "]"
        return string

    def push_back(self, element):
        curr_el = self.head
        if curr_el is not None:
            while curr_el.next is not None:
                curr_el = curr_el.next
            new = Element(element)
            curr_el.next = new
        else:
            self.head = Element(element)

    def remove_last(self):
        if self.head is not None:
            if self.head.next is None:
                self.head = None
            else:
                curr_el = self.head
                prev_el = curr_el
                while curr_el.next is not None:
                    prev_el = curr_el
                    curr_el = curr_el.next
                prev_el.next = None

    def revert(self):
        curr_el = self.head
        elements = []
        if curr_el is not None:
            while curr_el is not None:
                elements.append(curr_el.data)
                curr_el = curr_el.next
            self.destroy()
            for el in elements:
                self.add(el)

    def take(self, n):
        new_list = LinkedList()
        curr_el = self.head
        counter = 0
        while curr_el is not None and counter < n:
            new_list.push_back(curr_el.data)
            counter += 1
            curr_el = curr_el.next
        return new_list

    def drop(self, n):
        self.revert()
        new_list = self.take(self.length()-n)
        new_list.revert()
        return new_list


def main():
    lista_krotek = [
        ('AGH', 'Krak??w', 1919),
        ('UJ', 'Krak??w', 1364),
        ('PW', 'Warszawa', 1915),
        ('UW', 'Warszawa', 1915),
        ('UP', 'Pozna??', 1919),
        ('PG', 'Gda??sk', 1945)
        ]

    # Utworzenie listy wi??zanej i dodanie do niej trzech krotek za pomoc?? metody add
    linked_list = LinkedList()
    linked_list.add(lista_krotek[0])
    linked_list.add(lista_krotek[1])
    linked_list.add(lista_krotek[2])
    print("\nLista wi??zana po dodaniu 3 element??w na pocz??tek:")
    print(linked_list)

    # metoda revert - odwracanie kolejno??ci
    linked_list.revert()
    print("\nLista odwr??cona:")
    print(linked_list)

    # metoda push_back - dodanie na koniec elementu
    linked_list.push_back(lista_krotek[3])
    linked_list.push_back(lista_krotek[4])
    print("\nLista po dodaniu  2 element??w na koniec:")
    print(linked_list)

    # metoda length
    print("\nD??ugo???? listy wi??zanej:")
    print(linked_list.length())

    # metoda get
    first_el = linked_list.get()
    print("\nPierwszy element listy:")
    print(first_el)

    # metoda remove
    linked_list.remove()
    print("\nLista po usuni??ciu pierwszego elementu:")
    print(linked_list)

    # metoda remove_last
    linked_list.remove_last()
    print("\nLista po usuni??ciu ostatniego elementu:")
    print(linked_list)

    #metoda take(n) dla n = 2
    first_two = linked_list.take(2)
    print("\nNowa lista wi??zana stworzona z 2 pierwszych element??w listy:")
    print(first_two)

    # metoda drop(n) dla n = 2
    last_two = linked_list.drop(2)
    print("\nNowa lista wi??zana stworzona po odrzuceniu 2 pierwszych element??w listy:")
    print(last_two)

    # metoda destroy
    linked_list.destroy()
    print("\nLista wi??zana po u??yciu metody destroy:")
    print(linked_list)

    # metoda is_empty
    print("\nSprawdzanie czy lista jest pusta:")
    print(linked_list.is_empty())

    # utworzenie od nowa listy wi??zanej z podanej listy
    for el in lista_krotek:
        linked_list.push_back(el)
    print("\nLista wi??zana stworzona z podanej listy krotek:")
    print(linked_list)

if __name__ == "__main__":
    main()
