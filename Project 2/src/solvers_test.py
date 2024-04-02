from matrix import Matrix
from solvers import *

def almost_equal(a: float, b: float, epsilon: float = 10e-12) -> bool:
    if abs(a - b) > epsilon:
        return False
    return True

def test_jacobi():
    A = Matrix([[2, 1],
                [5, 7]])
    b = Matrix([[11],
                [13]])

    result = solve_jacobi(A, b)

    expected = Matrix([[7+1/9], [-3-2/9]])
    
    assert result.finished
    assert almost_equal(result.x[0][0], expected[0][0])
    assert almost_equal(result.x[1][0], expected[1][0])

def test_gauss_seidel():
    A = Matrix([[2, 1],
                [5, 7]])
    b = Matrix([[11],
                [13]])

    result = solve_gauss_seidel(A, b)

    expected = Matrix([[7+1/9], [-3-2/9]])
    
    assert result.finished
    assert almost_equal(result.x[0][0], expected[0][0])
    assert almost_equal(result.x[1][0], expected[1][0])

def test_lu_decomposition():
    A = Matrix([[1, 2, 4],
                [3, 8, 14],
                [2, 6, 13]])
    
    L, U = lu_decomposition(A)

    expected_L = Matrix([[1, 0, 0],
                         [3, 1, 0],
                         [2, 1, 1]])
    expected_U = Matrix([[1, 2, 4],
                         [0, 2, 2],
                         [0, 0, 3]])
    
    assert L == expected_L
    assert U == expected_U
    assert (L * U) == A

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
    
    assert result.finished
    assert result.x == expected

