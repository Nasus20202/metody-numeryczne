#pragma once

#include <vector>
#include <iostream>

class Matrix
{
public:
    Matrix(const std::vector<std::vector<double>> &data);
    Matrix(const int rows, const int cols);
    friend std::ostream &operator<<(std::ostream &os, const Matrix &matrix);
    std::vector<double> &operator[](int index);
    bool operator==(const Matrix &other) const;
    Matrix operator+(const Matrix &other) const;
    Matrix operator-(const Matrix &other) const;
    Matrix operator*(const Matrix &other) const;
    Matrix operator*(double scalar) const;
    Matrix &set_diagonal(double value, int diagonal = 0);
    double norm() const;

    std::vector<std::vector<double>> data;
    std::pair<int, int> shape;
};

std::ostream &operator<<(std::ostream &os, const Matrix &matrix);
