from matrix import Matrix

def test_sum():
    matrix0 = Matrix([[1,2,3],[4,5,6]])
    matrix1 = Matrix([[7, 8, 9], [10, 11, 12]])
    
    excepted = Matrix([[8, 10, 12], [14, 16, 18]])

    assert matrix0 + matrix1 == excepted

def test_sub():
    matrix0 = Matrix([[1,2,3],[4,5,6]])
    matrix1 = Matrix([[7, 8, 9], [10, 11, 12]])
    
    excepted = Matrix([[-6, -6, -6], [-6, -6, -6]])

    assert matrix0 - matrix1 == excepted

def test_mul():
    matrix0 = Matrix([[1,2,3],[4,5,6]])
    matrix1 = Matrix([[7, 8], [9, 10], [11, 12]])
    
    excepted = Matrix([[58, 64], [139, 154]])

    assert matrix0 * matrix1 == excepted

def test_mul_exception():
    matrix0 = Matrix([[1,2,3],[4,5,6]])
    
    try:
        matrix0 * matrix0
        assert False
    except ValueError:
        assert True