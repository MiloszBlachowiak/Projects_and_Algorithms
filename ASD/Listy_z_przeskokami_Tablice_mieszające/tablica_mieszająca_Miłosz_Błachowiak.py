class Element:
    def __init__(self, key, val):
        self.key = key
        self.val = val


class HashTable:

    def __init__(self, size=13, c1=1, c2=0):
        self.table = [None for i in range(size)]
        self.size = size
        self.c1 = c1
        self.c2 = c2

    def hash(self, key):
        if isinstance(key, str):
            val_sum = 0
            for l in key:
                val_sum += ord(l)
            key = val_sum
        return key % self.size

    def probe(self, hv, i):
        return (hv + self.c1 * i + self.c2 * i**2) % self.size

    def search(self, key):
        hv = self.hash(key)
        if self.table[hv].key == key:
            return self.table[hv].val
        elif self.table[hv] is None:
            return None
        else:
            i = 1
            while i < self.size:
                index = self.probe(hv, i)
                if self.table[index].key == key:
                    return self.table[index].val
                elif self.table[index] is None:
                    return None
                else:
                    i += 1

    def insert(self, key, val):
        hv = self.hash(key)
        if self.table[hv] is None:
            self.table[hv] = Element(key, val)
        elif self.table[hv].val is None:
            self.table[hv].key = key
            self.table[hv].val = val
        elif self.table[hv].key == key:
            self.table[hv] = Element(key, val)
        else:
            i = 1
            index = hv
            while self.table[index].key != key and i < self.size:
                index = self.probe(hv, i)
                if self.table[index] is None:
                    self.table[index] = Element(key, val)
                elif self.table[index].val is None:
                    self.table[index].val = val
                    self.table[index].key = key
                elif self.table[index].key == key:
                    self.table[index].val = val
                else:
                    i += 1
            if i == self.size:
                print("Brak miejsca dla elementu o kluczu {}!".format(key))
                return None

    def remove(self, key):
        hv = self.hash(key)
        if self.table[hv] is None:
            return None
        elif self.table[hv].key == key:
            self.table[hv].val = None
        else:
            i = 1
            index = hv
            while self.table[index].val is not None and i < self.size:
                index = self.probe(hv, i)
                if self.table[index] is None:
                    return None
                elif self.table[index].key == key:
                    self.table[index].val = None
                else:
                    i += 1

    def __str__(self):
        list_str = "["
        for i in range(self.size):
            if self.table[i] is not None:
                if self.table[i].val is not None:
                    if list_str == "[":
                        list_str += '(' + str(self.table[i].key) + ': ' + str(self.table[i].val) + ')'
                    else:
                        list_str += ', (' + str(self.table[i].key) + ': ' + str(self.table[i].val) + ')'
        list_str += "]"
        return list_str

    def print_whole(self):
        list_str = "["
        for i in range(self.size):
            if self.table[i] is not None:
                if list_str == "[":
                    list_str += '(' + str(self.table[i].key) + ': ' + str(self.table[i].val) + ')'
                else:
                    list_str += ', (' + str(self.table[i].key) + ': ' + str(self.table[i].val) + ')'
            else:
                if list_str == "[":
                    list_str += str(None)
                else:
                    list_str += ', ' + str(None)
        list_str += "]"
        print(list_str)


def test1():
    print("Pierwszy test:")
    # utworzenie tablicy o rozmiarze 13
    table = HashTable(13)
    letter = 65

    print("\nTworzymy now?? tablic?? i pr??bujemy wstawi?? 15 element??w")
    for i in range(1, 16):
        if i != 6 and i != 7:
            table.insert(i, chr(letter))
            letter += 1
        if i == 6:
            table.insert(18, chr(letter))
            letter += 1
        if i == 7:
            table.insert(31, chr(letter))
            letter += 1

    print("\nWypisanie tablicy po wstawieniu 15 danych:")
    print(table)

    print("\nWypisanie elementu o indeksie 5:")
    print(table.search(5))

    print("\nWypisanie elementu o indeksie 14:")
    print(table.search(14))

    # nadpisanie warto??ci pod kluczem 5
    table.insert(5, chr(letter))

    print("\nWypisanie elementu o indeksie 5 po nadpisaniu warto??ci pod tym kluczem:")
    print(table.search(5))

    table.remove(5)

    print("\nWypisanie tablicy po usuni??ciu elementu o kluczu 5 (bez pustych miejsc):")
    print(table)

    print("\nWypisanie tablicy po usuni??ciu elementu o kluczu 5 w ca??o??ci (z pustymi miejscami):")
    table.print_whole()

    print("\nWypisanie elementu o kluczu 5:")
    print(table.search(5))

    # Wstawienie warto??ci 'A' z kluczem 'test'
    table.insert('test', 'A')

    print("\nWypisanie tablicy po wstawieniu litery 'A' pod kluczem 'test'")
    print(table)


def test2():
    print("Drugi test:\n")
    # utworzenie tablicy o rozmiarze 13
    table = HashTable(13)
    letter = 65

    print("\nTworzymy now?? tablic?? i pr??bujemy wstawi?? 15 element??w")
    for i in range(1, 16):
        table.insert(i * 13, chr(letter))
        letter += 1

    print("\nWypisanie tablicy po wstawieniu 15 danych:")
    print(table)

    print("\nTworzymy now?? tablic?? z pr??bkowaniem kwadratowym i pr??bujemy wstawi?? 15 element??w:")
    # utworzenie tablicy o rozmiarze 13
    table = HashTable(13, 0, 1)
    letter = 65

    # wstawiamy 15 element??w
    for i in range(1, 16):
        table.insert(i * 13, chr(letter))
        letter += 1

    print("\nSprawdzanie zaj??to??ci tablicy po wstawieniu 15 danych:")
    table.print_whole()



    print("\nTworzymy now?? tablic?? z pr??bkowaniem kwadratowym z kluczami z pierwszej funkcji testuj??cej:")
    # utworzenie tablicy o rozmiarze 13
    table = HashTable(13, 0, 1)
    letter = 65

    # wstawiamy 15 element??w
    for i in range(1, 16):
        if i != 6 and i != 7:
            table.insert(i, chr(letter))
            letter += 1
        if i == 6:
            table.insert(18, chr(letter))
            letter += 1
        if i == 7:
            table.insert(31, chr(letter))
            letter += 1

    print("\nSprawdzanie zaj??to??ci tablicy po wstawieniu 15 danych:")
    table.print_whole()


def main():
    test1()

    test2()


if __name__ == "__main__":
    main()
