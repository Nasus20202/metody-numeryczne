import time
from matrix import Matrix
   
def validate_matrices(A: Matrix, b: Matrix) -> None:
    if A.shape[0] != A.shape[1]:
        raise ValueError("Matrix A must be square")
    if A.shape[0] != b.shape[0]:
        raise ValueError("Matrix A and vector b must have the same number of rows")
    if b.shape[1] != 1:
        raise ValueError("Vector b must have only one column")

def pivot(U: Matrix, L: Matrix, P: Matrix, i: int) -> None:
    n = U.shape[0]
    max_value = 0
    max_index = i
    for j in range(i, n):
        if abs(U.data[j][i]) > max_value:
            max_value = abs(U.data[j][i])
            max_index = j
    if max_index != i:
        U.data[i], U.data[max_index] = U.data[max_index], U.data[i]
        L.data[i], L.data[max_index] = L.data[max_index], L.data[i]
        P.data[i], P.data[max_index] = P.data[max_index], P.data[i]

def lu_decomposition(A: Matrix) -> tuple[Matrix, Matrix, Matrix]:
    if A.shape[0] != A.shape[1]:
        raise ValueError("Matrix A must be square")
    
    # https://en.wikipedia.org/wiki/LU_decomposition
    # https://www.geeksforgeeks.org/doolittle-algorithm-lu-decomposition/
    n = A.shape[0]
    L = Matrix.new(n, n)
    U = A.copy()
    P = Matrix.new(n, n)
    
    L.set_diagonal(1)
    P.set_diagonal(1)

    for i in range(n):
        pivot(U, L, P, i)
        for j in range(i+1, n):
            # lower triangular
            L.data[j][i] = U.data[j][i] / U.data[i][i]

            # upper triangular
            for k in range(i, n):
                U.data[j][k] -= L.data[j][i] * U.data[i][k]

    return L, U, P


def solve_forward_substitution(L: Matrix, b: Matrix) -> Matrix:
    validate_matrices(L, b)

    # https://en.wikipedia.org/wiki/Triangular_matrix#Forward_and_back_substitution
    # https://algowiki-project.org/en/Forward_substitution
    n = L.shape[0]
    x = Matrix.vector(n)
    for m in range(n):
        x.data[m][0] = b.data[m][0] - (sum([L.data[m][i] * x.data[i][0] for i in range(m)]))
    return x

def solve_backward_substitution(U: Matrix, b: Matrix) -> Matrix:
    validate_matrices(U, b)

    # https://en.wikipedia.org/wiki/Triangular_matrix#Forward_and_back_substitution
    # https://algowiki-project.org/en/Backward_substitution
    n = U.shape[0]
    x = Matrix.vector(n)
    for m in range(n-1, -1, -1):
        x.data[m][0] = (b.data[m][0] - sum([U.data[m][i] * x.data[i][0] for i in range(m+1, n)])) / U.data[m][m]
    return x


def solve_lu_decomposition(A: Matrix, b: Matrix) -> Matrix:
    validate_matrices(A, b)

    # https://en.wikipedia.org/wiki/LU_decomposition
    # https://www.sheffield.ac.uk/media/32074/download?attachment

    L, U, P = lu_decomposition(A)
    b = P * b
    
    n = A.shape[0]
    x = Matrix.vector(n)
    y = Matrix.vector(n)
    
    # Ly = b
    y = solve_forward_substitution(L, b)
    # Ux = y
    x = solve_backward_substitution(U, y)

    return x

