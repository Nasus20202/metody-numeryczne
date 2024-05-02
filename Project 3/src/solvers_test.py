from matrix import Matrix
from solvers import *

def almost_equal(a: float, b: float, epsilon: float = 10e-12) -> bool:
    if abs(a - b) > epsilon:
        return False
    return True

def test_forward_substitution():
    L = Matrix([[1, 0, 0],
                [3, 1, 0],
                [2, 1, 1]])
    b = Matrix([[3],
                [13],
                [4]])

    result = solve_forward_substitution(L, b)

    expected = Matrix([[3], [4], [-6]])

    assert result == expected

def test_backward_substitution():
    U = Matrix([[1, 2, 4],
                [0, 2, 2],
                [0, 0, 3]])
    b = Matrix([[3],
                [4],
                [-6]])

    result = solve_backward_substitution(U, b)

    expected = Matrix([[3], [4], [-2]])

    assert result == expected

def test_solve_lu_decomposition():
    A = Matrix([[1, 2, 4],
                [3, 8, 14],
                [2, 6, 13]])
    b = Matrix([[3],
                [13],
                [4]])

    result = solve_lu_decomposition(A, b)

    expected = Matrix([[3], [4], [-2]])
    for i in range(3):
        assert almost_equal(result.data[i][0], expected.data[i][0])

