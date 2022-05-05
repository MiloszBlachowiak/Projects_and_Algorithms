class Point:
    def __init__(self, x, y):
        self.x = x
        self.y = y


# Jarvis
def is_left_oriented(p, q, r, pts):
    P = pts[p]
    R = pts[r]
    Q = pts[q]

    return (Q.y - P.y) * (R.x - Q.x) - (R.y - Q.y) * (Q.x - P.x) < 0


def choose_next(p, pts):

    if p == len(pts) - 1:
        q = 0
    else:
        q = p + 1

    for i in range(len(pts)):
        if i != q:
            if is_left_oriented(p, i, q, pts):
                q = i
    return q


def Jarvis(points):
    pts = []
    for point in points:
        pts.append(Point(point[0], point[1]))

    left_idx = 0
    for i in range(len(pts) - 1):
        if pts[i + 1].x < pts[left_idx].x:
            left_idx = i + 1
        if pts[i + 1].x == pts[left_idx].x:
            if pts[i + 1].y < pts[left_idx].y:
                left_idx = i + 1

    conv_hull = [(pts[left_idx].x, pts[left_idx].y)]

    p = choose_next(left_idx, pts)

    while p != left_idx:
        conv_hull.append((pts[p].x, pts[p].y))

        p = choose_next(p, pts)

    return conv_hull


# Graham
def distance(P1, P2):
    return ((P2.x - P1.x) ** 2 + (P2.y - P1.y) ** 2) ** (1/2)


def orientation(P, Q, R):
    ang = (Q.y - P.y) * (R.x - Q.x) - (R.y - Q.y) * (Q.x - P.x)
    if ang == 0:
        return 0
    if ang < 0:
        return -1
    if ang > 0:
        return 1


def Graham(points):
    pts = []
    for point in points:
        pts.append(Point(point[0], point[1]))

    bottom_idx = 0
    for i in range(len(pts) - 1):
        if pts[i + 1].y < pts[bottom_idx].y:
            bottom_idx = i + 1
        if pts[i + 1].y == pts[bottom_idx].y:
            if pts[i + 1].x < pts[bottom_idx].x:
                bottom_idx = i + 1

    P0 = pts[bottom_idx]
    pts.pop(bottom_idx)

    changed = True
    while changed:
        changed = False
        for i in range(len(pts) - 1):
            if orientation(P0, pts[i], pts[i+1]) == 1:
                pts[i], pts[i+1] = pts[i+1], pts[i]
                changed = True
            if orientation(P0, pts[i], pts[i+1]) == 0:
                if distance(P0, pts[i+1]) < distance(P0, pts[i]):
                    pts[i], pts[i + 1] = pts[i + 1], pts[i]
                    changed = True

    sorted = pts
    sorted.insert(0, P0)

    i = 1
    while i < len(sorted) - 1:
        if orientation(P0, sorted[i], sorted[i+1]) == 0:
            sorted.pop(i)
        else:
            i += 1

    if len(sorted) < 3:
        return None

    hull = sorted[:3]
    sorted = sorted[3:]

    for point in sorted:
        if orientation(hull[-2], hull[-1], point) != -1:
            hull.pop()
        hull.append(point)

    for i in range(len(hull)):
        hull[i] = (hull[i].x, hull[i].y)

    return hull


def main():
    print("Algorytm Jarvisa")
    points = [(0, 3), (0, 0), (0, 1), (3, 0), (3, 3)]
    print("Zbiór punktów:")
    print(points)
    conv_hull = Jarvis(points)
    print("Otoczka:")
    print(conv_hull)

    points = [(0, 3), (0, 1), (0, 0), (3, 0), (3, 3)]
    print("\nZbiór punktów:")
    print(points)
    conv_hull = Jarvis(points)
    print("Otoczka:")
    print(conv_hull)

    points = [(2, 2), (4, 3), (5, 4), (0, 3), (0, 2), (0, 0), (2, 1), (2, 0), (4, 0)]
    print("\nZbiór punktów:")
    print(points)
    conv_hull = Jarvis(points)
    print("Otoczka:")
    print(conv_hull)

    print("\n\nAlgorytm Grahama")
    points = [(0, 3), (1, 1), (2, 2), (4, 4), (0, 0), (1, 2), (3, 1), (3, 3)]
    print("\nZbiór punktów:")
    print(points)
    conv_hull = Graham(points)
    print("Otoczka:")
    print(conv_hull)


if __name__ == "__main__":
    main()

