import numpy as np


class Vertex:
    def __init__(self, data, vertex_id):
        self.vertex_id = vertex_id
        self.data = data


class GraphMatrix:
    def __init__(self):
        self.vertex_to_index = {}
        self.adj_matrix = []

    def insertVertex(self, vertex_id, data=None):
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
        vertex = self.getVertex(vertex_id)
        neighbours = []
        for el in self.adj_list[vertex]:
            neighbours.append(el.vertex)
        return neighbours

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

    def getVertexByIdx(self, idx):
        for vertex in self.vertex_to_index.keys():
            if self.vertex_to_index[vertex] == idx:
                return vertex
        return None

    def neighbours_idx(self, index):
        neighbors = []
        for i in range(len(self.adj_matrix[index])):
            if self.adj_matrix[index][i] == 1:
                neighbors.append(i)
        return neighbors

    def deg(self, vertex_id):
        vertex = self.getVertex(vertex_id)
        return len(self.adj_matrix[vertex])

    def get_matrix(self):
        return np.array(self.adj_matrix)


def is_isomorphism(M, P, G):
    P_Mat = P.get_matrix()
    G_Mat = G.get_matrix()
    MG = np.dot(M, G_Mat)

    A = np.dot(M, MG.T)
    if A.shape == P_Mat.shape:
        for i in range(A.shape[0]):
            for j in range(A.shape[1]):
                if (A[i][j] != P_Mat[i][j]):
                    return False
        return True



def prune(M, P, G):
    M_changed = True

    while M_changed:
        M_changed = False

        for i in range(len(M)):
            for j in range(len(M[i])):
                if M[i][j] == 1:
                    neighbours_vi = P.neighbours_idx(i)
                    neighbours_vj = G.neighbours_idx(j)

                    for x in neighbours_vi:
                        no_neighb = True
                        for y in neighbours_vj:
                            if M[x][y] == 1:
                                no_neighb = False
                        if no_neighb:
                            M[i][j] = 0
                            M_changed = True


def ullman_v1_0(used_cols, curr_row, G, P, M):
    if curr_row == M.shape[0]:
        if is_isomorphism(M, P, G):
            print(M)
            return 1

    M_ = M.copy()
    # prune(M_, P, G)

    for c in range(M.shape[1]):
        if c not in used_cols:
            M_[curr_row][c] = 1
        else:
            M_[curr_row][c] = 0

            # ustawianie kolumny c na 1 i innych na 0
            # for col in range(M.shape[1]):
            #     if col == c:
            #         M_[curr_row][col] = 1
            #     else:
            #         M_[curr_row][col] = 0

            # oznaczenie kolumny c jako użytej
        used_cols.append(c)

            # wywołanie rekurencyjne ullmana
            # output, encoding = ullman(used_cols, curr_row + 1, G, P, M_)
        ullman_v1_0(used_cols, curr_row + 1, G, P, M_)

        # odznaczenie c z użytych
        for i in range(len(used_cols)):
            if used_cols[i] == c:
                used_cols.pop(i)
        #
            # return output



def create_graph(graf):
    G = GraphMatrix()

    for edge in graf:
        G.insertVertex(edge[0])
        G.insertVertex(edge[1])

    for edge in graf:
        G.insertEdge(edge[0], edge[1])
        G.insertEdge(edge[1], edge[0])

    return G



graph_G = [ ('A','B',1), ('B','F',1), ('B','C',1), ('C','D',1), ('C','E',1), ('D','E',1)]
graph_P = [ ('A','B',1), ('B','C',1), ('A','C',1)]


G = create_graph(graph_G)
P = create_graph(graph_P)


M = np.array(P.order() * [G.order() * [0]])
for i in range(M.shape[0]):
    M[i, i] = 1
print(M)
output = ullman_v1_0([], 0, G, P, M)

print(output)
