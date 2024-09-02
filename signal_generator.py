import numpy as np

class SignalGenerator():
    def __init__(self, ts=0.005, A=1.0, freq=1.0) -> None:
        self.A = A
        self.freq = freq
        self.T = 1/freq
        self.ts = ts
        self.t = -self.ts

    def set_params(self, A=1.0, freq=1.0):
        self.A = A
        self.freq = freq
        self.T = 1/freq

    def reset(self):
        self.t = -self.ts

    def gen_sin(self):
        self.t += self.ts
        sig = self.A * np.sin(self.freq * 2 * np.pi * self.t)
        d_sig = 2 * np.pi * self.freq * self.A * np.cos(self.freq * 2 * np.pi * self.t)
        # print(f"{sig:.2f}, {self.t:.2f}")
        return sig, self.t, d_sig

    def gen_square(self):
        self.t += self.ts
        sig = self.A * np.sign(np.sin(self.freq * 2 * np.pi * self.t))
        d_sig = 0.0
        return sig, self.t, d_sig

    def gen_triangle(self):
        self.t += self.ts
        sig = self.A - (2*self.A/np.pi) * np.arccos((np.cos(2*np.pi*self.freq*self.t - np.pi/2)))
        
        if (self.t%self.T < self.T/4 or self.t%self.T >= 3*self.T/4):
            d_sig = 4 * self.A * self.freq
        elif self.T/4 <= self.t%self.T < 3*self.T/4:
            d_sig = -4 * self.A * self.freq

        return sig, self.t, d_sig