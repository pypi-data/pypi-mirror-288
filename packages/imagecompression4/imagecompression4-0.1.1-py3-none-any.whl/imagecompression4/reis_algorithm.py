import numpy as np
from .matrix_operations import matrix_multiply, schur_decomposition, solve_sylvester_equation

def reis_algorithm(A, P, epsilon):
    n = A.shape[0]
    P1 = P[:, :n//2]
    P2 = P[:, n//2:]
    
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
        
        for j in range(1, T.shape[0]):
            X = solve_sylvester_equation(A22 - T[j, j]*np.eye(A22.shape[0]), T[j, j]*np.eye(T.shape[0]), -Ahat21[:, j].reshape(-1, 1))
            Rk[:, j] = X.squeeze()
        
        rk = A21 - matrix_multiply(Rk, A12)
        k += 1
    
    return Rk