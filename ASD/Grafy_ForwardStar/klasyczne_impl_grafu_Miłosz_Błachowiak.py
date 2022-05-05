import polska


class Vertex:
    def __init__(self, data, vertex_id):
        self.vertex_id = vertex_id
        self.data = data


class GraphMatrix:
    def __init__(self):
        self.vertex_to_index = {}
        self.adj_matrix = []

    def insertVertex(self, data, vertex_id):
        size = self.order()
        index = self.getVertexIdx(vertex_id)

        if index is None:
            self.adj_matrix.append((size + 1) * [0])
            for i in range(size):
                self.adj_matrix[i].append(0)
            vertex = Vertex(data, vertex_id)
            self.vertex_to_index[vertex] = size

    def insertEdge(self, vertex1_id, vertex2_id):
        vert1_index = self.getVertexIdx(vertex1_id)
        vert2_index = self.getVertexIdx(vertex2_id)

        if vertex1_id and vertex2_id:
            self.adj_matrix[vert1_index][vert2_index] = 1

    def deleteVertex(self, vertex_id):
        index = self.getVertexIdx(vertex_id)
        vertex = self.getVertex(vertex_id)

        for row in self.adj_matrix:
            row.pop(index)

        self.adj_matrix.pop(index)
        self.vertex_to_index.pop(vertex)
        for vertex in self.vertex_to_index.keys():
            if self.vertex_to_index[vertex] > index:
                self.vertex_to_index[vertex] -= 1

    def deleteEdge(self, vertex1_id, vertex2_id):
        vert1_index = self.getVertexIdx(vertex1_id)
        vert2_index = self.getVertexIdx(vertex2_id)

        if vertex1_id and vertex2_id:
            self.adj_matrix[vert1_index][vert2_index] = 0

    def getVertexIdx(self, key):
        vertex = self.getVertex(key)
        if vertex in self.vertex_to_index.keys():
            index = self.vertex_to_index[vertex]
            return index
        return None

    def getVertex(self, vertex_id):
        for vertex in self.vertex_to_index.keys():
            if vertex.vertex_id == vertex_id:
                return vertex
        return None

    def neighbours(self, vertex_id):
        index = self.getVertexIdx(vertex_id)

        neighbors = []
        for i in range(len(self.adj_matrix[index])):
            if self.adj_matrix[index][i] == 1:
                for vertex in self.vertex_to_index.keys():
                    if self.vertex_to_index[vertex] == i:
                        neighbors.append(vertex.vertex_id)
        return neighbors

    def order(self):
        return len(self.adj_matrix)

    def size(self):
        size = 0
        for row in self.adj_matrix:
            for el in row:
                if el == 1:
                    size += 1
        return size

    def edges(self):
        edges = []
        for vertex in self.vertex_to_index.keys():
            vert_neighb = self.neighbours(vertex.vertex_id)
            for neighb in vert_neighb:
                edges.append((vertex.vertex_id, neighb))
        return edges

    def vertices(self):
        vert = []
        for el in self.vertex_to_index.keys():
            vert.append((el.vertex_id, el.vertex_id))
        return vert


class GraphList:
    def __init__(self):
        self.adj_list = {}

    def insertVertex(self, data, vertex_id):
        if self.getVertex(vertex_id) is None:
            vertex = Vertex(data, vertex_id)
            self.adj_list[vertex] = []

    def insertEdge(self, vertex1_id, vertex2_id):
        vertex1 = self.getVertex(vertex1_id)
        vertex2 = self.getVertex(vertex2_id)
        if vertex1 and vertex2:
            self.adj_list[vertex1].append(vertex2)

    def deleteVertex(self, vertex_id):
        vertex = self.getVertex(vertex_id)
        if vertex in self.adj_list:
            self.adj_list.pop(vertex)

        for el in self.adj_list.keys():
            i = 0
            while i < len(self.adj_list[el]):
                if self.adj_list[el][i] == vertex:
                    self.adj_list[el].pop(i)
                i += 1

    def deleteEdge(self, vertex1_id, vertex2_id):
        vertex1 = self.getVertex(vertex1_id)
        vertex2 = self.getVertex(vertex2_id)

        if vertex1 and vertex2:
            i = 0
            while i < len(self.adj_list[vertex1]):
                if self.adj_list[vertex1][i] == vertex2:
                    self.adj_list[vertex1].pop(i)
                i += 1

    def getVertex(self, key):
        for vertex in self.adj_list.keys():
            if vertex.vertex_id == key:
                return vertex
        return None

    def neighbours(self, vertex_id):
        vertex = self.getVertex(vertex_id)
        return self.adj_list[vertex]

    def order(self):
        return len(self.adj_list)

    def size(self):
        nr_of_edges = 0
        for el in self.adj_list.keys():
            nr_of_edges += len(self.adj_list[el])
        return nr_of_edges

    def edges(self):
        edges = []
        for el in self.adj_list.keys():
            for neigh in self.adj_list[el]:
                edges.append((el.vertex_id, neigh.vertex_id))
        return edges

    def vertices(self):
        vert = []
        for el in self.adj_list.keys():
            vert.append((el.vertex_id, el.vertex_id))
        return vert


def main():
    # utworzenie grafu
    graph = GraphMatrix()
    # graph = GraphList()

    # dodanie wierzchołków
    for el in polska.polska:
        data = (el[0], el[1])
        vertex_id = el[2]
        graph.insertVertex(data, vertex_id)

    # wstawienie krawędzi
    for el in polska.graf:
        graph.insertEdge(el[0], el[1])

    # usunięcie wierzchołka dla województwa małopolskiego
    graph.deleteVertex('K')

    # usunięcie połączeń między województwami łódzkim i mazowieckim
    graph.deleteEdge('W', 'E')
    graph.deleteEdge('E', 'W')

    # wyświetlenie stworzonyego grafu
    edges = graph.edges()
    vertices = graph.vertices()
    polska.draw_map(edges, vertices)


if __name__ == "__main__":
    main()
