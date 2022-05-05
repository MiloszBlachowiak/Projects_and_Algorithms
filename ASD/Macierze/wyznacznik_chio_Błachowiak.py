from typing import List, Tuple
from implementacja_macierzy_Błachowiak import Matrix


def chio_det(mat: Matrix):
    d = len(mat.matrix)
    d2 = len(mat.matrix[0])

    if d != d2:
        raise Exception("Macierz nie jest kwadratowa.")

    # implementacja rozwiązania problemu liczenia wyznacznika macierzy z a_11 = 0
    if mat[0][0] == 0:
        i = 1
        while mat.matrix[0][0] == 0 and i < d:
            for j in range(0, d):
                mat[0][j] += mat[i][j]
            i += 1

    if d == 1:
        return mat[0][0]
    if d == 2:
        return mat[0][0] * mat[1][1] - mat[0][1] * mat[1][0]
    else:
        det_mat = Matrix((d-1, d-1))
        for i in range(0, d-1):
            for j in range(0, d-1):
                mat_2x2 = Matrix([[mat[0][0], mat[0][j+1]], [mat[i+1][0], mat[i+1][j+1]]])
                det_mat[i][j] = chio_det(mat_2x2)
        return (1/(mat[0][0] ** (d-2))) * chio_det(det_mat)


macierz_A = Matrix([[5, 1, 1, 2, 3], [4, 2, 1, 7, 3], [2, 1, 2, 4, 7], [9, 1, 0, 7, 0], [1, 4, 7, 2, 2]])

print("Macierz A:")
print(macierz_A)
print("Wyznacznik macierzy A: ", chio_det(macierz_A))

print('\n')

macierz_B = Matrix([[0, 1, 1, 2, 3], [4, 2, 1, 7, 3], [2, 1, 2, 4, 7], [9, 1, 0, 7, 0], [1, 4, 7, 2, 2]])
# Aby wyliczyć wyznacznik tej macierzy musimy pozbyć się zera w a_11, dlatego dodajemy do 1. wiersza kombinację liniową
# pozostałych wierszy
print("Macierz B:")
print(macierz_B)
print("Wyznacznik macierzy B: ", chio_det(macierz_B))
