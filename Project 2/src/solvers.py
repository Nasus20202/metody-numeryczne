import time
from matrix import Matrix

class SolverResult:
    def __init__(self, x: Matrix, error: float, error_history: list[float], iterations: int,  time: float, finished: bool = True):
        self.x = x
        self.error = error
        self.error_history = error_history
        self.iterations = iterations
        self.time = time
        self.finished = finished
        
def validate_matrices(A: Matrix, b: Matrix) -> None:
    if A.shape[0] != A.shape[1]:
        raise ValueError("Matrix A must be square")
    if A.shape[0] != b.shape[0]:
        raise ValueError("Matrix A and vector b must have the same number of rows")
    if b.shape[1] != 1:
        raise ValueError("Vector b must have only one column")

def solve_jacobi(A: Matrix, b: Matrix, precision: float = 1e-12, error_threshold: float = 1e12) -> SolverResult:
    validate_matrices(A, b)
    
    # https://en.wikipedia.org/wiki/Jacobi_method#Matrix-based_formula
    n = A.shape[0]

    x = Matrix.vector(n)
    error = float('inf')
    error_history = []
    iterations = 0
    finished = True

    start_time = time.perf_counter_ns()
    while error > precision:
        new_x = Matrix.vector(n)
        for i in range(n):
            new_x[i][0] = 1/A[i][i] * (b[i][0] - sum([A[i][j] * x[j][0] for j in range(n) if j != i]))
        x = new_x
        iterations += 1
        error = (A * x - b).norm()
        error_history.append(error)
        if error > error_threshold:
            finished = False
            break
    end_time = time.perf_counter_ns() 
    total_time = (end_time - start_time) / 1e9
    return SolverResult(x, error, error_history, iterations, total_time, finished)

def solve_gauss_seidel(A: Matrix, b: Matrix, precision: float = 1e-12, error_threshold: float = 1e12) -> SolverResult:
    validate_matrices(A, b)
    
    # https://en.wikipedia.org/wiki/Gauss%E2%80%93Seidel_method#Element-based_formula
    n = A.shape[0]

    x = Matrix.vector(n)
    error = float('inf')
    error_history = []
    iterations = 0
    finished = True

    start_time = time.perf_counter_ns()
    while error > precision:
        new_x = Matrix.vector(n)
        for i in range(n):
            new_x[i][0] = 1/A[i][i] * (b[i][0] - sum([A[i][j] * new_x[j][0] for j in range(i)]) - sum([A[i][j] * x[j][0] for j in range(i+1, n)]))
        x = new_x
        iterations += 1
        error = (A * x - b).norm()
        error_history.append(error)
        if error > error_threshold:
            finished = False
            break
    end_time = time.perf_counter_ns() 
    total_time = (end_time - start_time) / 1e9
    return SolverResult(x, error, error_history, iterations, total_time, finished)

def lu_decomposition(A: Matrix) -> tuple[Matrix, Matrix]:
    if A.shape[0] != A.shape[1]:
        raise ValueError("Matrix A must be square")
    
    # https://en.wikipedia.org/wiki/LU_decomposition
    # https://www.geeksforgeeks.org/doolittle-algorithm-lu-decomposition/
    n = A.shape[0]
    L = Matrix.new(n, n)
    U = Matrix.new(n, n)
    
    L.set_diagonal(1)
    for i in range(n):
        # upper triangular
        for j in range(i, n):
            U[i][j] = A[i][j] - sum([L[i][k] * U[k][j] for k in range(i)])

        # lower triangular
        for j in range(i+1, n):
            L[j][i] = 1/U[i][i] * (A[j][i] - sum([L[j][k] * U[k][i] for k in range(i)]))

    return L, U

def solve_forward_substitution(L: Matrix, b: Matrix) -> Matrix:
    validate_matrices(L, b)

    # https://en.wikipedia.org/wiki/Triangular_matrix#Forward_and_back_substitution
    n = L.shape[0]
    x = Matrix.vector(n)
    for m in range(n):
        x[m][0] = 1/L[m][m] * (b[m][0] - sum([L[m][i] * x[i][0] for i in range(m)]))
    return x

def solve_backward_substitution(U: Matrix, b: Matrix) -> Matrix:
    validate_matrices(U, b)

    # https://en.wikipedia.org/wiki/Triangular_matrix#Forward_and_back_substitution
    # https://algowiki-project.org/en/Backward_substitution
    n = U.shape[0]
    x = Matrix.vector(n)
    for m in range(n-1, -1, -1):
        x[m][0] = 1/U[m][m] * (b[m][0] - sum([U[m][i] * x[i][0] for i in range(m+1, n)]))
    return x


def solve_lu_decomposition(A: Matrix, b: Matrix) -> SolverResult:
    validate_matrices(A, b)

    # https://en.wikipedia.org/wiki/LU_decomposition
    # https://www.sheffield.ac.uk/media/32074/download?attachment

    start_time = time.perf_counter_ns()
    L, U = lu_decomposition(A)
    
    n = A.shape[0]
    x = Matrix.vector(n)
    y = Matrix.vector(n)
    
    # Ly = b
    y = solve_forward_substitution(L, b)
    # Ux = y
    x = solve_backward_substitution(U, y)

    error = (A * x - b).norm()
    end_time = time.perf_counter_ns()
    total_time = (end_time - start_time) / 1e9
    return SolverResult(x, error, [], 1, total_time, True)

