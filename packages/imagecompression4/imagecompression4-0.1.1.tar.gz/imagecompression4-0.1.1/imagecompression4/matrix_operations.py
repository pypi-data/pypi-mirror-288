import numpy as np
from scipy.linalg import schur, solve_sylvester

def matrix_multiply(A, B):
    return np.dot(A, B)

def schur_decomposition(A):
    T, Z = schur(A, output='real')
    return T, Z

def solve_sylvester_equation(A, B, C):
    return solve_sylvester(A, B, C)