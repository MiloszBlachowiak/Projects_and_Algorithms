from Lista_wiązana_Miłosz_Błachowiak import Element


# ===INTERFEJS LISTY ABSTRAKCYJNEJ===

def nil():
    return None


def cons(el, lst):
    if lst is not None:
        prev_head = lst
        lst = Element(el)
        lst.next = prev_head
    else:
        lst = Element(el)
    return lst


def first(lst):
    return lst.data


def rest(lst):
    return lst.next


# ====LISTA WIĄZANA====
def create():
    return nil()


def destroy():
    return nil()


def add(el, lst):
    return cons(el, lst)


def remove(lst):
    return rest(lst)


def is_empty(lst):
    return not lst


def length(lst):
    if is_empty(lst):
        return 0
    else:
        return 1 + length(rest(lst))


def get(lst):
    return first(lst)


def print_list(lst):
    def lst_to_str(l):
        if length(l) == 0:
            return ""
        if length(l) == 1:
            return str(first(l)) + lst_to_str(rest(l))  # żeby na końcu listy nie wyświetlał się przecinek
        else:
            return str(first(l)) + ", " + lst_to_str(rest(l))

    list_str = "[ " + lst_to_str(lst) + " ]"
    print(list_str)


def push_back(el, lst):
    if is_empty(lst):
        return cons(el, lst)
    else:
        return cons(first(lst), push_back(el, rest(lst)))


def remove_last(lst):
    if length(lst) <= 1:
        return nil()
    else:
        return cons(first(lst), remove_last(rest(lst)))


def revert(lst, acc=None):
    if acc is None:
        acc = []
    if is_empty(lst):
        return acc
    else:
        return revert(rest(lst), cons(first(lst), acc))


def take(n, lst):
    if n > length(lst):
        return lst
    elif n <= 0:
        return nil()
    else:
        return cons(first(lst), take(n-1, rest(lst)))


def drop(n, lst):
    lst = revert(lst)
    lst = take(length(lst) - n, lst)
    lst = revert(lst)
    return lst


# ===MAIN===
def main():
    lista_krotek = [
        ('AGH', 'Kraków', 1919),
        ('UJ', 'Kraków', 1364),
        ('PW', 'Warszawa', 1915),
        ('UW', 'Warszawa', 1915),
        ('UP', 'Poznań', 1919),
        ('PG', 'Gdańsk', 1945)
        ]

    # Utworzenie listy wiązanej i dodanie do niej trzech krotek za pomocą metody add
    linked_list = create()
    linked_list = add(lista_krotek[0], linked_list)
    linked_list = add(lista_krotek[1], linked_list)
    linked_list = add(lista_krotek[2], linked_list)
    print("\nLista wiązana po dodaniu 3 elementów na początek:")
    print_list(linked_list)

    # metoda revert - odwracanie kolejności
    linked_list = revert(linked_list)
    print("\nLista odwrócona:")
    print_list(linked_list)

    # metoda push_back - dodanie na koniec elementu
    linked_list = push_back(lista_krotek[3], linked_list)
    linked_list = push_back(lista_krotek[4], linked_list)
    print("\nLista po dodaniu  2 elementów na koniec:")
    print_list(linked_list)

    # metoda length
    print("\nDługość listy wiązanej:")
    print(length(linked_list))

    # metoda get
    first_el = get(linked_list)
    print("\nPierwszy element listy:")
    print(first_el)

    # metoda remove
    linked_list = remove(linked_list)
    print("\nLista po usunięciu pierwszego elementu:")
    print_list(linked_list)

    # metoda remove_last
    linked_list = remove_last(linked_list)
    print("\nLista po usunięciu ostatniego elementu:")
    print_list(linked_list)

    #metoda take(n) dla n = 2
    first_two = take(2, linked_list)
    print("\nNowa lista wiązana stworzona z 2 pierwszych elementów listy:")
    print_list(first_two)

    # metoda drop(n) dla n = 2
    last_two = drop(2, linked_list)
    print("\nNowa lista wiązana stworzona po odrzuceniu 2 pierwszych elementów listy:")
    print_list(last_two)

    # metoda destroy
    linked_list = destroy()
    print("\nLista wiązana po użyciu metody destroy:")
    print_list(linked_list)

    # metoda is_empty
    print("\nSprawdzanie czy lista jest pusta:")
    print(is_empty(linked_list))

    # utworzenie od nowa listy wiązanej z podanej listy
    for el in lista_krotek:
        linked_list = push_back(el, linked_list)
    print("\nLista wiązana stworzona z podanej listy krotek:")
    print_list(linked_list)

if __name__ == "__main__":
    main()


