import numpy as np


class Graph:
    def __init__(self, n, seed=None):
        """
        Initialize the graph with the number of agents
        """
        self.n = n
        self.rng = np.random.default_rng(seed)

    def erdos_renyi_adj(self, p) -> np.ndarray:
        """
        Generates an adjacency matrix from an Erdos-Renyi
        graph G of size n with edge probability p
        """
        random_matrix = self.rng.random((self.n, self.n))
        A = (random_matrix < p).astype(int)
        A = np.triu(A, 1)
        A = A + A.T

        return A

    @staticmethod
    def make_laplacian(A) -> np.ndarray:
        """
        Makes a graph Laplacian matrix L from an adjacency matrix A
        """
        D = np.diag(A.sum(axis=1))
        L = D - A
        return L

    @staticmethod
    def make_setpoint_transform_2D(L, alpha, beta, p_track) -> np.ndarray:
        """
        Takes a graph Laplacian L and 2D setpoint p.

        Computes a transform matrix B and offset vector c from the stack of
        all positions resulting from consensus with neighbors and setpoint
        attraction

        pdot = Bp + c , p = [(x1,y1), ...., (xn, yn)]
        """
        N = L.shape[0]
        I2 = np.eye(2)
        IN = np.eye(N)
        ones_N = np.ones(N)

        B = -alpha*np.kron(L, I2) - beta*np.kron(IN, I2)
        c = beta*np.kron(p_track, ones_N)

        return B, c

    @staticmethod
    def make_setpoint_formation_transform_2D(L, alpha, beta, p_track, formation_offsets) -> np.ndarray:
        """
        Takes a graph Laplacian L and 2D setpoint p.

        Computes a transform matrix B and offset vector c from the stack of
        all positions resulting from consensus with neighbors, setpoint attraction,
        and formation positioning

        pdot = Bp + c , p = [(x1,y1), ...., (xn, yn)]
        """
        N = L.shape[0]
        I2 = np.eye(2)
        IN = np.eye(N)
        ones_N = np.ones(N)

        B = -alpha*np.kron(L, I2) - beta*np.kron(IN, I2)
        D = formation_offsets.flatten()
        c = alpha*np.kron(L, I2) @ D + beta*np.kron(p_track, ones_N)

        return B, c

    @staticmethod
    def make_circle_formation_transform_2D(L, alpha, beta, p_track, formation_offsets) -> np.ndarray:
        """
        Takes a graph Laplacian L and 2D setpoint p.

        Computes a transform matrix B and offset vector c from the stack of
        all positions resulting from consensus with neighbors, setpoint attraction,
        and formation positioning

        pdot = Bp + c , p = [(x1,y1), ...., (xn, yn)]
        """
        N = L.shape[0]
        I2 = np.eye(2)
        IN = np.eye(N)

        B = -alpha*np.kron(L, I2) - beta*np.kron(IN, I2)
        D = formation_offsets.flatten()
        c = alpha*np.kron(L, I2) @ D + beta*p_track

        return B, c
