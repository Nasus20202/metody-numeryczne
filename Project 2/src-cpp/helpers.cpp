#include <cmath>
#include "matrix.h"

Matrix generateAMatrix(int N, int a1, int a2, int a3) {
    Matrix A(N, N);
    for (int i = 0; i < N; i++) {
        A[i][i] = a1;
    }
    for (int i = 0; i < N - 1; i++) {
        A[i][i + 1] = a2;
        A[i + 1][i] = a2;
    }
    for (int i = 0; i < N - 2; i++) {
        A[i][i + 2] = a3;
        A[i + 2][i] = a3;
    }
    return A;
}

Matrix generateBVector(int N, int f) {
    Matrix b(N, 1);
    for (int i = 0; i < N; i++) {
        b[i][0] = std::sin((i + 1) * (f + 1));
    }
    return b;
}

