#include "matrix.h"
#include "helpers.h"
#include "solvers.h"
#include <iostream>

using namespace std;

void printResult(string name, SolverResult& result, bool minimalOutput = false) {
    if (minimalOutput) {
        cout << result.time << endl;
        return;
    }
    cout << name << ": Time elapsed: " << result.time << "s, Iterations: " << result.iterations << ", Error: " << result.error << " Finished: " << (result.finished ? "True" : "False") << endl;
}

void testSolvers(Matrix& A, Matrix& b, bool minimalOutput = false) {
    SolverResult jacobiResult = solveJacobi(A, b);
    printResult("Jacobi method", jacobiResult, minimalOutput);

    SolverResult gaussSeidelResult = solveGaussSeidel(A, b);
    printResult("Gauss-Seidel method", gaussSeidelResult, minimalOutput);

    SolverResult luResult = solveLU(A, b);
    printResult("LU Decomposition", luResult, minimalOutput);
}

int main(int argc, char** argv) {
    bool minimalOutput = argc > 1;
    int N = 928;

    // A
    Matrix a = generateAMatrix(N, 8, -1, -1);
    Matrix b = generateBVector(N, 3);

    cout << "First linear system:" << endl;
    testSolvers(a, b, minimalOutput);
    cout << endl;

    a = generateAMatrix(N, 3, -1, -1);
    cout << "Second linear system:" << endl;
    testSolvers(a, b, minimalOutput);
    cout << endl;

    // time comparison
    vector<int> test_sizes = {100, 500, 1000, 1500, 2000, 2500, 3000};
    for (int N : test_sizes) {
        cout << "N = " << N << endl;
        a = generateAMatrix(N, 8, -1, -1);
        b = generateBVector(N, 3);
        testSolvers(a, b, minimalOutput);
        cout << endl;
    }
}