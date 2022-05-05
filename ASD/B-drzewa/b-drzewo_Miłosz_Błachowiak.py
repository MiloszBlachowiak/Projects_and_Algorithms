class Node:
    def __init__(self, max):
        self.keys = [None for i in range(max-1)]
        self.children = [None for i in range(max)]
        self.size = 0


class BTree:
    def __init__(self, max_children):
        self.root = None
        self.max = max_children

    def insert(self, key, curr=None):
        if curr is None:
            curr = self.root
            if curr is None:
                self.root = Node(self.max)
                self.root.keys[0] = key
                self.root.size += 1
            else:
                divided = self.insert(key, curr)
                if divided:
                    middle_key = divided[0]
                    new_node = divided[1]
                    new_root = Node(self.max)
                    new_root.keys[0] = middle_key
                    new_root.size += 1
                    old_root = self.root
                    self.root = new_root
                    self.root.children[0] = old_root
                    self.root.children[1] = new_node
        else:
            index = 0
            while index < curr.size and key > curr.keys[index]:
                index += 1

            if all(el is None for el in curr.children):
                return self.add_to_node(key, curr)
            else:
                divided = self.insert(key, curr.children[index])

            if divided:
                middle_key = divided[0]
                new_node = divided[1]
                return self.add_to_node(middle_key, curr, new_node)

    def add_to_node(self, key, node, new_child=None):
        if node.size < self.max - 1:
            node.keys[node.size] = key
            node.size += 1
            index = node.size - 1
            while index > 0 and node.keys[index - 1] > node.keys[index]:
                node.keys[index - 1], node.keys[index] = node.keys[index], node.keys[index - 1]
                index -= 1

            if new_child:
                node.children[node.size] = new_child
                index = node.size
                while index > 0 and node.children[index - 1].keys[0] > node.children[index].keys[0]:
                    node.children[index - 1], node.children[index] = \
                        node.children[index], node.children[index - 1]
                    index -= 1
            return None

        k = node.keys[:]
        k.append(key)
        index = node.size
        while index > 0 and k[index - 1] > k[index]:
            k[index - 1], k[index] = k[index], k[index - 1]
            index -= 1
        middle_idx = len(k)//2
        middle_key = k[middle_idx]

        new_node = Node(self.max)
        i = middle_idx + 1
        while i < len(k):
            new_node.keys[i - middle_idx - 1] = k[i]
            new_node.size += 1
            i += 1

        if new_child:
            old_node_children = node.children[:]
            old_node_children.append(new_child)
            index = self.max
            while index > 0 and old_node_children[index - 1].keys[0] > old_node_children[index].keys[0]:
                old_node_children[index - 1], old_node_children[index] = \
                    old_node_children[index], old_node_children[index - 1]
                index -= 1
            for i in range(new_node.size + 1):
                new_node.children[i] = old_node_children[i + middle_idx + 1]
                node.children[i] = old_node_children[i]

        for i in range(node.size):
            if node.keys[i] >= middle_key:
                node.keys[i] = None
                node.children[i + 1] = None
                node.size -= 1
        if key < middle_key:
            node.keys[node.size] = key
            node.size += 1

        return middle_key, new_node

    def print_tree(self):
        print("==============")
        self._print_tree(self.root, 0)
        print("==============")

    def _print_tree(self, node, lvl):
        if node is not None:
            for i in range(node.size + 1):
                self._print_tree(node.children[i], lvl + 1)
                if i < node.size:
                    print(lvl * '  ', node.keys[i])


def main():
    # utworzenie pustego drzewa
    btree = BTree(3)

    # wstawienie kolejnych elementów
    keys = [5, 17, 2, 14, 7, 4, 12, 16, 8, 11, 9, 6, 13, 0, 3, 18, 15, 10, 19]

    # dodajemy elementy z listy
    for el in keys:
        btree.insert(el)

    print("Stan drzewa po dodaniu 20 elementów w losowej kolejności w pętli:")
    btree.print_tree()

    # tworzymy nowe drzewo i dodajemy po kolei liczby od 0 do 19
    btree2 = BTree(3)
    for i in range(20):
        btree2.insert(i)

    print("\nStan drzewa po dodaniu kolejno 20 elementów w pętli (od 0 do 19):")
    btree2.print_tree()

    #dodajemy następne 180 elementów
    for i in range(20, 200):
        btree2.insert(i)

    print("\nStan drzewa po dodaniu kolejnych 180 elementów w pętli (od 20 do 199):")
    btree2.print_tree()

    # utworzenie drzewa o maksymalnej liczbie potomków równej 5
    btree3 = BTree(5)

    # dodajemy kolejno 200 elementów
    for i in range(200):
        btree3.insert(i)

    print("\nStan drzewa o maksymalnej liczbie potomków zwiększonej do 5 po dodaniu kolejnych 200 elementów w pętli:")
    btree3.print_tree()


if __name__ == "__main__":
    main()

