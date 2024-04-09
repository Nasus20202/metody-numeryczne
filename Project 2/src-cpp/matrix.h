#pragma once

#include <vector>
#include <iostream>

class Matrix
{
public:
    Matrix(const std::vector<std::vector<double>> &data);
    Matrix(const int rows, const int cols);
    friend std::ostream &operator<<(std::ostream &os, const Matrix &matrix);
    double &operator()(int x, int y);
    bool operator==(const Matrix &other) const;
    Matrix operator+(Matrix &other);
    Matrix operator-(Matrix &other);
    Matrix operator*(Matrix &other);
    Matrix operator*(double scalar);
    Matrix &set_diagonal(double value, int diagonal = 0);
    double norm() const;

    std::vector<double> data;
    std::pair<int, int> shape;
};

std::ostream &operator<<(std::ostream &os, const Matrix &matrix);
