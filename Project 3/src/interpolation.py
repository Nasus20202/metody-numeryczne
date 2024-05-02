import math
from matrix import Matrix
from solvers import solve_lu_decomposition

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

def lagrange_interpolation(points_to_interpolate: list[float], x_points: list[float], y_points: list[float]) -> list[float]:
    y = []
    for i in points_to_interpolate:
        y.append(lagrange_interpolation_for_point(i, x_points, y_points))
    return y

def spline_interpolation(points_to_interpolate: list[float], x_points: list[float], y_points: list[float]) -> list[float]:
    if len(x_points) != len(y_points):
        raise ValueError("x_points and y_points must have the same length")

    nodes = len(x_points)
    n = 4 * (len(x_points) - 1)
    A = Matrix.new(n, n)
    b = Matrix.vector(n)
    x = Matrix.vector(n, 1)
    
    # S_0(x0) = y_0
    A[0][0] = 1
    b[0][0] = y_points[0]

     # S_0(x1) = y_1
    h = x_points[1] - x_points[0]
    A[1][0] = 1
    A[1][1] = h
    A[1][2] = h ** 2
    A[1][3] = h ** 3
    b[1][0] = y_points[1]

    # S''_0(x0) = 0
    A[2][2] = 1
    b[2][0] = 0

    # S''_{n-1}(x_n) = 0
    h = x_points[-1] - x_points[-2]
    A[3][4 * (nodes - 2) + 2] = 2
    A[3][4 * (nodes - 2) + 3] = 6 * h
    b[3][0] = 0

    for i in range(1, nodes - 1):
        h = x_points[i] - x_points[i - 1]

        # S_i(x_i) = y_i
        A[4 * i][4 * i] = 1
        b[4 * i][0] = y_points[i]

        # S_i(x_{i+1}) = y_{i+1}
        A[4 * i + 1][4 * i] = 1
        A[4 * i + 1][4 * i + 1] = h
        A[4 * i + 1][4 * i + 2] = h ** 2
        A[4 * i + 1][4 * i + 3] = h ** 3
        b[4 * i + 1][0] = y_points[i + 1]

        # S'_i(x_i) = S'_{i-1}(x_i)
        A[4 * i + 2][4 * (i - 1) + 1] = 1
        A[4 * i + 2][4 * (i - 1) + 2] = 2 * h
        A[4 * i + 2][4 * (i - 1) + 3] = 3 * h ** 2
        A[4 * i + 2][4 * i + 1] = -1
        b[4 * i + 2][0] = 0

        # S''_i(x_i) = S''_{i-1}(x_i)
        A[4 * i + 3][4 * (i - 1) + 2] = 2
        A[4 * i + 3][4 * (i - 1) + 3] = 6 * h
        A[4 * i + 3][4 * i + 2] = -2
        b[4 * i + 3][0] = 0
        

    x = solve_lu_decomposition(A, b)
    interpolated_y = []
    for i in points_to_interpolate:
        found = False
        for j in range(nodes-1):
            if x_points[j] <= i <= x_points[j + 1]:
                h = i - x_points[j]
                j = 4 * j
                interpolated_y.append(x[j][0] + x[j + 1][0] * h + x[j + 2][0] * h ** 2 + x[j + 3][0] * h ** 3)
                found = True
                break
        if not found:
            interpolated_y.append(interpolated_y[-1])
    return interpolated_y

    
    
            

        

