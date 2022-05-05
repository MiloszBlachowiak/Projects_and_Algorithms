class Vertex:
    def __init__(self, vertex_id, data=None, colour=None):
        self.vertex_id = vertex_id
        self.data = data
        self.colour = colour


class Edge:
    def __init__(self, vertex, capacity, isResidual):
        self.vertex = vertex
        self.capacity = capacity
        self.flow = 0
        self.residual = capacity
        self.isResidual = isResidual



class GraphList:
    def __init__(self):
        self.adj_list = {}

    def insertVertex(self, vertex_id, data=None, colour=None):
        if self.getVertex(vertex_id) is None:
            vertex = Vertex(vertex_id, data, colour)
            self.adj_list[vertex] = []

    def insertEdge(self, vertex1_id, vertex2_id, capacity, isResidual):
        vertex1 = self.getVertex(vertex1_id)
        vertex2 = self.getVertex(vertex2_id)
        if vertex1 and vertex2:
            edge = Edge(vertex2, capacity, isResidual)
            self.adj_list[vertex1].append(edge)

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
                if self.adj_list[vertex1][i].vertex == vertex2:
                    self.adj_list[vertex1].pop(i)
                i += 1

    def getVertex(self, key):
        for vertex in self.adj_list.keys():
            if vertex.vertex_id == key:
                return vertex
        return None

    def neighbours(self, vertex_id):
        vertex = self.getVertex(vertex_id)
        neighbours = []
        for el in self.adj_list[vertex]:
            neighbours.append(el.vertex)
        return neighbours

    def neighbours_keys(self, vertex_id):
        vertex = self.getVertex(vertex_id)
        neighb = []
        for el in self.adj_list[vertex]:
            neighb.append(el.vertex.vertex_id)
        return neighb

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
                edges.append((el.vertex_id, neigh.vertex.vertex_id, neigh.capacity, neigh.flow, neigh.residual))
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

        for edge in self.adj_list[vertex]:
            edges.append(edge)

        for ver in self.adj_list.keys():
            if ver != vertex:
                for edge in self.adj_list[ver]:
                    if edge.vertex == vertex:
                        edges.append(edge)
        return edges

    def print_adj_list(self):
        adj_list = {}
        for vertex in self.adj_list.keys():
            adj_list[vertex.vertex_id] = []
            for neighb in self.adj_list[vertex]:
                adj_list[vertex.vertex_id].append(neighb.vertex.vertex_id)
        print(adj_list)

    def getVertexIdx(self, vertex_id):
        vertices = self.vertices()
        for i in range(len(vertices)):
            if vertices[i] == vertex_id:
                return i
        return None

    def getVertexByIdx(self, idx):
        return list(self.adj_list.keys())[idx]

    def BFS(self, root):
        root_vertex = self.getVertex(root)
        root_vertex_idx = self.getVertexIdx(root)
        visited = [0 for vertex in self.adj_list.keys()]
        parent = [None for vertex in self.adj_list.keys()]
        queue = []

        visited[root_vertex_idx] = 1
        queue.append(root_vertex)

        while queue:
            element = queue.pop(0)
            neighbours = self.neighbours(element.vertex_id)

            for neighb in neighbours:
                neighb_idx = self.getVertexIdx(neighb.vertex_id)
                e = None
                for edge in self.adj_list[element]:
                    if edge.vertex == neighb and edge.residual > 0:
                        e = edge

                if visited[neighb_idx] == 0 and e and e.residual > 0:
                    queue.append(neighb)
                    visited[neighb_idx] = 1
                    parent[neighb_idx] = element.vertex_id

        return parent

    def calc_min_res(self, G, root, end, parent):
        curr_vertex = G.getVertex(end)
        root_vertex = G.getVertex(root)
        min_res_capacity = float('inf')

        curr_idx = G.getVertexIdx(curr_vertex.vertex_id)
        if curr_idx and parent[curr_idx] is None:
            return 0

        while curr_vertex != root_vertex:
            vertex_edges = G.vertex_edges(curr_vertex.vertex_id)
            chosen_edge = None
            chosen_edge_capacity = float('inf')
            for edge in vertex_edges:
                if edge.vertex == curr_vertex and edge in G.adj_list[G.getVertex(parent[curr_idx])]:
                    if edge.residual < chosen_edge_capacity:
                        if chosen_edge is not None:
                            if chosen_edge.flow < edge.flow:
                                chosen_edge = edge
                                chosen_edge_capacity = edge.residual
                        else:
                            chosen_edge = edge
                            chosen_edge_capacity = edge.residual

            if chosen_edge.residual < min_res_capacity:
                min_res_capacity = chosen_edge.residual

            curr_vertex = G.getVertex(parent[curr_idx])
            curr_idx = G.getVertexIdx(curr_vertex.vertex_id)
        return min_res_capacity

    def augumentation(self, G, root, end, parent, min_capacity):
        curr_vertex = G.getVertex(end)
        root_vertex = G.getVertex(root)

        curr_idx = G.getVertexIdx(curr_vertex.vertex_id)
        if curr_idx and parent[curr_idx] is None:
            return 0

        while curr_vertex != root_vertex:
            vertex_edges = G.vertex_edges(curr_vertex.vertex_id)
            chosen_edge = None
            chosen_edge_capacity = float('inf')
            for edge in vertex_edges:
                if edge.vertex == curr_vertex and edge in G.adj_list[G.getVertex(parent[curr_idx])]:
                    if edge.residual < chosen_edge_capacity:
                        if chosen_edge is not None:
                            if chosen_edge.flow < edge.flow:
                                chosen_edge = edge
                                chosen_edge_capacity = edge.residual
                        else:
                            chosen_edge = edge
                            chosen_edge_capacity = edge.residual

            chosen_edge.flow += min_capacity
            chosen_edge.residual -= min_capacity

            chosen_residual = None
            for edge in vertex_edges:
                if edge.vertex.vertex_id == parent[curr_idx]:
                    if edge.isResidual:
                        chosen_residual = edge

            chosen_residual.residual += min_capacity

            curr_vertex = G.getVertex(parent[curr_idx])
            curr_idx = G.getVertexIdx(curr_vertex.vertex_id)

    def get_max_flow(self, G, end):
        end_vertex = G.getVertex(end)
        flow = 0

        vertex_edges = G.vertex_edges(end_vertex.vertex_id)

        for edge in vertex_edges:
            if edge.vertex == end_vertex:
                flow += edge.flow

        return flow


