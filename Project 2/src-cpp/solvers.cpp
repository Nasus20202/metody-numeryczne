#include "solvers.h"

SolverResult::SolverResult(Matrix x, double error, std::vector<double> error_history, int iterations, double time, bool finished)
    : x(x), error(error), error_history(error_history), iterations(iterations), time(time), finished(finished) {}

void validateMatrices(const Matrix& A, const Matrix& b) {
    if (A.shape.first != A.shape.second) {
        throw std::invalid_argument("Matrix A must be square");
    }
    if (A.shape.first != b.shape.first) {
        throw std::invalid_argument("Matrix A and vector b must have the same number of rows");
    }
    if (b.shape.second != 1) {
        throw std::invalid_argument("Vector b must be a column vector");
    }
}

SolverResult solveJacobi(Matrix& A, Matrix& b, double precision, double error_threshold) {
    validateMatrices(A, b);

    // https://en.wikipedia.org/wiki/Jacobi_method#Element-based_formula
    int n = A.shape.first;

    Matrix x(n, 1);
    double error = INFINITY;
    std::vector<double> error_history;
    int iterations = 0;
    bool finished = true;

    auto start_time = std::chrono::high_resolution_clock::now();
    while (error > precision) {
        Matrix new_x = Matrix(n, 1);
        for (int i = 0; i < n; i++) {
            double sum = 0;
            for (int j = 0; j < n; j++) {
                if (j != i) {
                    sum += A(i, j) * x(j, 0);
                }
            }
            new_x(i, 0) = (b(i, 0) - sum) / A(i, i);
        }
        x = new_x;
        iterations++;
        error = (A * x - b).norm();
        error_history.push_back(error);
        if (error > error_threshold) {
            finished = false;
            break;
        }
    }
    auto end_time = std::chrono::high_resolution_clock::now();
    double total_time = std::chrono::duration<double>(end_time - start_time).count();
    return SolverResult(x, error, error_history, iterations, total_time, finished);
}


SolverResult solveGaussSeidel(Matrix& A, Matrix& b, double precision, double error_threshold) {
    validateMatrices(A, b);

    // https://en.wikipedia.org/wiki/Gauss%E2%80%93Seidel_method#Algorithm
    int n = A.shape.first;

    Matrix x(n, 1);
    double error = INFINITY;
    std::vector<double> error_history;
    int iterations = 0;
    bool finished = true;

    auto start_time = std::chrono::high_resolution_clock::now();
    while (error > precision) {
        Matrix new_x = Matrix(n, 1);
        for (int i = 0; i < n; i++) {
            double sum1 = 0;
            for (int j = 0; j < i; j++) {
                sum1 += A(i, j) * new_x(j, 0);
            }
            double sum2 = 0;
            for (int j = i + 1; j < n; j++) {
                sum2 += A(i, j) * x(j, 0);
            }
            new_x(i, 0) = (b(i, 0) - sum1 - sum2) / A(i, i);
        }
        x = new_x;
        iterations++;
        error = (A * x - b).norm();
        error_history.push_back(error);
        if (error > error_threshold) {
            finished = false;
            break;
        }
    }
    auto end_time = std::chrono::high_resolution_clock::now();
    double total_time = std::chrono::duration<double>(end_time - start_time).count();
    return SolverResult(x, error, error_history, iterations, total_time, finished);
}


std::pair<Matrix, Matrix> luDecomposition(Matrix& A) {
    if (A.shape.first != A.shape.second) {
        throw std::invalid_argument("Matrix A must be square");
    }

    // https://en.wikipedia.org/wiki/LU_decomposition#C_code_example
    int n = A.shape.first;
    Matrix L(n, n);
    Matrix U(n, n);

    for (int i = 0; i < n; i++) {
        L(i, i) = 1;
    }

    for (int i = 0; i < n; i++) {
        for (int j = i; j < n; j++) {
            double sum = 0;
            for (int k = 0; k < i; k++) {
                sum += L(i, k) * U(k, j);
            }
            U(i, j) = A(i, j) - sum;
        }

        for (int j = i; j < n; j++) {
            double sum = 0;
            for (int k = 0; k < i; k++) {
                sum += L(j, k) * U(k, i);
            }
            L(j, i) = (A(j, i) - sum) / U(i, i);
        }
    }

    return std::make_pair(L, U);
}

SolverResult solveLU(Matrix& A, Matrix& b) {
    validateMatrices(A, b);

    auto start_time = std::chrono::high_resolution_clock::now();
    std::pair<Matrix, Matrix> lu = luDecomposition(A);
    Matrix L = lu.first;
    Matrix U = lu.second;

    // https://en.wikipedia.org/wiki/LU_decomposition#Solving_linear_equations
    int n = A.shape.first;

    Matrix y(n, 1);
    for (int i = 0; i < n; i++) {
        double sum = 0;
        for (int j = 0; j < i; j++) {
            sum += L(i, j) * y(j, 0);
        }
        y(i, 0) = (b(i, 0) - sum) / L(i, i);
    }

    Matrix x(n, 1);
    for (int i = n - 1; i >= 0; i--) {
        double sum = 0;
        for (int j = i + 1; j < n; j++) {
            sum += U(i, j) * x(j, 0);
        }
        x(i, 0) = (y(i, 0) - sum) / U(i, i);
    }
    auto end_time = std::chrono::high_resolution_clock::now();
    double total_time = std::chrono::duration<double>(end_time - start_time).count();
    return SolverResult(x, (A * x - b).norm(), {}, 1, total_time, true);
}