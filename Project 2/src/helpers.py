from matrix import Matrix
from IPython.display import display, Math
from math import sin

def display_matrix(matrix: Matrix, max_rows: int = 20, max_cols: int = 20, precision: int = 2) -> None:
    display(Math(matrix.as_latex(max_cols=max_cols, max_rows=max_rows, precision=precision)))

def generate_A_matrix(N: int, a1: int, a2: int, a3: int) -> Matrix:
    return Matrix.new(N, N) \
        .set_diagonal(a1, 0) \
        .set_diagonal(a2, 1) \
        .set_diagonal(a3, 2) \
        .set_diagonal(a2, -1) \
        .set_diagonal(a3, -2)

def generate_b_vector(N: int, f: int) -> Matrix:
    data = []
    for i in range(N):
        data.append(sin((i+1) * (f + 1)))
    return Matrix.vectorize_list(data)