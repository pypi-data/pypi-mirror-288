import numpy as np
from scipy.linalg import schur, solve_sylvester

def matrix_multiply(A, B):
    return np.dot(A, B)

def schur_decomposition(A):
    T, Z = schur(A)
    return T, Z

def solve_sylvester_equation(A, B, C):
    X = solve_sylvester(A, B, C)
    return X

def reis_algorithm(A, P, epsilon):
    n = A.shape[0]
    half_n = n // 2
    P1 = P[:, :half_n]
    P2 = P[:, half_n:]

    A11 = matrix_multiply(matrix_multiply(P1.T, A), P1)
    A12 = matrix_multiply(matrix_multiply(P1.T, A), P2)
    A21 = matrix_multiply(matrix_multiply(P2.T, A), P1)

    k = 0
    Rk = np.zeros_like(A21)
    rk = A21

    while np.linalg.norm(rk) >= epsilon:
        A22 = matrix_multiply(matrix_multiply(P2.T, A), P2)
        Atilde11 = A11 + matrix_multiply(A12, Rk)
        T, Q = schur_decomposition(Atilde11)

        Ahat21 = matrix_multiply(A21 + matrix_multiply(matrix_multiply(Rk, A12), Rk), Q)

        for j in range(T.shape[0]):
            C = -Ahat21[:, j].reshape(-1, 1)
            X = solve_sylvester_equation(A22, T[j, j] * np.eye(A22.shape[0]), C)
            Rk[:, j] = X.flatten()

        rk = A21 - matrix_multiply(Rk, A12)
        k += 1

    return Rk
