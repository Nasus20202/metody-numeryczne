import math

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
