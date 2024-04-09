#pragma once

#include <cmath>
#include <vector>
#include <chrono>
#include "matrix.h"

class SolverResult {
public:
    SolverResult(Matrix x, double error, std::vector<double> error_history, int iterations, double time, bool finished = true);

    Matrix x;
    double error;
    std::vector<double> error_history;
    int iterations;
    double time;
    bool finished;
};

void validateMatrices(const Matrix& A, const Matrix& b);
SolverResult solveJacobi(Matrix& A, Matrix& b, double precision = 1e-10, double error_threshold = 1e10);
SolverResult solveGaussSeidel(Matrix& A, Matrix& b, double precision = 1e-10, double error_threshold = 1e10);
std::pair<Matrix, Matrix> luDecomposition(Matrix& A);
SolverResult solveLU(Matrix &A, Matrix &b);

