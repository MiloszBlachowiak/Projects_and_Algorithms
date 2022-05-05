import graf_mst
import sys


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


class Sort:
    def __init__(self):
        self.tab = []

    def insert(self, val, data):
        element = Element(val, data)
        self.tab.append(element)

    def sort(self):
        for i in range(len(self.tab)):
            m = i
            for j in range(i, len(self.tab)):
                if self.tab[j] < self.tab[m]:
                    m = j
            self.tab[i], self.tab[m] = self.tab[m], self.tab[i]

    def get_tab(self):
        sorted = []
        for el in self.tab:
            sorted.append((el.value[0], el.value[1], el.priority))
        return sorted


class Vertex:
    def __init__(self, vertex_id, data=None, colour=None):
        self.vertex_id = vertex_id
        self.data = data
        self.colour = colour


class GraphList:
    def __init__(self):
        self.adj_list = {}

        self.intree = None
        self.distance = None
        self.parent = None

    def insertVertex(self, vertex_id, data=None, colour=None):
        if self.getVertex(vertex_id) is None:
            vertex = Vertex(vertex_id, data, colour)
            self.adj_list[vertex] = []

    def insertEdge(self, vertex1_id, vertex2_id, weight=1):
        vertex1 = self.getVertex(vertex1_id)
        vertex2 = self.getVertex(vertex2_id)
        if vertex1 and vertex2:
            if (vertex2, weight) not in self.adj_list[vertex1]:
                self.adj_list[vertex1].append((vertex2, weight))
                self.adj_list[vertex2].append((vertex1, weight))

    def deleteVertex(self, vertex_id):
        vertex = self.getVertex(vertex_id)
        if vertex in self.adj_list:
            self.adj_list.pop(vertex)

        for el in self.adj_list.keys():
            i = 0
            while i < len(self.adj_list[el]):
                if self.adj_list[el][i][0] == vertex:
                    self.adj_list[el].pop(i)
                i += 1

    def deleteEdge(self, vertex1_id, vertex2_id):
        vertex1 = self.getVertex(vertex1_id)
        vertex2 = self.getVertex(vertex2_id)

        if vertex1 and vertex2:
            i = 0
            while i < len(self.adj_list[vertex1]):
                if self.adj_list[vertex1][i][0] == vertex2:
                    self.adj_list[vertex1].pop(i)
                i += 1
            j = 0
            while j < len(self.adj_list[vertex2]):
                if self.adj_list[vertex2][j][0] == vertex1:
                    self.adj_list[vertex2].pop(j)
                j += 1

    def getVertex(self, key):
        for vertex in self.adj_list.keys():
            if vertex.vertex_id == key:
                return vertex
        return None

    def neighbours(self, vertex_id):
        vertex = self.getVertex(vertex_id)
        return self.adj_list[vertex]

    def neighbours_keys(self, vertex_id):
        vertex = self.getVertex(vertex_id)
        neighb = []
        for n in self.adj_list[vertex]:
            neighb.append(n[0].vertex_id)
        return neighb

    def order(self):
        return len(self.adj_list)

    def size(self):
        nr_of_edges = 0
        for el in self.adj_list.keys():
            nr_of_edges += len(self.adj_list[el])
        return nr_of_edges/2

    def edges(self):
        edges = []
        for el in self.adj_list.keys():
            for neigh in self.adj_list[el]:
                if (neigh[0].vertex_id, el.vertex_id, neigh[1]) not in edges:
                    edges.append((el.vertex_id, neigh[0].vertex_id, neigh[1]))
        return edges

    def vertices(self):
        vert = []
        for el in self.adj_list.keys():
            vert.append(el.vertex_id)
        return vert

    def set_colour(self, vertex_id, colour):
        vertex = self.getVertex(vertex_id)
        if vertex:
            vertex.colour = colour

    def get_colour(self, vertex_id):
        vertex = self.getVertex(vertex_id)
        if vertex:
            return vertex.colour

    def vertex_edges(self, vertex_id):
        vertex = self.getVertex(vertex_id)
        edges = []
        for neigh in self.adj_list[vertex]:
            edges.append((vertex_id, neigh[0].vertex_id, neigh[1]))
        return edges

    def print_adj_list(self):
        adj_list = {}
        for vertex in self.adj_list.keys():
            adj_list[vertex.vertex_id] = []
            for neighb in self.adj_list[vertex]:
                adj_list[vertex.vertex_id].append(neighb[0].vertex_id)
        print(adj_list)

    def getVertexIdx(self, vertex_id):
        vertices = self.vertices()
        for i in range(len(vertices)):
            if vertices[i] == vertex_id:
                return i
        return None

    def getVertexByIdx(self, idx):
        return list(self.adj_list.keys())[idx]

    def Kruskal_MST(self, G):
        edges = G.edges()

        lst_of_edges = Sort()
        for el in edges:
            lst_of_edges.insert((el[0], el[1]), el[2])

        lst_of_edges.sort()
        sorted_edges = lst_of_edges.get_tab()

        union = UnionFind(G.order())

        for edge in sorted_edges:
            if not union.same_component(ord(edge[0]) - 64, ord(edge[1]) - 64):
                self.insertEdge(edge[0], edge[1], edge[2])
                union.union_sets(ord(edge[0]) - 64, ord(edge[1]) - 64)


