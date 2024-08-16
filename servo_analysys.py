import numpy as np
import matplotlib.pyplot as plt

class ServoAnalysys:
    def __init__(self, 
                 J=1.0,
                 B=1.0,
                 delta=1.0,
                 alpha=0.787
                 ) -> None:
        self.J = J
        self.B = B
        self.delta = delta
        self.alpha = alpha

    def set_model_params(self, J=1.0, B=1.0):
        self.J = J
        self.B = B

    def set_root_params(self, delta=1.0, alpha=0.787):
        self.delta = delta
        self.alpha = alpha

    def calc_kxkv(self, lambda1 : complex, lambda2 : complex):
        kx = self.J * lambda1 * lambda2
        kv = -self.B - self.J * (lambda1 + lambda2)
        return kx.real, kv.real

    def calc_lambda(self, kx, kv):
        kx = complex(kx)
        kv = complex(kv)
        D = np.sqrt((self.B + kv)**2 - 4 * self.J * kx)
        lambda1 = (-(self.B + kv) + D)/(2*self.J)
        lambda2 = (-(self.B + kv) - D)/(2*self.J)
        return lambda1, lambda2

    def calc_k_curves(self, range, step):
        # curve 1
        kv1 = np.arange(0.0, range, step)
        kx1 = -self.J*self.delta**2 + self.B*self.delta + kv1*self.delta

        # curve 2
        tg2a = np.tan(self.alpha)**2
        kv2 = np.arange(0.0, range, step)
        kx2 = (1/(4*self.J)) * (1 + tg2a) * kv2**2 + \
                kv2*(self.B + (self.B - 2*self.J*self.delta) * tg2a)/(2*self.J) + \
                (self.B**2 + (self.B - 2*self.J*self.delta)**2 * tg2a)/(4*self.J)

        # curve 3
        l = np.arange(-range, 0.0, step)
        kx3 = self.J * l**2
        kv3 = -self.B - 2*self.J*l
        return [kx1, kv1], [kx2, kv2], [kx3, kv3]
    

if __name__ == "__main__":
    J = 1.0
    B = 1.0
    delta = 1.0
    alpha = 0.787

    range = 5
    step = 0.1
    
    lambda1 = -2.0+3j
    lambda2 = -2.0-3j

    servo = ServoAnalysys()
    servo.set_model_params(J, B)
    servo.set_root_params(delta, alpha)

    kx, kv = servo.calc_kxkv(lambda1, lambda2)
    print(f"kx: {kx} | kv {kv}")
    lambda1_, lambda2_ = servo.calc_lambda(kx, kv)
    print(f"lambda1: {lambda1} | lambda2: {lambda2}")

    k1, k2, k3 = servo.calc_k_curves(range, step)
    
    plt.plot(k1[0], k1[1], color='blue',linewidth=2)
    plt.plot(k2[0], k2[1], color='red',linewidth=2)
    plt.plot(k3[0], k3[1], color='black',linewidth=2)
    plt.grid()
    plt.show()
    



