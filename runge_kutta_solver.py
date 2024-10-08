import numpy as np
import matplotlib.pyplot as plt
import control as ct

class RungeKuttaSolver():
    def __init__(self, A, B, C, ts) -> None:
        self.A = A
        self.B = B
        self.C = C
        self.h = ts

    def set_params(self, A, B, C, ts):
        self.A = A
        self.B = B
        self.C = C
        self.h = ts

    def step(self, x, u):
        # print(u[1])
        Bu = np.matmul(self.B, u)
        k1 = np.matmul(self.A, x) + Bu
        k2 = np.matmul(self.A, (x+k1*self.h/2)) + Bu
        k3 = np.matmul(self.A, (x+k2*self.h/2)) + Bu
        k4 = np.matmul(self.A, (x+k3*self.h)) + Bu
        x_ = x + self.h*(k1 + 2*k2 + 2*k3 + k4)/6
        # y = np.matmul(self.C, x_)
        return x_