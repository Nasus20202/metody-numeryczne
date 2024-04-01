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
test_jacobi()


