import polska


class Vertex:
    def __init__(self, data, vertex_id):
        self.vertex_id = vertex_id
        self.data = data


class ForwardStar:
    def __init__(self):
        self.vertex_to_index = {}
        self.vertices_list = []
        self.edges_list = []

    def insertVertex(self, data, vertex_id):
        if self.getVertex(vertex_id) is None:
            vertex = Vertex(data, vertex_id)
            self.vertices_list.append([])
            self.vertex_to_index[vertex] = len(self.vertices_list) - 1

    def insertEdge(self, vertex1_id, vertex2_id):
        vertex1_index = self.getVertexIdx(vertex1_id)
        vertex2_index = self.getVertexIdx(vertex2_id)

        if vertex1_index is not None and vertex2_index is not None:
            self.edges_list.append([vertex1_index, vertex2_index])
            index = len(self.edges_list) - 1
            while index > 0 and self.edges_list[index - 1][0] > self.edges_list[index][0]:
                for edge in self.vertices_list[self.edges_list[index - 1][0]]:
                    if edge == index - 1:
                        edge += 1
                self.edges_list[index], self.edges_list[index - 1] = self.edges_list[index - 1], self.edges_list[index]
                index -= 1

            if index not in self.vertices_list[vertex1_index]:
                self.vertices_list[vertex1_index].append(index)

    def deleteVertex(self, vertex_id):
        index = self.getVertexIdx(vertex_id)
        if index is not None:
            i = 0
            while i < len(self.edges_list):
                vertex1 = self.edges_list[i][0]
                vertex2 = self.edges_list[i][1]
                if vertex1 > index:
                    self.edges_list[i][0] -= 1
                if vertex2 > index:
                    self.edges_list[i][1] -= 1

                if vertex1 == index or vertex2 == index:
                    if vertex2 == index:
                        j = 0
                        while j < len(self.vertices_list[vertex1]):
                            if self.vertices_list[vertex1][j] == i:
                                self.vertices_list[vertex1].pop(j)
                            else:
                                j += 1
                    self.edges_list.pop(i)
                    for vertex in self.vertices_list:
                        for j in range(len(vertex)):
                            if vertex[j] > i:
                                vertex[j] -= 1
                else:
                    i += 1

            self.vertices_list.pop(index)
            to_pop = None
            for vertex in self.vertex_to_index.keys():
                index_ = self.vertex_to_index[vertex]
                if index_ > index:
                    self.vertex_to_index[vertex] -= 1
                if index_ == index:
                    to_pop = vertex
            if to_pop:
                self.vertex_to_index.pop(to_pop)

    def deleteEdge(self, vertex1_id, vertex2_id):
        vertex1_index = self.getVertexIdx(vertex1_id)
        vertex2_index = self.getVertexIdx(vertex2_id)

        if vertex1_index is not None and vertex2_index is not None:
            i = 0
            while i < len(self.edges_list):
                if self.edges_list[i][0] == vertex1_index and self.edges_list[i][1] == vertex2_index:
                    self.edges_list.pop(i)

                    for vertex in self.vertices_list:
                        j = 0
                        while j < (len(vertex)):
                            if vertex[j] > i:
                                vertex[j] -= 1
                            if vertex[j] == i:
                                vertex.pop(j)
                            else:
                                j += 1
                else:
                    i += 1

    def getVertexIdx(self, key):
        vertex = self.getVertex(key)
        if vertex and vertex in self.vertex_to_index.keys():
            index = self.vertex_to_index[vertex]
            return index
        return None

    def getVertex(self, key):
        for vertex in self.vertex_to_index.keys():
            if vertex.vertex_id == key:
                return vertex
        return None

    def getVertexByIndex(self, index):
        for vertex in self.vertex_to_index.keys():
            if self.vertex_to_index[vertex] == index:
                return vertex
        return None

    def neighbours(self, vertex_id):
        index = self.getVertexIdx(vertex_id)
        neighb = []
        for edge_idx in self.vertices_list[index]:
            neighb.append(self.getVertexByIndex(self.edges_list[edge_idx][1]).vertex_id)
        return neighb

    def order(self):
        return len(self.vertices_list)

    def size(self):
        return len(self.edges_list)

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


def main():
    #utworzenie grafu
    graph = ForwardStar()

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
