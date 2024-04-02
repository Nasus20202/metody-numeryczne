from typing import Tuple
from matrix import Matrix
from IPython.display import display, Math
from math import sin
import os
from functools import partial

def display_matrix(matrix: Matrix, max_rows: int = 20, max_cols: int = 20, precision: int = 4) -> None:
    display(Math(matrix.as_latex(max_rows, max_cols, precision)))

def display_matrices(matrices: list[Tuple[Matrix, str]], max_rows: int = 20, max_cols: int = 20, precision: int = 4) -> None:
    display(Math(''.join([f"{name} = {matrix.as_latex(max_rows, max_cols, precision)}" for matrix, name in matrices])))

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

def result_cache(func: partial, serializer: callable, deserializer: callable, file_name: str, cache_dir: str = "../results"):
    if not os.path.exists(cache_dir):
        os.makedirs(cache_dir)
    
    if os.path.exists(f"{cache_dir}/{file_name}"):
        with open(f"{cache_dir}/{file_name}", "r") as file:
            return deserializer(file.read())
    else:
        result = func()
        with open(f"{cache_dir}/{file_name}", "w") as file:
            file.write(serializer(result))
        return result
    
