import numpy as np
from scipy.linalg import schur, solve_sylvester
from skimage.color import rgb2gray
from concurrent.futures import ThreadPoolExecutor

def compute_A_tilde(A, P1, R):
    s = P1.shape[1]
    A11 = A[:s, :s]
    A12 = A[:s, s:]
    A21 = A[s:, :s]
    A11_tilde = A11 + A12 @ R
    A_tilde = P1 @ A11_tilde @ P1.T
    return A_tilde, A11_tilde

def solve_sylvester_parallel(A22, Z, A_hat_21, Q_T):
    with ThreadPoolExecutor() as executor:
        future = executor.submit(solve_sylvester, A22 - Z, -A_hat_21, Q_T)
        X = future.result()
    return X

def algorithm_1(A, P, epsilon):
    n, m = A.shape
    s = P.shape[1]
    P1 = P[:, :s]
    
    A11 = A[:s, :s]
    A12 = A[:s, s:]
    A21 = A[s:, :s]
    A22 = A[s:, s:]
    k = 0
    Rk = np.zeros((s, s))
    rk = A21
    
    while np.linalg.norm(rk) >= epsilon:
        A11_tilde = A11 + A12 @ Rk
        Q, Z = schur(A11_tilde)
        A_hat_21 = (A21 + Rk @ A12 @ Rk) @ Q
        X = solve_sylvester_parallel(A22, Z, A_hat_21, Q.T)
        Rk = Rk + X @ Q.T
        rk = A21 + Rk @ A12
    
    A_tilde, A11_tilde = compute_A_tilde(A, P1, Rk)
    
    return Rk, A_tilde

def compress_image(image, epsilon=1e-6):
    image_gray = rgb2gray(image) if image.ndim == 3 else image
    n, m = image_gray.shape
    s = min(n, m) // 2
    A = image_gray[:2*s, :2*s]
    
    P = np.random.rand(2*s, s)
    
    R, A_tilde = algorithm_1(A, P, epsilon)
    
    compressed_image = A_tilde.reshape((2*s, 2*s))
    
    return compressed_image
