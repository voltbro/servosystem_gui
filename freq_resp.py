import numpy as np
from motor_dynamics import MotorDynamics
import matplotlib.pyplot as plt
from scipy.signal import correlate

class FreqResponce():
    def __init__(self, ts) -> None:
        self.ts = ts

        self.model_J = 1.0
        self.model_B = 1.0
        self.model_k = 1.0

        self.sin_A = 1.0
        self.sin_f = 1.0
        self.sin_phi = 0.0

        self.t = 0.0

        self.mot = MotorDynamics(ts=self.ts,
                            J=self.model_J,
                            B=self.model_B,
                            k=self.model_k,
                            )

    def gen_sin(self, A, f, phi, t):
        return A * np.sin(f * t + phi)

    def set_sin_params(self, A=1.0, f=1.0, phi=0.0):
        self.sin_A = A
        self.sin_f = f*(2*np.pi)
        self.sin_phi = phi

    def set_model_params(self, J=1.0, B=1.0, k=1.0):
        self.model_J = J
        self.model_B = B
        self.model_k = k
        self.mot.set_identification_params(J, B, k)

    def reset(self):
        self.t = 0.0
        self.mot.reset_x()

    def step_sin_model(self):
        u = self.gen_sin(self.sin_A, self.sin_f, self.sin_phi, self.t)
        self.t += self.ts
        y = self.mot.step_openloop(u)
        return u, y, self.t
    
    def calc_point_model(self, omega, J, B, k):
        A = 1/np.sqrt((-J * omega**2 + k)**2 + (B * omega)**2)
        psi = np.arctan2(B*omega, J * omega**2 - k) - np.pi
        return A, psi
    
    def calc_point_real(self, sig1, sig2, t, period):
        # correct t
        t0 = t[0]
        for i in range(len(t)):
            t[i] -= t0
        # print(t[-1])
        # print(len(t))
        # get phase shift
        xcorr = correlate(sig1, sig2)
        dt = np.linspace(-t[-1], t[-1], 2*len(t)-1)
        recovered_time_shift = dt[xcorr.argmax()]
        recovered_phase_shift = 2*np.pi*recovered_time_shift/period
        
        # get amplitude ratio
        # get real amplitude of sig2
        points_num=len(t)
        fft_freq = np.fft.fftfreq(points_num-1, t[1]-t[0])   # assume uniform spacing
        fft_result=np.fft.fft(sig2)
        #Remove negative frequencies
        for i in range(len(fft_freq)):
            if fft_freq[i]<0:
                fft_result[i]=0
        ampl=np.abs(fft_result)/points_num*2
        max_index=np.argmax(ampl)
        sig2_amplitude=ampl[max_index]
        amp_ratio = sig2_amplitude/self.sin_A

        return amp_ratio, recovered_phase_shift

    def freq_resp_model(self):
        omega_lst = np.arange(0.1, 35.0, 0.1)
        A_lst = []
        psi_lst = []
        for omega in omega_lst:
            # A.append(1/np.sqrt((-self.model_J * omega**2 + self.model_k)**2 + (self.model_B * omega)**2))
            # psi.append(np.arctan2(self.model_B*omega, self.model_J * omega**2 - self.model_k) - np.pi)
            A, psi = self.calc_point_model(omega, self.model_J, self.model_B, self.model_k)
            A_lst.append(A)
            psi_lst.append(psi)
        return A_lst, psi_lst, omega_lst.tolist()

    

if __name__ == "__main__":
    ts = 1/200

    J = 1.0
    B = 1.0
    k = 1.0

    A = 1.0
    f = 1.0
    phi = 0.0

    fr = FreqResponce(ts)
    fr.set_model_params(J, B, k)
    fr.set_sin_params(A, f, phi)

    amp, phase, omega = fr.freq_resp_model()

    plt.subplot(2, 1, 1)
    plt.plot(omega, amp, color='blue',linewidth=2)
    plt.grid()
    plt.title("Amplitude")
    # plt.show() 
    plt.subplot(2, 1, 2)
    plt.plot(omega, phase, color='blue',linewidth=2)
    plt.grid()
    plt.title("Phase Lag")
    plt.show() 

    t = 0.0
    t_vec = []
    u_vec = []
    y_vec = []
    while t < 50.0:
        u, y, t = fr.step_sin_model()

        t_vec.append(t)
        y_vec.append(y)
        u_vec.append(u)


    plt.plot(t_vec, y_vec, color='blue',linewidth=2)
    plt.plot(t_vec, u_vec, color='black',linewidth=2)
    plt.grid()
    plt.show() 