class UnionFind:
    def __init__(self, size):
        self.p = [i + 1 for i in range(size)]
        self.size = [1 for i in range(size)]
        self.n = size

    def parent(self, v):
        return self.p[v - 1]

    def find(self, v):
        if self.parent(v) == v:
            return v - 1
        return self.find(self.parent(v))

    def union_sets(self, s1, s2):
        root1 = self.find(s1)
        root2 = self.find(s2)

        if root1 != root2:
            if self.size[root1] == self.size[root2]:
                self.p[root2] = root1 + 1
                self.size[root1] += self.size[root2]

            elif self.size[root1] > self.size[root2]:
                self.p[root2] = root1 + 1
                self.size[root1] += self.size[root2]

            elif self.size[root1] < self.size[root2]:
                self.p[root1] = root2 + 1
                self.size[root2] += self.size[root1]

    def same_component(self, s1, s2):
        root1 = self.find(s1)
        root2 = self.find(s2)
        return root1 == root2


def main():

    print("Testy struktury Union-Find:")

    # tworzymy zbiór pięciu wierzchołków
    unia = UnionFind(5)

    # łączymy 1-2, 4-5
    unia.union_sets(1, 2)
    unia.union_sets(4, 5)

    #sprawdzamy czy 1-2, 2-3, 4-5 są połączone
    print("\nPo połączeniu 1-2 i 4-5:\n")
    print("1-2 połączone?: ", unia.same_component(1, 2))
    print("2-3 połączone?: ", unia.same_component(2, 3))
    print("4-5 połączone?: ", unia.same_component(4, 5))

    # łączymy 3-1
    unia.union_sets(3, 1)

    print("\nPo połączeniu 3-1:\n")

    print("1-2 połączone?: ", unia.same_component(1, 2))
    print("2-3 połączone?: ", unia.same_component(2, 3))
    print("4-5 połączone?: ", unia.same_component(4, 5))


    print("\nTesty algorytmu Kruskala:")

    # tworzymy graf testowy
    G = GraphList()

    # dodajemy wierzchołki i krawędzie
    for edge in graf_mst.graf:
        G.insertVertex(edge[0])
        G.insertVertex(edge[1])
        G.insertEdge(edge[0], edge[1], edge[2])

    # tworzymy strukturę pod MST
    Kruskal_MST = GraphList()

    # dodajemy wierzchołki
    for edge in graf_mst.graf:
        Kruskal_MST.insertVertex(edge[0])
        Kruskal_MST.insertVertex(edge[1])

    # wykonujemy algorytm Kruskala
    Kruskal_MST.Kruskal_MST(G)
    print("Krawędzie w MST:\n", Kruskal_MST.edges())


if __name__ == "__main__":
    main()
