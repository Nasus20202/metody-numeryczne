from interpolation import *

def test_linspace():
    start = 0
    stop = 10
    num = 5

    result = linspace(start, stop, num)

    expected = [0, 2.5, 5, 7.5, 10]

    assert result == expected

def test_lagrange_interpolation_for_point():
    data = Matrix([[0, 4], [2, 1], [3, 6], [4, 1]])

    yminus1 = lagrange_interpolation_for_point(-1, data)
    y1 = lagrange_interpolation_for_point(1, data)
    y5 = lagrange_interpolation_for_point(5, data)

    assert yminus1 == 33.5
    assert y1 == -3.25
    assert y5 == -24.75

def test_lagrange_interpolation():
    x = Matrix([[-1], [1], [5]])
    data = Matrix([[0, 4], [2, 1], [3, 6], [4, 1]])

    result = lagrange_interpolation(x, data)

    expected = Matrix([[-1, 33.5], [1, -3.25], [5, -24.75]])
    assert result == expected