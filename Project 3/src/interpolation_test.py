from interpolation import *

def test_linspace():
    start = 0
    stop = 10
    num = 5

    result = linspace(start, stop, num)

    expected = [0, 2.5, 5, 7.5, 10]

    assert result == expected

def test_generate_chebyshev_nodes():
    start = -1
    stop = 1
    n = 20

    result = generate_chebyshev_nodes(start, stop, n)
    expected = [math.cos((2 * k + 1) * math.pi / (2 * n)) for k in range(n)]

    assert result == expected

def test_lagrange_interpolation_for_point():
    x_points = [0, 2, 3, 4]
    y_points = [4, 1, 6, 1]

    yminus1 = lagrange_interpolation_for_point(-1, x_points, y_points)
    y1 = lagrange_interpolation_for_point(1, x_points, y_points)
    y5 = lagrange_interpolation_for_point(5, x_points, y_points)

    assert yminus1 == 33.5
    assert y1 == -3.25
    assert y5 == -24.75

def test_lagrange_interpolation():
    x = [-1, 1, 5]
    x_points = [0, 2, 3, 4]
    y_points = [4, 1, 6, 1]


    y = lagrange_interpolation(x, x_points, y_points)

    expected = [33.5, -3.25, -24.75]
    assert y == expected