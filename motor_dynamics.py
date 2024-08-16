import numpy as np
import control as ct
import matplotlib.pyplot as plt


class MotorDynamics():
    def __init__(self, 
                 ts=0.005, 
                 J=1.0, 
                 B=1.0, 
                 k=1.0, 
                 kx=1.0, 
                 kv=1.0) -> None:
        self.ts = ts

        self.J = J
        self.B = B

        self.k = k
        self.kx = kx
        self.kv = kv

        self.x = np.array([0, 0])

        self.__update_model()

    def set_identification_params(self, J, B, k):
        self.J = J
        self.B = B
        self.k = k
        self.__update_model()

    def set_servo_params(self, kx, kv):
        self.kx = kx
        self.kv = kv

    def __update_model(self):
        num = [100]
        den = [self.J, self.B, self.k]

        W = ct.tf(num, den)
        sys = ct.ss(W)
        dsys = ct.c2d(sys, self.ts)
        self.A = dsys.A
        self.B = dsys.B
        self.C = dsys.C

    def reset_x(self):
        self.x = np.array([0, 0])

    def step_openloop(self, u):
        u = np.array([u])
        self.x = np.matmul(self.A, self.x) + np.matmul(self.B, u)
        # self.y = np.matmul(self.C, self.x)
        # self.x = self.x_
        return self.x[1]#, self.x[0]

    def step_closedloop(self, ref):
        x_ref = np.array([0.0, ref])
        K = np.array([self.kv, self.kx])
        e = x_ref-self.x
        u = np.matmul(K, e)
        y = self.step_openloop(u)
        return y
    

if __name__ == "__main__":
    J = 0.2
    B = 1.0
    k = 0.0
    kx = 16.0
    kv = 0.0
    ts = 0.005

    t = -ts
    y_vec = []
    y1_vec = []
    ref_vec = []
    t_vec = []

    model = MotorDynamics(ts=ts,
                          J=J,
                          B=B,
                          k=k,
                          kx=kx,
                          kv=kv)
    model.reset_x()

    for i in range(2000):
        t += ts
        # u = 2 * np.sin(2*np.pi*t)
        if i% 1000:
            ref = 1.0
        y = model.step_closedloop(ref)

        t_vec.append(t)
        y_vec.append(y)
        # y1_vec.append(y1)
        ref_vec.append(ref)

    plt.plot(t_vec, y_vec, color='blue',linewidth=2)
    # plt.plot(t_vec, y1_vec, color='green',linewidth=2)
    plt.plot(t_vec, ref_vec, color='black',linewidth=2)
    plt.grid()
    plt.show()



