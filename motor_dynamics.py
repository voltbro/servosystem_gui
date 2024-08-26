import numpy as np
import control as ct
import matplotlib.pyplot as plt

from runge_kutta_solver import RungeKuttaSolver

OPEN = 0
CLOSE = 1

class MotorDynamics():
    def __init__(self, 
                 model_type=0, # 0 - openloop, 1 - closedloop
                 ts=0.005, 
                 J=1.0, 
                 B=1.0, 
                 k=1.0, 
                 kx=1.0, 
                 kv=1.0) -> None:
        self.ts = ts
        self.model_type = model_type

        self.J = J
        self.B = B

        self.k = k
        self.kx = kx
        self.kv = kv

        self.x = np.array([0, 0])
        self.y = np.array([0, 0])
        self.pre_e = 0

        self.__update_model()

        self.ode4 = RungeKuttaSolver(A=self.AA, B=self.BB, C=self.CC, ts=self.ts)

    def set_identification_params(self, J, B, k):
        self.J = J
        self.B = B
        self.k = k
        self.__update_model()
        self.ode4.set_params(A=self.AA, B=self.BB, C=self.CC, ts=self.ts)

    def set_servo_params(self, kx, kv):
        self.kx = kx
        self.kv = kv
        self.__update_model()
        self.ode4.set_params(A=self.AA, B=self.BB, C=self.CC, ts=self.ts)

    def __update_model(self):
        if self.model_type == OPEN:
            num = [1]
            den = [self.J, self.B, self.k]
        else:
            num = [self.kv, self.kx]
            den = [self.J, self.B+self.kv, self.kx]

        W = ct.tf(num, den)
        sys = ct.tf2ss(W)
        # dsys = ct.c2d(sys, self.ts, 'foh')
        self.AA = sys.A
        self.BB = sys.B
        self.CC = sys.C

    def reset_x(self):
        self.x = np.array([0, 0])
        self.y = np.array([0, 0])
        self.pre_e = 0

    def step(self, u):
        u = np.array([u])
        # self.x_ = np.matmul(self.AA, self.x) + np.matmul(self.BB, u)
        # self.y = np.matmul(self.CC, self.x)
        # self.x = self.x_
        # print(self.x[1][0])
        self.x_ = self.ode4.step(self.x, u)
        self.y = np.matmul(self.CC, self.x_)
        self.x = self.x_
        return self.y[0]#self.x[1]#, self.x[0]

    # def step_closedloop(self, ref):
        # # x_ref = np.array([0.0, ref])
        # # K = np.array([self.kv, self.kx])
        
        # # e = x_ref-self.y[0]
        # # u = np.matmul(K, e)
        # e = ref-self.y[0]
        # de = (e - self.pre_e)/self.ts
        # u = self.kx*e + self.kv*de
        # # u = np.clip(u, -12, 12)
        # y = self.step_openloop(u)
        # self.pre_e = e
        # # print(y)
        # return y

    

if __name__ == "__main__":
    J = 0.09
    B = 1.85
    k = 1.0
    kx = 3.52
    kv = -1.84
    ts = 0.005

    t = -ts
    y_vec = []
    y1_vec = []
    ref_vec = []
    t_vec = []

    ref = 1.0

    model = MotorDynamics(model_type=OPEN,
                          ts=ts,
                          J=J,
                          B=B,
                          k=k,
                          kx=kx,
                          kv=kv)
    model.reset_x()

    while t < 100.0:
        t += ts
        ref = 2 * np.sin(0.1*np.pi*t)
        # if i% 1000:
        #     ref = 1.0
        y = model.step(ref)
        # y =  model.step_openloop(ref)

        t_vec.append(t)
        y_vec.append(y)
        # y1_vec.append(y1)
        ref_vec.append(ref)

    plt.plot(t_vec, y_vec, color='blue',linewidth=2)
    # plt.plot(t_vec, y1_vec, color='green',linewidth=2)
    plt.plot(t_vec, ref_vec, color='black',linewidth=2)
    plt.grid()
    plt.show()



