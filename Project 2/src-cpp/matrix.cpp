#include "matrix.h"
#include <cmath>

Matrix::Matrix(const std::vector<std::vector<double>> &data)
{
    shape = {data.size(), data[0].size()};
    this->data = std::vector<double>(shape.first * shape.second);
    for (int i = 0; i < shape.first; i++)
    {
        for (int j = 0; j < shape.second; j++)
        {
            this->data[i * shape.second + j] = data[i][j];
        }
    }
}

Matrix::Matrix(const int rows, const int cols) : shape({rows, cols})
{
    data = std::vector<double>(rows * cols, 0.0f);
}

double &Matrix::operator()(int x, int y)
{
    return data[x * shape.second + y];
}

bool Matrix::operator==(const Matrix &other) const
{
    if (shape != other.shape)
    {
        return false;
    }
    return data == other.data;
}

Matrix Matrix::operator+(Matrix &other)
{
    if (shape != other.shape)
    {
        throw std::invalid_argument("Matrices must have the same shape");
    }
    std::vector<std::vector<double>> result(shape.first, std::vector<double>(shape.second));
    for (int i = 0; i < shape.first; i++)
    {
        for (int j = 0; j < shape.second; j++)
        {
            result[i][j] = this->operator()(i, j) + other(i, j);
        }
    }
    return Matrix(result);
}

Matrix Matrix::operator-(Matrix &other)
{
    if (shape != other.shape)
    {
        throw std::invalid_argument("Matrices must have the same shape");
    }
    std::vector<std::vector<double>> result(shape.first, std::vector<double>(shape.second));
    for (int i = 0; i < shape.first; i++)
    {
        for (int j = 0; j < shape.second; j++)
        {
            result[i][j] = this->operator()(i, j) - other(i, j);
        }
    }
    return Matrix(result);
}

Matrix Matrix::operator*(Matrix &other)
{
    if (shape.second != other.shape.first)
    {
        throw std::invalid_argument("Number of columns in the first matrix must be equal to the number of rows in the second matrix");
    }
    int n = shape.first;
    int m = shape.second;
    int p = other.shape.second;
    std::vector<std::vector<double>> result(n, std::vector<double>(p, 0.0f));
    for (int i = 0; i < n; i++)
    {
        for (int j = 0; j < p; j++)
        {
            for (int k = 0; k < m; k++)
            {
                result[i][j] += this->operator()(i, k) * other(k, j);
            }
        }
    }
    return Matrix(result);
}

Matrix Matrix::operator*(double scalar)
{
    std::vector<std::vector<double>> result(shape.first, std::vector<double>(shape.second));
    for (int i = 0; i < shape.first; i++)
    {
        for (int j = 0; j < shape.second; j++)
        {
            result[i][j] = this->operator()(i, j) * scalar;
        }
    }
    return Matrix(result);
}

Matrix &Matrix::set_diagonal(double value, int diagonal)
{
    if (shape.first != shape.second)
    {
        throw std::invalid_argument("Matrix must be square");
    }
    for (int i = 0; i < shape.first; i++)
    {
        if (0 <= i + diagonal && i + diagonal < shape.second)
        {
            this->operator()(i, i + diagonal) = value;
        }
    }
    return *this;
}

double Matrix::norm() const
{
    double result = 0.0f;
    for (const double elem : data)
    {
        result += elem * elem;
    }
    return std::sqrt(result);
}

std::ostream &operator<<(std::ostream &os, const Matrix &matrix)
{
    os << "Matrix(" << matrix.shape.first << "x" << matrix.shape.second << ")\n";
    int counter = 0;
    for (const double elem : matrix.data)
    {
        os << elem << "\t";
        if (++counter % matrix.shape.second == 0)
        {
            os << "\n";
        }
    }
    return os;
}
