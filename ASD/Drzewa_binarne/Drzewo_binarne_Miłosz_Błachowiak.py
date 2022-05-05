class Node:
    def __init__(self, key=None, val=None):
        self.key = key
        self.value = val
        self.right = None
        self.left = None


class BST:
    def __init__(self):
        self.head = None

    def search(self, key, curr=None):
        if curr is None:
            curr = self.head
            if curr is None:
                return None
            else:
                return self.search(key, curr)
        else:
            if curr.key == key:
                return curr.value

            if key < curr.key:
                if curr.left is None:
                    return None
                else:
                    return self.search(key, curr.left)
            if key > curr.key:
                if curr.right is None:
                    return None
                else:
                    return self.search(key, curr.right)

    def insert(self, key, val, curr=None):
        if curr is None:
            curr = self.head
            if curr is None:
                self.head = Node(key, val)
            else:
                self.insert(key, val, curr)
        else:
            if curr.key == key:
                curr.value = val

            if key < curr.key:
                if curr.left is None:
                    curr.left = Node(key, val)
                else:
                    self.insert(key, val, curr.left)
            if key > curr.key:
                if curr.right is None:
                    curr.right = Node(key, val)
                else:
                    self.insert(key, val, curr.right)

    def delete(self, key, curr=None, prev=None):
        if curr is None:
            curr = self.head
            self.delete(key, curr)
        else:
            if curr.key == key:
                if curr.left and curr.right:
                    successor = curr.right

                    while successor.left:
                        p = successor
                        successor = successor.left
                        if successor.left is None:
                            p.left = successor.right
                            successor.right = curr.right

                    successor.left = curr.left
                    if prev:
                        if key < prev.key:
                            prev.left = successor
                        else:
                            prev.right = successor
                    else:
                        self.head = successor

                elif curr.left or curr.right:
                    if curr.left:
                        if prev:
                            if key < prev.key:
                                prev.left = curr.left
                            else:
                                prev.right = curr.left
                        else:
                            self.head = curr.left
                    elif curr.right:
                        if prev:
                            if key < prev.key:
                                prev.left = curr.right
                            else:
                                prev.right = curr.right
                        else:
                            self.head = curr.right

                else:
                    if prev:
                        if key < prev.key:
                            prev.left = None
                        else:
                            prev.right = None
                    else:
                        self.head = None

            elif key < curr.key and curr.left:
                self.delete(key, curr.left, curr)
            elif key > curr.key and curr.right:
                self.delete(key, curr.right, curr)

    def height(self):
        return self.height_help(self.head)

    def height_help(self, curr):
        if curr is None:
            return 0
        else:
            left_height = self.height_help(curr.left)
            right_height = self.height_help(curr.right)

            if left_height > right_height:
                return left_height + 1
            else:
                return right_height + 1

    def print(self):
        self.print_help(self.head)
        print("\n")

    def print_help(self, curr=None):
        if curr:
            self.print_help(curr.left)

            node_str = str(curr.key) + ":" + str(curr.value)
            print(node_str, end=" ")

            self.print_help(curr.right)

    def print_tree(self):
        print("==============")
        self._print_tree(self.head, 0)
        print("==============")

    def _print_tree(self, node, lvl):
        if node != None:
            self._print_tree(node.right, lvl + 10)

            print()
            for i in range(10, lvl + 10):
                print(end=" ")
            print(node.key)
            self._print_tree(node.left, lvl + 10)


def main():
    # utworzenie pustego drzewa
    tree = BST()

    # wstawienie kolejnych elementów
    tree.insert(50, "A")
    tree.insert(15, "B")
    tree.insert(62, "C")
    tree.insert(5, "D")
    tree.insert(20, "E")
    tree.insert(58, "F")
    tree.insert(91, "G")
    tree.insert(3, "H")
    tree.insert(8, "I")
    tree.insert(37, "J")
    tree.insert(60, "K")
    tree.insert(24, "L")

    print("Struktura drzewa w formie 2D po wstawieniu 12 elementów:")
    tree.print_tree()

    print("Struktura drzewa od najmniejszego do największego klucza w formie klucz:wartość:")
    tree.print()

    print("Wartość dla klucza 24: ", tree.search(24))

    # zaktualizowanie wartości dla klucza 15
    tree.insert(15, "AA")

    # dodanie i usuwanie elementów
    tree.insert(6, "M")
    tree.delete(62)
    tree.insert(59, "N")
    tree.insert(100, "P")
    tree.delete(8)
    tree.delete(15)
    tree.insert(55, "R")
    tree.delete(50)
    tree.delete(5)
    tree.delete(24)

    print("\nWysokość drzewa po dodaniu i usunięciu kilku elementów: ", tree.height())

    print("\nObecna struktura drzewa od najmniejszego do największego klucza w formie klucz:wartość:")
    tree.print()

    print("Obecna struktura drzewa w formie 2D:")
    tree.print_tree()


if __name__ == "__main__":
    main()
