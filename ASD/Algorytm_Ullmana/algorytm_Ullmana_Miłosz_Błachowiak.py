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
        vertex_idx = self.getVertexIdx(vertex_id)
        neighbours = []
        for i in range(len(self.adj_matrix[vertex_idx])):
            if self.adj_matrix[vertex_idx][i] == 1:
                neighbours.append(self.getVertexByIdx(i))
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
            vert.append(el.vertex_id)
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
        neighbours = self.neighbours(vertex_id)
        return len(neighbours)

    def get_matrix(self):
        return np.array(self.adj_matrix)


def matrix_equal(A, B):
    if A.shape == B.shape:
        for i in range(A.shape[0]):
            for j in range(A.shape[1]):
                if A[i][j] != B[i][j]:
                    return False
    return True

def is_isomorphism(M, P, G):

    P_Mat = P.get_matrix()
    G_Mat = G.get_matrix()

    A = M @ (M @ G_Mat).T
    return matrix_equal(A, P_Mat)



def M0(col, row, G, P):
    g = G.getVertexByIdx(col)
    p = P.getVertexByIdx(row)

    deg_g = G.deg(g.vertex_id)
    deg_p = P.deg(p.vertex_id)

    return deg_g >= deg_p


def prune(M, P, G, row):
    MP = M.copy()

    for i in range(len(MP)):
        for j in range(len(MP[i])):
            if MP[i, j] == 1:
                neighbours_vi = P.neighbours_idx(i)
                neighbours_vj = G.neighbours_idx(j)

                for x in neighbours_vi:
                    is_counterpart = False
                    for y in neighbours_vj:
                        if MP[x, y] == 1:
                            is_counterpart = True
                    if not is_counterpart:
                        MP[i, j] = 0
                        return MP
    return MP


def ullman_v1_0(used_cols, curr_row, G, P, M, no_recursion):

    if curr_row == M.shape[0]:
        if is_isomorphism(M, P, G):
            print("Przekodowanie:")
            print(M)
            print("\n")
        return no_recursion

    M_ = M.copy()

    for c in range(M.shape[1]):
        if c not in used_cols:
            M_[curr_row, :] = 0
            M_[curr_row, c] = 1

            used_cols.append(c)

            no_recursion = ullman_v1_0(used_cols, curr_row + 1, G, P, M_, no_recursion + 1)

            for i in range(len(used_cols)):
                if used_cols[i] == c:
                    used_cols.pop(i)
    return no_recursion


def ullman_v2_0(used_cols, curr_row, G, P, M, no_recursion):

    if curr_row == M.shape[0]:
        if is_isomorphism(M, P, G):
            print("Przekodowanie:")
            print(M)
            print("\n")
        return no_recursion

    M_ = M.copy()

    for c in range(M.shape[1]):
        if c not in used_cols:
            if M0(c, curr_row, G, P):
                M_[curr_row, :] = 0
                M_[curr_row, c] = 1

                used_cols.append(c)

                no_recursion = ullman_v2_0(used_cols, curr_row + 1, G, P, M_, no_recursion + 1)

                for i in range(len(used_cols)):
                    if used_cols[i] == c:
                        used_cols.pop(i)
    return no_recursion


def ullman_v3_0(used_cols, curr_row, G, P, M, no_recursion):
    if curr_row == M.shape[0]:
        if is_isomorphism(M, P, G):
            print("Przekodowanie:")
            print(M)
            print("\n")
        return no_recursion

    M_ = M.copy()

    for c in range(M.shape[1]):
        if c not in used_cols:
            if M0(c, curr_row, G, P):
                M_[curr_row, :] = 0
                M_[curr_row, c] = 1

                no_isomorphism = False
                if curr_row == M_.shape[0] - 1:
                    M_P = prune(M_, P, G, curr_row)
                    for i in range(curr_row):
                        if 1 not in M_P[i]:
                            no_isomorphism = True

                if not no_isomorphism:
                    used_cols.append(c)
                    no_recursion = ullman_v3_0(used_cols, curr_row + 1, G, P, M_, no_recursion + 1)
                    for i in range(len(used_cols)):
                        if used_cols[i] == c:
                            used_cols.pop(i)
    return no_recursion


def create_graph(graf):
    G = GraphMatrix()

    for edge in graf:
        G.insertVertex(edge[0])
        G.insertVertex(edge[1])

    for edge in graf:
        G.insertEdge(edge[0], edge[1])
        G.insertEdge(edge[1], edge[0])

    return G


def main():
    graph_G = [('A','B',1), ('B','F',1), ('B','C',1), ('C','D',1), ('C','E',1), ('D','E',1)]
    graph_P = [('A','B',1), ('B','C',1), ('A','C',1)]


    G = create_graph(graph_G)
    P = create_graph(graph_P)

    M = np.array(P.order() * [G.order() * [0]])
    print("Ullman w wersji 1.0:")
    recursions = ullman_v1_0([], 0, G, P, M, no_recursion=0)

    print("Liczba rekurencji: ", recursions)
    print("\n")

    # =============================
    G = create_graph(graph_G)
    P = create_graph(graph_P)

    M = np.array(P.order() * [G.order() * [0]])
    print("Ullman w wersji 2.0:")
    recursions = ullman_v2_0([], 0, G, P, M, no_recursion=0)

    print("Liczba rekurencji: ", recursions)
    print("\n")

    # =============================
    G = create_graph(graph_G)
    P = create_graph(graph_P)
    M = np.array(P.order() * [G.order() * [0]])
    print("Ullman w wersji 3.0:")
    recursions = ullman_v3_0([], 0, G, P, M, no_recursion=0)

    print("Liczba rekurencji: ", recursions)
    print("\n")



if __name__ == "__main__":
    main()
