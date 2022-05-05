from typing import List, Tuple


class Matrix:

    def __init__(self, argument, init_value=0):
        if isinstance(argument, Tuple):
            self.matrix = [argument[1] * [init_value] for i in range(0, argument[0])]
        else:
            self.matrix = argument

    def __add__(self, other_matrix):
        result = Matrix((len(self.matrix), len(self.matrix[0])))
        for i in range(0, len(self.matrix)):
            for j in range(0, len(self.matrix[0])):
                result.matrix[i][j] = self.matrix[i][j] + other_matrix[i][j]
        return result

    def __mul__(self, other_matrix):
        if len(self.matrix[0]) != len(other_matrix.matrix):
            raise Exception("Wymiary macierzy się nie zgadzają.")

        result = Matrix((len(self.matrix), len(other_matrix[0])))
        for i in range(0, len(self.matrix)):
            for j in range(0, len(other_matrix[0])):
                mul_sum = 0
                k = 0
                for el in self.matrix[i]:
                    mul_sum += el * other_matrix[k][j]
                    k += 1
                result[i][j] = mul_sum
        return result

    def __getitem__(self, item_nr):
        return self.matrix[item_nr]

    def __str__(self):
        matrix_str = ""
        for i in range(0, len(self.matrix)):
            matrix_str += str(self.matrix[i]) + '\n'
        return matrix_str


def transpose(mat: Matrix):
    tr_matrix = Matrix((len(mat.matrix[0]), len(mat.matrix)))
    for i in range(0, len(tr_matrix.matrix)):
        for j in range(0, len(tr_matrix.matrix[0])):
            tr_matrix[i][j] = mat[j][i]
    return tr_matrix


def main():
    macierz_A = Matrix([[1, 0, 2], [-1, 3, 1]])

    macierz_transponowana = transpose(macierz_A)
    print("Macierz transponowana:")
    print(macierz_transponowana)

    macierz_B = Matrix([[-1, 3, 1], [1, 0, 2]])

    suma_macierzy = macierz_A + macierz_B
    print("Suma macierzy:")
    print(suma_macierzy)

    macierz_C = Matrix([[3, 1], [2, 1], [1, 0]])

    iloczyn_macierzy = macierz_A * macierz_C
    print("Iloczyn macierzy:")
    print(iloczyn_macierzy)


if __name__ == "__main__":
    main()