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
        

def solve_jacobi(A: Matrix, b: Matrix, precision: float = 1e-12, error_threshold: float = 1e12) -> SolverResult:
    if A.shape[0] != A.shape[1]:
        raise ValueError("Matrix A must be square")
    if A.shape[0] != b.shape[0]:
        raise ValueError("Matrix A and vector b must have the same number of rows")
    if b.shape[1] != 1:
        raise ValueError("Vector b must have only one column")
    
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
    if A.shape[0] != A.shape[1]:
        raise ValueError("Matrix A must be square")
    if A.shape[0] != b.shape[0]:
        raise ValueError("Matrix A and vector b must have the same number of rows")
    if b.shape[1] != 1:
        raise ValueError("Vector b must have only one column")
    
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