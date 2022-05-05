from Drzewo_binarne_Miłosz_Błachowiak import BST, Node


class NodeAVL(Node):
    def __init__(self, key, val):
        super().__init__(key, val)
        self.balance = 0


class AVL(BST):
    def __init__(self):
        super().__init__()

    def insert(self, key, val, curr=None, prev=None):
        if curr is None:
            curr = self.head
            if curr is None:
                self.head = NodeAVL(key, val)
            else:
                self.insert(key, val, curr)
        else:
            if curr.key == key:
                curr.value = val

            if key < curr.key:
                if curr.left is None:
                    curr.left = NodeAVL(key, val)
                else:
                    self.insert(key, val, curr.left, curr)
            if key > curr.key:
                if curr.right is None:
                    curr.right = NodeAVL(key, val)
                else:
                    self.insert(key, val, curr.right, curr)

        if curr is not None:
            curr.balance = self.height(curr.left) - self.height(curr.right)

            # LL
            if curr.balance > 1 and key < curr.left.key:
                if curr == self.head:
                    self.head = self.rotate_right(curr)
                else:
                    if curr.key > prev.key:
                        prev.right = self.rotate_right(curr)
                    else:
                        prev.left = self.rotate_right(curr)

            # RR
            elif curr.balance < -1 and key > curr.right.key:
                if curr == self.head:
                    self.head = self.rotate_left(curr)
                else:
                    if curr.key > prev.key:
                        prev.right = self.rotate_left(curr)
                    else:
                        prev.left = self.rotate_left(curr)

            # RL
            elif curr.balance < -1 and key < curr.right.key:
                curr.right = self.rotate_right(curr.right)
                if curr == self.head:
                    self.head = self.rotate_left(curr)
                else:
                    if curr.key > prev.key:
                        prev.right = self.rotate_left(curr)
                    else:
                        prev.left = self.rotate_left(curr)

            # LR
            elif curr.balance > 1 and key > curr.left.key:
                curr.left = self.rotate_left(curr.left)

                if curr == self.head:
                    self.head = self.rotate_right(curr)
                else:
                    if curr.key > prev.key:
                        prev.right = self.rotate_right(curr)
                    else:
                        prev.left = self.rotate_right(curr)

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
                            curr = prev.left
                        else:
                            prev.right = successor
                            curr = prev.right
                    else:
                        self.head = successor
                        curr = self.head

                elif curr.left or curr.right:
                    if curr.left:
                        if prev:
                            if key < prev.key:
                                prev.left = curr.left
                                curr = prev.left
                            else:
                                prev.right = curr.left
                                curr = prev.right
                        else:
                            self.head = curr.left
                            curr = self.head
                    elif curr.right:
                        if prev:
                            if key < prev.key:
                                prev.left = curr.right
                                curr = prev.left
                            else:
                                prev.right = curr.right
                                curr = prev.right
                        else:
                            self.head = curr.right
                            curr = self.head

                else:
                    if prev:
                        if key < prev.key:
                            prev.left = None
                            curr = prev.left
                        else:
                            prev.right = None
                            curr = prev.right
                    else:
                        self.head = None
                        curr = self.head

            elif key < curr.key and curr.left:
                self.delete(key, curr.left, curr)
            elif key > curr.key and curr.right:
                self.delete(key, curr.right, curr)

        if curr is not None:
            curr.balance = self.height(curr.left) - self.height(curr.right)

            # LL
            if curr.balance > 1 and curr.left.balance >= 0:
                if curr == self.head:
                    self.head = self.rotate_right(curr)
                else:
                    if curr.key > prev.key:
                        prev.right = self.rotate_right(curr)
                    else:
                        prev.left = self.rotate_right(curr)

            # RR
            elif curr.balance < -1 and curr.right.balance <= 0:
                if curr == self.head:
                    self.head = self.rotate_left(curr)
                else:
                    if curr.key > prev.key:
                        prev.right = self.rotate_left(curr)
                    else:
                        prev.left = self.rotate_left(curr)

            # RL
            elif curr.balance < -1 and curr.right.balance > 0:
                curr.right = self.rotate_right(curr.right)
                if curr == self.head:
                    self.head = self.rotate_left(curr)
                else:
                    if curr.key > prev.key:
                        prev.right = self.rotate_left(curr)
                    else:
                        prev.left = self.rotate_left(curr)

            # LR
            elif curr.balance > 1 and curr.left.balance < 0:
                curr.left = self.rotate_left(curr.left)

                if curr == self.head:
                    self.head = self.rotate_right(curr)
                else:
                    if curr.key > prev.key:
                        prev.right = self.rotate_right(curr)
                    else:
                        prev.left = self.rotate_right(curr)

    def rotate_right(self, curr):
        left_child = curr.left
        l_childs_right = left_child.right

        left_child.right = curr
        curr.left = l_childs_right

        curr.balance = self.height(curr.left) - self.height(curr.right)
        left_child.balance = self.height(left_child.left) - self.height(left_child.right)

        return left_child

    def rotate_left(self, curr):
        right_child = curr.right
        r_childs_left = right_child.left

        right_child.left = curr
        curr.right = r_childs_left

        curr.balance = self.height(curr.left) - self.height(curr.right)
        right_child.balance = self.height(right_child.left) - self.height(right_child.right)

        return right_child

    def height(self, curr):
        if curr is None:
            return 0
        else:
            left_height = self.height_help(curr.left)
            right_height = self.height_help(curr.right)

            if left_height > right_height:
                return left_height + 1
            else:
                return right_height + 1


def main():
    # utworzenie pustego drzewa samorównoważącego
    tree = AVL()

    # wstawienie kolejnych elementów
    tree.insert(50, "A")
    tree.insert(15, "B")
    tree.insert(62, "C")
    tree.insert(5, "D")
    tree.insert(2, "E")
    tree.insert(1, "F")
    tree.insert(11, "G")
    tree.insert(100, "H")
    tree.insert(7, "I")
    tree.insert(6, "J")
    tree.insert(55, "K")
    tree.insert(52, "L")
    tree.insert(51, "M")
    tree.insert(57, "N")
    tree.insert(8, "O")
    tree.insert(9, "P")
    tree.insert(10, "R")
    tree.insert(99, "S")
    tree.insert(12, "T")

    print("Struktura drzewa w formie 2D po wstawieniu 19 elementów:")
    tree.print_tree()

    print("Struktura drzewa od najmniejszego do największego klucza w formie klucz:wartość:")
    tree.print()

    print("Wartość dla klucza 10: ", tree.search(10))

    tree.delete(50)
    tree.delete(52)
    tree.delete(11)
    tree.delete(57)
    tree.delete(1)
    tree.delete(12)
    tree.insert(3, "AA")
    tree.insert(4, "BB")
    tree.delete(7)
    tree.delete(8)

    print("\nPo dodaniu i usunięciu kilku elementów:\n")
    print("Obecna struktura drzewa w formie 2D:")
    tree.print_tree()

    print("\nObecna struktura drzewa od najmniejszego do największego klucza w formie klucz:wartość:")
    tree.print()


if __name__ == "__main__":
    main()
