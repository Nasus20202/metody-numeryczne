#include "matrix.h"
#include "helpers.h"
#include "solvers.h"
#include <iostream>

using namespace std;

void printResult(string name, SolverResult& result) {
    cout << name << ": Time elapsed: " << result.time << "s, Iterations: " << result.iterations << ", Error: " << result.error << " Finished: " << (result.finished ? "True" : "False") << endl;
    //cout << result.time << endl;
}

void testSolvers(Matrix& A, Matrix& b) {
    SolverResult jacobiResult = solveJacobi(A, b);
    printResult("Jacobi method", jacobiResult);

    SolverResult gaussSeidelResult = solveGaussSeidel(A, b);
    printResult("Gauss-Seidel method", gaussSeidelResult);

    SolverResult luResult = solveLU(A, b);
    printResult("LU Decomposition", luResult);
}

int main() {
    int N = 928;

    // A
    Matrix a = generateAMatrix(N, 8, -1, -1);
    Matrix b = generateBVector(N, 3);

    cout << "First linear system:" << endl;
    testSolvers(a, b);
    cout << endl;
    // C

    a = generateAMatrix(N, 3, -1, -1);
    cout << "Second linear system:" << endl;
    testSolvers(a, b);
    cout << endl;

    // time comparison
    vector<int> test_sizes = {100, 500, 1000, 1500, 2000, 2500, 3000};
    for (int N : test_sizes) {
        cout << "N = " << N << endl;
        a = generateAMatrix(N, 8, -1, -1);
        b = generateBVector(N, 3);
        testSolvers(a, b);
        cout << endl;
    }
}