def get_path(G, parent, end):
    curr_vertex = G.getVertex(end)
    path = []

    curr_idx = G.getVertexIdx(curr_vertex.vertex_id)

    while curr_vertex is not None:
        path.insert(0, curr_vertex.vertex_id)
        curr_vertex = G.getVertex(parent[curr_idx])
        if curr_vertex is not None:
            curr_idx = G.getVertexIdx(curr_vertex.vertex_id)

    return path


def do_EdmondsKarp(G, start, end):
    parent = G.BFS(start)

    min_cap = G.calc_min_res(G, start, end, parent)

    while min_cap > 0:
        G.augumentation(G, start, end, parent, min_cap)
        parent = G.BFS(start)
        min_cap = G.calc_min_res(G, start, end, parent)

    flow = G.get_max_flow(G, end)
    print("Maksymalny przepływ: ", flow)


def create_graph(graf):
    G = GraphList()

    for edge in graf:
        G.insertVertex(edge[0])
        G.insertVertex(edge[1])

    for edge in graf:
        G.insertEdge(edge[0], edge[1], edge[2], isResidual=False)
        G.insertEdge(edge[1], edge[0], 0, isResidual=True)

    return G


def main():
    graf_0 = [('s', 'u', 2), ('u', 't', 1), ('u', 'v', 3), ('s', 'v', 1), ('v', 't', 2)]

    graf_1 = [('s', 'a', 16), ('s', 'c', 13), ('a', 'c', 10), ('c', 'a', 4), ('a', 'b', 12), ('b', 'c', 9),
              ('b', 't', 20), ('c', 'd', 14), ('d', 'b', 7), ('d', 't', 4)]

    graf_2 = [('s', 'a', 3), ('s', 'c', 3), ('a', 'b', 4), ('b', 's', 3), ('b', 'c', 1), ('b', 'd', 2), ('c', 'e', 6),
              ('c', 'd', 2), ('d', 't', 1), ('e', 't', 9)]

    graf_3 = [('s', 'a', 8), ('s', 'd', 3), ('a', 'b', 9), ('b', 'd', 7), ('b', 't', 2), ('c', 't', 5), ('d', 'b', 7),
              ('d', 'c', 4)]


    print("Obliczanie maksymalnego przepływu dla przypadków testowych z konspektu:")
    print("\nGraf 0:")
    graph0 = create_graph(graf_0)
    do_EdmondsKarp(graph0, 's', 't')

    print("\nGraf 1:")
    graph1 = create_graph(graf_1)
    do_EdmondsKarp(graph1, 's', 't')

    print("\nGraf 2:")
    graph2 = create_graph(graf_2)
    do_EdmondsKarp(graph2, 's', 't')

    print("\nGraf 3:")
    graph3 = create_graph(graf_3)
    do_EdmondsKarp(graph3, 's', 't')


if __name__ == "__main__":
    main()
