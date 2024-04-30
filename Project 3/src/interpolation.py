from matrix import Matrix

def linspace(start, stop, num=50):
    return [start + (stop - start) * i / (num - 1) for i in range(num)]

def lagrange_interpolation_for_point(x: float, data: Matrix) -> float:
    # https://www.codesansar.com/numerical-methods/lagrange-interpolation-method-pseudocode.htm

    n = data.shape[0]
    y = 0
    for i in range(n):
        p = 1
        for j in range(n):
            if i != j:
                p *= (x - data[j][0]) / (data[i][0] - data[j][0])
        y += p * data[i][1]
    return y

def lagrange_interpolation(x: Matrix, data: Matrix) -> Matrix:
    y = []
    for i in range(x.shape[0]):
        y.append([x[i][0], lagrange_interpolation_for_point(x[i][0], data)])
    return Matrix(y)
