from typing import Tuple
from IPython.display import display, Math
from matrix import Matrix
import csv

def display_matrix(matrix: Matrix, max_rows: int = 20, max_cols: int = 20, precision: int = 4) -> None:
    display(Math(matrix.as_latex(max_rows, max_cols, precision)))

def display_matrices(matrices: list[Tuple[Matrix, str]], max_rows: int = 20, max_cols: int = 20, precision: int = 4) -> None:
    display(Math(''.join([f"{name} = {matrix.as_latex(max_rows, max_cols, precision)}" for matrix, name in matrices])))

def load_data(file_name: str, delimeter: str = ",", path: str = "../data/") -> Matrix:
    with open(path + file_name, 'r') as file:
        reader = csv.reader(file, delimiter=delimeter)
        data = []
        for row in reader:
            try:
                data.append([float(x) for x in row])
            except ValueError:
                continue
    return Matrix(data)