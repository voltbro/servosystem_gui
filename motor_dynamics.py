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
        self.y = np.array([0, 0])
        self.pre_e = 0

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
        num = [1]
        den = [self.J, self.B, self.k]
        # den = [0.03, 0.7, 0.0]

        W = ct.tf(num, den)
        # print(W)
        # y,t = ct.step_response(W)
        # plt.plot(t,y)
        # plt.xlabel('Time')
        # plt.title('Response of a Second Order System')
        sys = ct.tf2ss(W)
        dsys = ct.c2d(sys, self.ts, 'foh')
        self.AA = dsys.A
        self.BB = dsys.B
        self.CC = dsys.C
        # print(self.BB)
        
        
        # self.AA = np.array([[0.8899,   0.0],
        #                     [0.004719, 1.0]])
        # self.BB = np.array([[0.03564], [0.000187]])
        # self.CC = np.array([0.0, 4.167])

    def reset_x(self):
        self.x = np.array([0, 0])

    def step_openloop(self, u):
        u = np.array([u])
        self.x_ = np.matmul(self.AA, self.x) + np.matmul(self.BB, u)
        self.y = np.matmul(self.CC, self.x)
        self.x = self.x_
        # print(self.x[1][0])
        return self.y[0]#self.x[1]#, self.x[0]

    def step_closedloop(self, ref):
        # x_ref = np.array([0.0, ref])
        # K = np.array([self.kv, self.kx])
        
        # e = x_ref-self.y[0]
        # u = np.matmul(K, e)
        e = ref-self.y[0]
        de = (e - self.pre_e)/self.ts
        u = self.kx*e + self.kv*de
        u = np.clip(u, -12, 12)
        y = self.step_openloop(u)
        self.pre_e = e
        # print(y)
        return y
    

if __name__ == "__main__":
    J = 0.03
    B = 0.7
    k = 0.0
    kx = 16.01
    kv = 0.0
    ts = 0.005

    t = -ts
    y_vec = []
    y1_vec = []
    ref_vec = []
    t_vec = []

    ref = 1.0

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



