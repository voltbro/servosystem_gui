import numpy as np

class SignalGenerator():
    def __init__(self, ts=0.005, A=1.0, freq=1.0) -> None:
        self.A = A
        self.freq = freq
        self.ts = ts
        self.t = -self.ts

    def set_params(self, A=1.0, freq=1.0):
        self.A = A
        self.freq = freq

    def reset(self):
        self.t = -self.ts

    def gen_sin(self):
        self.t += self.ts
        sig = self.A * np.sin(self.freq * 2 * np.pi * self.t)
        # print(f"{sig:.2f}, {self.t:.2f}")
        return sig, self.t

    def gen_square(self):
        self.t += self.ts
        sig = self.A * np.sign(np.sin(self.freq * 2 * np.pi * self.t))
        return sig, self.t

    def gen_triangle(self):
        self.t += self.ts
        sig = self.A - (2*self.A/np.pi) * np.arccos((np.cos(2*np.pi*self.freq*self.t - np.pi/2)))
        return sig, self.t