class Matrix:
    def __init__(self, data: list[list[float]]):
        self.data = data
        self.shape = (len(data), len(data[0]))
    
    def __str__(self) -> str:
        str = f"Matrix{self.shape}\n"
        for row in self.data:
            for elem in row:
                str += f"{elem}\t"
            str += "\n"
        return str
    
    def __getitem__(self, index: int) -> list[float]:
        return self.data[index]
    
    def __eq__(self, other: 'Matrix') -> bool:
        if self.shape != other.shape:
            return False
        return self.data == other.data

    def __add__(self, other: 'Matrix') -> 'Matrix':
        if self.shape != other.shape:
            raise ValueError("Matrices must have the same shape")
        return Matrix([[self.data[i][j] + other.data[i][j] for j in range(self.shape[1])] for i in range(self.shape[0])])
    
    def __sub__(self, other: 'Matrix') -> 'Matrix':
        if self.shape != other.shape:
            raise ValueError("Matrices must have the same shape")
        return Matrix([[self.data[i][j] - other.data[i][j] for j in range(self.shape[1])] for i in range(self.shape[0])])
    
    def __mul__(self, other) -> 'Matrix':
        if type(other) == int:
            return Matrix([[self.data[i][j] * other for j in range(self.shape[1])] for i in range(self.shape[0])])

        if self.shape[1] != other.shape[0]:
            raise ValueError("Number of columns in the first matrix must be equal to the number of rows in the second matrix")

        n = self.shape[0]
        m = self.shape[1]
        p = other.shape[1]
        data = Matrix.new(n, p)
        for i in range(n):
            for j in range(p):
                value = 0
                for k in range(m):
                    value += self.data[i][k] * other.data[k][j]
                data.data[i][j] = value

        return data
    
    def set_diagonal(self, value: float, diagonal: int = 0) -> 'Matrix':
        if self.shape[0] != self.shape[1]:
            raise ValueError("Matrix must be square")
        for i in range(self.shape[0]):
            if 0 <= i + diagonal < self.shape[0]:
                self.data[i][i + diagonal] = value
        return self
    
    def norm(self) -> float:
        result = 0
        for row in self.data:
            for elem in row:
                result += elem ** 2
        return result ** 0.5
    
    def as_latex(self, max_rows: int = 20, max_cols: int = 20, precision: int = 2) -> str:
        data = self.data
        rows = self.shape[0]
        cols = self.shape[1]
        
        if rows > max_rows:
            data = data[:max_rows//2] + [['...'] * cols] + data[-max_rows//2:]
            rows = max_rows
        if cols > max_cols:
            data = [row[:max_cols//2] + ['...'] + row[-max_cols//2:] for row in data]
            cols = max_cols
        for row in range(rows):
            for col in range(cols):
                if type(data[row][col]) is float:
                    data[row][col] = round(data[row][col], precision)
        
        result = '\\begin{bmatrix}\n'
        for i in range(rows):
            for j in range(cols):
                result += str(data[i][j]) + ' & '
            result = result[:-2] + '\\\\ \n'
        result += '\\end{bmatrix}'
        
        return result
    
    def as_typst(self, max_rows: int = 20, max_cols: int = 20, precision: int = 2) -> str:
        data = self.data
        rows = self.shape[0]
        cols = self.shape[1]

        if rows > max_rows:
            data = data[:max_rows//2] + [['dots.h'] * cols] + data[-max_rows//2:]
            rows = max_rows
        if cols > max_cols:
            data = [row[:max_cols//2] + ['dots.h'] + row[-max_cols//2:] for row in data]
            cols = max_cols
        for row in range(rows):
            for col in range(cols):
                if type(data[row][col]) is float:
                    data[row][col] = round(data[row][col], precision)

        result = 'mat(\n'
        for i in range(rows):
            result += '  '
            for j in range(cols):
                result += str(data[i][j]) + ', '
            result = result[:-2] + ';\n'
        result += ')'

        return result
    
    def copy(self) -> 'Matrix':
        return Matrix([row.copy() for row in self.data])

    @staticmethod
    def vectorize_list(data: list) -> 'Matrix':
        return Matrix([[elem] for elem in data])
    
    @staticmethod
    def vector(n: int, value: int = 0) -> 'Matrix':
        return Matrix.new(n, 1, value)
    
    @staticmethod
    def new(n: int, m: int, value: int = 0) -> 'Matrix':
        return Matrix([[value for _ in range(m)] for _ in range(n)])
    