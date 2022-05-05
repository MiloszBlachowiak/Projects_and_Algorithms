import graf_mst
import sys
MAX_INT = sys.maxsize


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

    def init_MST(self):
        n = len(self.adj_list)
        self.intree = n * [0]
        self.distance = n * [MAX_INT]
        self.parent = n * [-1]

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

    def Prim_MST(self, G):
        curr_vertex = self.getVertex(list(G.adj_list.keys())[0].vertex_id)
        v = self.getVertexIdx(curr_vertex.vertex_id)

        total_dist = 0

        while v is not None and self.intree[v] == 0:
            self.intree[v] = 1
            for neighb in G.adj_list[G.getVertex(curr_vertex.vertex_id)]:
                neighb_idx = self.getVertexIdx(neighb[0].vertex_id)
                if neighb[1] < self.distance[neighb_idx] and self.intree[neighb_idx] == 0:
                    self.distance[neighb_idx] = neighb[1]
                    self.parent[neighb_idx] = v

            # szukamy kolejnego wierzchołka
            next_vertex = None
            for vertex in self.adj_list.keys():
                if self.intree[self.getVertexIdx(vertex.vertex_id)] == 0:
                    if next_vertex is None:
                        next_vertex = vertex
                    else:
                        if self.distance[self.getVertexIdx(vertex.vertex_id)] < self.distance[self.getVertexIdx(next_vertex.vertex_id)]:
                            next_vertex = vertex
            if next_vertex:
                v = self.getVertexIdx(next_vertex.vertex_id)
                self.insertEdge(self.getVertexByIdx(self.parent[v]).vertex_id, next_vertex.vertex_id, self.distance[v])
                curr_vertex = next_vertex
                total_dist += self.distance[v]
            else:
                v = None
        return total_dist


def main():
    print("Testy przed implementacją algorytmu Prima:")
    graph = GraphList()

    for edge in graf_mst.graf:
        graph.insertVertex(edge[0])
        graph.insertVertex(edge[1])
        graph.insertEdge(edge[0], edge[1], edge[2])

    print("Sąsiedzi A: ", graph.neighbours_keys('A'))
    print("\nKrawędzie z wierzchołka B:")
    print(graph.vertex_edges('B'))

    graph.deleteVertex('G')

    graph.deleteEdge('E', 'F')

    print("\nGraf w postaci listy:")
    graph.print_adj_list()



    print("\n\nTest algorytmu Prima: ")

    G = GraphList()

    for edge in graf_mst.graf:
        G.insertVertex(edge[0])
        G.insertVertex(edge[1])
        G.insertEdge(edge[0], edge[1], edge[2])

    MST = GraphList()

    for edge in graf_mst.graf:
        MST.insertVertex(edge[0])
        MST.insertVertex(edge[1])

    MST.init_MST()
    total_dist = MST.Prim_MST(G)
    print("\nSuma krawędzi tworzących drzewo: ", total_dist)
    print("\nKrawędzie w MST:")
    print(MST.edges())


if __name__ == "__main__":
    main()
