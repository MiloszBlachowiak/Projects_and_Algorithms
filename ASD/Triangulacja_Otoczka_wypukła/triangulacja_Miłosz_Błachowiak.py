import time


class Point:
    def __init__(self, x, y):
        self.x = x
        self.y = y


def distance(P1, P2):
    return ((P2.x - P1.x) ** 2 + (P2.y - P1.y) ** 2) ** (1/2)


def cost(p, q, r):
    P = Point(p[0], p[1])
    Q = Point(q[0], q[1])
    R = Point(r[0], r[1])
    return distance(P, Q) + distance(P, R) + distance(Q, R)


def triangulation_r(points, i=0, j=None):
    if j is None:
        j = len(points) - 1

    if j - i < 2:
        return 0, []

    min_cost = float('Inf')
    min_triangles = []

    for k in range(i+1, j):
        new_cost = triangulation_r(points, i, k)[0] + cost(points[i], points[k], points[j]) + triangulation_r(points, k, j)[0]
        new_triangles = triangulation_r(points, i, k)[1] + [(points[i], points[k], points[j])] + triangulation_r(points, k, j)[1]
        if new_cost < min_cost:
            min_cost = new_cost
            min_triangles = new_triangles

    return min_cost, min_triangles


def triangulation_dynamic(points):
    l = len(points)
    if l < 3:
        return None

    tab = [[0 for i in range(l)] for j in range(l)]
    triangles = []
    cost_tab = []
    for col in range(l):
        for i, j in zip(range(l), range(col, l)):
            if j - i < 2:
                tab[i][j] = 0
            else:
                tab[i][j] = float('Inf')
                min_k = 0
                for k in range(i+1, j):
                    c = cost(points[i], points[k], points[j])
                    if tab[i][j] > tab[i][k] + c + tab[k][j]:
                        tab[i][j] = tab[i][k] + c + tab[k][j]
    return tab[0][l-1]


def main():
    print("Metoda rekurencyjna:")
    points = [[0, 0], [1, 0], [2, 1], [1, 2], [0, 2]]
    print("Wierzchołki wielokąta:")
    print(points)
    start = time.time()
    minimalny_koszt, triangles = triangulation_r(points)
    print("Czas obliczeń: ", time.time() - start)
    print("Minimalny koszt triangulacji: ", minimalny_koszt)
    print("Wyznaczone trójkąty (współrzędne ich wierzchołków): ")
    print(triangles)
    print("\n")

    points = [[0, 0], [4, 0], [5, 4], [4, 5], [2, 5], [1, 4], [0, 3], [0, 2]]
    print("Wierzchołki wielokąta:")
    print(points)
    start = time.time()
    minimalny_koszt, triangles = triangulation_r(points)
    print("Czas obliczeń: ", time.time() - start)
    print("Minimalny koszt triangulacji: ", minimalny_koszt)
    print("Wyznaczone trójkąty (współrzędne ich wierzchołków): ")
    print(triangles)
    print("\n")

    print("Metoda dynamiczna:")
    points = [[0, 0], [1, 0], [2, 1], [1, 2], [0, 2]]
    print("Wierzchołki wielokąta:")
    print(points)
    start = time.time()
    minimalny_koszt = triangulation_dynamic(points)
    print("Czas obliczeń: ", time.time() - start)
    print("Minimalny koszt triangulacji: ", minimalny_koszt)

    print("\n")
    points = [[0, 0], [4, 0], [5, 4], [4, 5], [2, 5], [1, 4], [0, 3], [0, 2]]
    print("Wierzchołki wielokąta:")
    print(points)
    start = time.time()
    minimalny_koszt = triangulation_dynamic(points)
    print("Czas obliczeń: ", time.time() - start)
    print("Minimalny koszt triangulacji: ", minimalny_koszt)


if __name__ == "__main__":
    main()
