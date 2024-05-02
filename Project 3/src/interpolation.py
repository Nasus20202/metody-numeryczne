import math
from matrix import Matrix

def linspace(start: float, stop: float, n: int = 100) -> list[float]:
    return [start + (stop - start) * i / (n - 1) for i in range(n)]

def generate_chebyshev_nodes(start: float, stop: float, n: int = 100) -> list[float]:
    # https://en.wikipedia.org/wiki/Chebyshev_nodes

    nodes = []
    for k in range(n):
        nodes.append(0.5 * (start + stop) + 0.5 * (stop - start) * math.cos((2 * k + 1) * math.pi / (2 * n)))
    return nodes

def lagrange_interpolation_for_point(x: float, x_points: list[float], y_points: list[float]) -> float:
    # https://www.codesansar.com/numerical-methods/lagrange-interpolation-method-pseudocode.htm

    if len(x_points) != len(y_points):
        raise ValueError("x_points and y_points must have the same length")

    n = len(x_points)
    y = 0
    for i in range(n):
        p = 1
        for j in range(n):
            if i != j:
                p *= (x - x_points[j]) / (x_points[i] - x_points[j])
        y += p * y_points[i]
    return y

def lagrange_interpolation(x: list[float], x_points: list[float], y_points: list[float]) -> list[float]:
    y = []
    for i in x:
        y.append(lagrange_interpolation_for_point(i, x_points, y_points))
    return y

def spline_interpolation(x_points: list[float], y_points: list[float]) -> list[float]:
    if len(x_points) != len(y_points):
        raise ValueError("x_points and y_points must have the same length")

    n = len(x_points) - 1 # number of intervals
    A = Matrix.new(4 *n, 4 * n)
    y = Matrix.vector(4 * n)

    h = 0

    for i in range(n):
        h = x_points[i + 1] - x_points[i]
        j = 4 * i

        # S_j(x_j) = y_j
        A[j][j] = 1
        y[j][0] = y_points[i]

        # S_j(x_{j+1}) = y_{j+1}
        A[j + 1][j + 0] = 1
        A[j + 1][j + 1] = h
        A[j + 1][j + 2] = h ** 2
        A[j + 1][j + 3] = h ** 3
        y[j + 1][0] = y_points[i + 1]

        if i != 0: # inner node
            # S'_{j-1}(x_j) = S'_j(x_j)
            A[j + 2][j - 3] = 1
            A[j + 2][j - 2] = 2 * h
            A[j + 2][j - 1] = 3 * (h ** 2)
            A[j + 2][j + 1] = -1
            y[j + 2][0] = 0

            # S''_{i-1}(x_j) = S''_i(x_j)
            A[j + 3][j - 2] = 2
            A[j + 3][j - 1] = 6 * h
            A[j + 3][j + 2] = -2
            y[j + 3][0] = 0


        else: # boundary node
            # S''_0(x_0) = 0
            A[j + 2][j + 2] = 2
            y[j + 2][0] = 0

            # S''_{n-1}(x_n) = 0
            A[j + 3][j + 6] = 2
            A[j + 3][j + 7] = 6 * h
            y[j + 3][0] = 0

    return A, y
            

        

