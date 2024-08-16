#!/home/yoggi/Labs/dc_motor/.venv/bin/python3
import numpy as np
import pyqtgraph as pg
import time
import threading

import sys
from PyQt5 import QtWidgets, uic
from PyQt5.QtCore import Qt, QTimer
from forms.servo_form import Ui_Form
from ident_window import IdentWidget
from PyQt5.QtWidgets import QPushButton, QHBoxLayout, QVBoxLayout, QSpacerItem, QSizePolicy

from plot_widget import PlotWidget
from servo_analysys import ServoAnalysys
from signal_generator import SignalGenerator
from motor_dynamics import MotorDynamics
from device import Device

X_ROOT_RANGE = 12.0
Y_ROOT_RANGE = 11.5
X_K_RANGE = 21
Y_K_RANGE = 12
X_RESP_RANGE = 10
Y_RESP_RANGE = 5
STEP_DELTA = 0.05

DELTA = 1
ALPHA = np.pi/4
K_RANGE = 40

class ServoWidget(QtWidgets.QWidget, Ui_Form):
    def __init__(self, *args, obj=None, **kwargs):
        super().__init__(*args, **kwargs)
        self.setupUi(self)
        self.resize(2048, 1536)

        self.servo = ServoAnalysys()
        self.servo.set_root_params(DELTA, ALPHA)

        self.model_J = 0.2
        self.model_B = 1.0
        self.sig_A = 1.0
        self.sig_freq = 1.0
        self.t = 0
        self.sig_rate = 200
        self.draw_rate = 100
        self.ts = 1/self.sig_rate
        self.sig_gen = SignalGenerator(ts=self.ts, A=self.sig_A, freq=self.sig_freq)
        self.model = MotorDynamics(ts=self.ts,
                            J=self.model_J,
                            B=self.model_B,
                            k=0.0,
                            )
        self.device = Device()

        self.ref_plot_vec = []
        self.real_plot_vec = []
        self.ref_sig = 0.0
        self.real_sig = 0.0

        self.im_x_line = [0, 0]
        self.im_y_line = [50, -50]
        self.re_x_line = [-50, 50]
        self.re_y_line = [0, 0]
        self.root_pos_re = []
        self.root_pos_im = []

        self.lambda1 = complex(-DELTA, 0)
        self.lambda2 = complex(-DELTA, 0)
        self.kx, self.kv = self.servo.calc_kxkv(self.lambda1, self.lambda2)

        self.startModel_toggled = False
        self.startDevice_toggled = False
        self.stop_gen_sig = False
        self.sig_vec = [[],[],[]]
        self.sig_type = "sine"
        
        self.init_root_locus_plot()
        self.init_k_plot()
        self.init_resp_plot()
        self.splitter.setSizes([1000, 2000])
        self.kxLine.setText(f"{self.kx:.2f}")
        self.kvLine.setText(f"{self.kv:.2f}")
        self.l1Line.setText(f"{self.lambda1}")
        self.l2Line.setText(f"{self.lambda2}")
        self.aLine.setText(f"{self.sig_A}")
        self.freqLine.setText(f"{self.sig_freq}")

        self.calcKBtn.clicked.connect(self.calcKBtn_clicked)
        self.calcLambdaBtn.clicked.connect(self.calcLambdaBtn_clicked)
        self.startModelBtn.clicked.connect(self.startModelBtn_clicked)
        self.startDeviceBtn.clicked.connect(self.startDeviceBtn_clicked)

        self.start = 0.0
        self.timer = QTimer()
        self.timer.setInterval(int(1000/self.draw_rate))
        self.timer.timeout.connect(self.update_resp_plot)
    
    def init_root_locus_plot(self):
        self.x_root_range = X_ROOT_RANGE
        self.y_root_range = Y_ROOT_RANGE
        self.root_plot_graph = PlotWidget()
        self.root_plot_graph.sigMouseClicked.connect(self.root_plot_clicked)
        self.leftLay.addWidget(self.root_plot_graph)
        self.root_plot_graph.setBackground("w")
        styles = {"color": "black", "font-size": "36px"}
        self.root_plot_graph.setLabel("left", "Im", **styles)
        self.root_plot_graph.setLabel("bottom", "Re", **styles)
        # self.root_plot_graph.addLegend()
        self.root_plot_graph.showGrid(x=True, y=True)
        self.root_plot_graph.setYRange(-self.y_root_range, self.y_root_range)
        self.root_plot_graph.setXRange(-self.x_root_range, 0.2)

        pen = pg.mkPen(None)
        pen_axis = pg.mkPen(color=(0, 0, 0), width=2)
        pen_field = pg.mkPen(color=(0, 0, 0), width=3)
        
        self.im_line = self.plot_line(self.root_plot_graph, "", self.im_x_line, self.im_y_line, pen_axis, "b", 0.0)
        self.re_line = self.plot_line(self.root_plot_graph, "", self.re_x_line, self.re_y_line, pen_axis, "b", 0.0)
        self.field_line = self.plot_line(self.root_plot_graph, "", [], [], pen_field, "b", 0.0)
        self.root_line = self.plot_line(self.root_plot_graph, "Roots", self.root_pos_re, self.root_pos_im, pen, "r", 20.0)
        self.draw_root_field(self.field_line, ALPHA, DELTA)

    def init_k_plot(self):
        self.x_k_range = X_K_RANGE
        self.y_k_range = Y_K_RANGE
        self.k_plot_graph = PlotWidget()
        self.k_plot_graph.sigMouseClicked.connect(self.k_plot_clicked)
        self.leftLay.addWidget(self.k_plot_graph)
        self.k_plot_graph.setBackground("w")
        styles = {"color": "black", "font-size": "36px"}
        self.k_plot_graph.setLabel("left", "k_v", **styles)
        self.k_plot_graph.setLabel("bottom", "k_x", **styles)
        # self.k_plot_graph.addLegend()
        self.k_plot_graph.showGrid(x=True, y=True)
        self.k_plot_graph.setYRange(0, self.y_k_range)
        self.k_plot_graph.setXRange(0, self.x_k_range)

        pen = pg.mkPen(None)
        pen_k = pg.mkPen(color=(0, 0, 0), width=3)

        self.root_pos_re = []
        self.k_line = self.plot_line(self.k_plot_graph, "1", [], [], pen_k, "r", 20.0)
        self.k1_line = self.plot_line(self.k_plot_graph, "1", self.root_pos_re, [], pen_k, "r", 0.0)
        self.k2_line = self.plot_line(self.k_plot_graph, "2", self.root_pos_re, [], pen_k, "g", 0.0)
        self.k3_line = self.plot_line(self.k_plot_graph, "3", self.root_pos_re, [], pen_k, "b", 0.0)
        self.draw_k_curves()

    def init_resp_plot(self):
        self.x_resp_range = X_RESP_RANGE
        self.y_resp_range = Y_RESP_RANGE
        self.resp_plot_graph = PlotWidget()
        self.resp_plot_graph.sigMouseClicked.connect(self.resp_plot_clicked)
        self.rightLay.addWidget(self.resp_plot_graph)
        self.resp_plot_graph.setBackground("w")
        styles = {"color": "black", "font-size": "36px"}
        self.resp_plot_graph.setLabel("left", "Angle [rad]", **styles)
        self.resp_plot_graph.setLabel("bottom", "Time [sec]", **styles)
        self.resp_plot_graph.addLegend()
        self.resp_plot_graph.showGrid(x=True, y=True)
        self.resp_plot_graph.setYRange(-self.y_resp_range, self.y_resp_range)
        self.resp_plot_graph.setXRange(-self.x_resp_range, 0.2)

        pen_ref = pg.mkPen(color=(0, 190, 0), width=3)
        pen_real = pg.mkPen(color=(0, 0, 190), width=3)

        self.time = []

        self.ref_line = self.plot_line(self.resp_plot_graph, "Ref", self.time, [], pen_ref, "r", 0.0)
        self.real_line = self.plot_line(self.resp_plot_graph, "Real", self.time, [], pen_real, "g", 0.0)

    def update_resp_plot(self):
        if self.t >= 0:
            self.time.append(self.t)
            # print(f"{self.t:.3f}  {len(self.time)}  {self.x_range * self.tim_rate}")
            # if len(self.time) > self.x_resp_range * self.draw_rate:
            while (self.time[-1] - self.time[0]) > self.x_resp_range:
                self.time = self.time[1:]
                self.ref_plot_vec = self.ref_plot_vec[1:]
                self.real_plot_vec = self.real_plot_vec[1:]
                self.resp_plot_graph.setXRange(self.time[0]-0.1, self.time[-1]+0.1)
            # print(f"{len(self.time)} | {self.time[0]:.2f} | {self.time[-1]:.2f}")
            
            # sin stuff
            self.ref_plot_vec.append(self.ref_sig)
            self.real_plot_vec.append(self.real_sig)
            self.ref_line.setData(self.time, self.ref_plot_vec)
            self.real_line.setData(self.time, self.real_plot_vec)
            
            # end = time.time() - self.start ## собственно время работы программы
            # print(end) ## вывод времени
            # self.start = time.time()

    def gen_sig(self):
        while self.stop_gen_sig == False:
            if self.startModel_toggled == True:
                if self.sig_type == "square":
                    self.ref_sig, self.t = self.sig_gen.gen_square()
                elif self.sig_type == "sine":
                    self.ref_sig, self.t = self.sig_gen.gen_sin()
                elif self.sig_type == "triangle":
                    self.ref_sig, self.t = self.sig_gen.gen_triangle()
                self.real_sig = self.model.step_closedloop(self.ref_sig)

            elif self.startDevice_toggled == True:
                self.ref_sig, self.real_sig, self.t = self.device.get_data()

            time.sleep(self.ts)
            # end = time.time() - self.start ## собственно время работы программы
            # print(end) ## вывод времени
            # self.start = time.time()

    def root_plot_clicked(self, e):
        mousePoint = self.root_plot_graph.getPlotItem().vb.mapSceneToView(e.pos())
        x = mousePoint.x()
        y = mousePoint.y()
        if np.abs(y) <= 0.15:
            y = 0.0

        if y == 0.0:
            self.root_pos_re = [x, x]
            self.root_pos_im = [0.0, 0.0]
            self.root_line.setData(self.root_pos_re, self.root_pos_im)
        else:
            self.root_pos_re = [x, x]
            self.root_pos_im = [y, -y]
            self.root_line.setData(self.root_pos_re, self.root_pos_im)
        
        # create lambdas
        self.lambda1 = complex(x, y)
        self.lambda2 = complex(x, -y)
        # calculate feedback constants
        self.kx, self.kv = self.servo.calc_kxkv(self.lambda1, self.lambda2)
        # show resultas in polots and linedits
        self.draw_k(self.kx, self.kv)
        self.l1Line.setText(f"{self.lambda1.real:.2f}{'+-'[int(self.lambda1.imag < 0)]}{np.abs(self.lambda1.imag):.2f}j")
        self.l2Line.setText(f"{self.lambda2.real:.2f}{'+-'[int(self.lambda2.imag < 0)]}{np.abs(self.lambda2.imag):.2f}j")
        self.kxLine.setText(f"{self.kx:.2f}")
        self.kvLine.setText(f"{self.kv:.2f}")

    def k_plot_clicked(self, e):
        mousePoint = self.k_plot_graph.getPlotItem().vb.mapSceneToView(e.pos())
        self.kx = mousePoint.x()
        self.kv = mousePoint.y()
        # print(f"X: {x:.2f} | Y: {y:.2f}")
        # self.k_line.setData([self.kx], [self.kv])

        # calculate lambdas
        self.lambda1, self.lambda2 = self.servo.calc_lambda(self.kx, self.kv)
        # show resultas in polots and linedits
        self.draw_k(self.kx, self.kv)
        self.root_pos_re = [self.lambda1.real, self.lambda2.real]
        self.root_pos_im = [self.lambda1.imag, self.lambda2.imag]
        self.root_line.setData(self.root_pos_re, self.root_pos_im)
        self.l1Line.setText(f"{self.lambda1.real:.2f}{'+-'[int(self.lambda1.imag < 0)]}{np.abs(self.lambda1.imag):.2f}j")
        self.l2Line.setText(f"{self.lambda2.real:.2f}{'+-'[int(self.lambda2.imag < 0)]}{np.abs(self.lambda2.imag):.2f}j")
        self.kxLine.setText(f"{self.kx:.2f}")
        self.kvLine.setText(f"{self.kv:.2f}")

    def resp_plot_clicked(self):
        pass

    def calcKBtn_clicked(self):
        try:
            self.lambda1 = complex(self.l1Line.text())
            self.lambda2 = complex(self.l2Line.text())
        
            self.kx, self.kv = self.servo.calc_kxkv(self.lambda1, self.lambda2)

            self.kxLine.setText(f"{self.kx:.2f}")
            self.kvLine.setText(f"{self.kv:.2f}")

            self.draw_k(self.kx, self.kv)
            
            self.root_pos_re = [self.lambda1.real, self.lambda2.real]
            self.root_pos_im = [self.lambda1.imag, self.lambda2.imag]
            self.root_line.setData(self.root_pos_re, self.root_pos_im)
        except ValueError:
            print("Wrong number in Line Edits! Correct and try again")

    def calcLambdaBtn_clicked(self):
        try:
            self.kx = float(self.kxLine.text())
            self.kv = float(self.kvLine.text())
        
            self.lambda1, self.lambda2 = self.servo.calc_lambda(self.kx, self.kv)

            self.l1Line.setText(f"{self.lambda1.real:.2f}{'+-'[int(self.lambda1.imag < 0)]}{np.abs(self.lambda1.imag):.2f}j")
            self.l2Line.setText(f"{self.lambda2.real:.2f}{'+-'[int(self.lambda2.imag < 0)]}{np.abs(self.lambda2.imag):.2f}j")

            self.draw_k(self.kx, self.kv)
            
            self.root_pos_re = [self.lambda1.real, self.lambda2.real]
            self.root_pos_im = [self.lambda1.imag, self.lambda2.imag]
            self.root_line.setData(self.root_pos_re, self.root_pos_im)
        except ValueError:
            print("Wrong number in Line Edits! Correct and try again")

    def startModelBtn_clicked(self):
        if self.startModel_toggled == False:
            self.stop_gen_sig = False
            self.startModel_toggled = True
            self.sig_vec = [[],[],[]]

            self.sig_type = self.check_radio_btns()
            self.disable_widgets()
            self.startDeviceBtn.setEnabled(False)
            self.startModelBtn.setText("Stop Model")

            self.sig_A = float(self.aLine.text())
            self.sig_freq = float(self.freqLine.text())
            self.sig_gen.reset()
            self.sig_gen.set_params(self.sig_A, self.sig_freq)
            self.model.reset_x()
            self.model.set_servo_params(self.kx, self.kv)
            # self.fr.set_sin_params(self.sin_A, self.sin_freq)
            # self.fr.set_model_params(self.mot_J, self.mot_B, self.mot_k)
            
            # self.fr.reset()
            self.reset_resp_plot()
            self.resp_plot_graph.setYRange(-self.sig_A*1.1, self.sig_A*1.3)
            
            self.timer.start()
            th1 = threading.Thread(target=self.gen_sig, daemon=True)
            th1.start()
            
        else:
            self.stop_gen_sig = True
            self.startModel_toggled = False

            self.timer.stop()
            
            self.enable_widgets()
            # self.startModelBtn.setEnabled(True)
            self.startModelBtn.setText("Start Model")
            self.startDeviceBtn.setEnabled(True)
            
            

    def startDeviceBtn_clicked(self):
        if self.startDevice_toggled == False:
            self.stop_gen_sig = False
            self.startDevice_toggled = True
            self.sig_vec = [[],[],[]]

            self.sig_type = self.check_radio_btns()
            self.disable_widgets()
            self.startModelBtn.setEnabled(False)
            self.startDeviceBtn.setText("Stop Device")

            self.sig_A = float(self.aLine.text())
            self.sig_freq = float(self.freqLine.text())



            self.resp_plot_graph.setYRange(-self.sig_A*1.1, self.sig_A*1.3)
            self.reset_resp_plot()

            self.device.connect()
            time.sleep(0.05)
            self.device.stop()
            self.device.set_k(16, 0)
            self.device.set_fric(1, 20)
            self.device.start_step(0)
            self.device.wait_step(STEP_DELTA)
            self.device.set_k(self.kx, self.kv)
            if self.sig_type == "square":
                # self.ref_sig, self.t = self.sig_gen.gen_square()
                self.device.start_square(self.sig_A, self.sig_freq)
            elif self.sig_type == "sine":
                self.device.start_sin(self.sig_A, self.sig_freq)
                # self.ref_sig, self.t = self.sig_gen.gen_sin()
            elif self.sig_type == "triangle":
                # self.ref_sig, self.t = self.sig_gen.gen_triangle()
                self.device.start_triangle(self.sig_A, self.sig_freq)
            

            th1 = threading.Thread(target=self.gen_sig, daemon=True)
            th1.start()
            self.timer.start()

            print("Start Device")
        else:
            self.startDevice_toggled = False
            self.stop_gen_sig = True
            # self.sin_type = DEVICE
            self.timer.stop()

            # self.device.sp.data = b""
            self.device.stop()
            time.sleep(0.05)
            self.device.disconnect()

            self.enable_widgets()
            # self.startModelBtn.setEnabled(True)
            self.startDeviceBtn.setText("Start Device")
            self.startModelBtn.setEnabled(True)
            print("Stop Device")


    def reset_resp_plot(self):
        self.ref_plot_vec = []
        self.real_plot_vec = []
        self.time = []
        self.resp_plot_graph.setXRange(0, self.x_resp_range)
        self.ref_line.setData(self.time, self.ref_plot_vec)
        self.real_line.setData(self.time, self.real_plot_vec)

    def check_radio_btns(self):
        sig_type = "sine"
        if self.sinRadio.isChecked():
            sig_type = "sine"
        elif self.squareRadio.isChecked():
            sig_type = "square"
        elif self.triangleRadio.isChecked():
            sig_type = "triangle"
        return sig_type
    
    def disable_widgets(self):
        self.kxLine.setEnabled(False)
        self.kvLine.setEnabled(False)
        self.l1Line.setEnabled(False)
        self.l2Line.setEnabled(False)
        self.aLine.setEnabled(False)
        self.freqLine.setEnabled(False)
        self.calcLambdaBtn.setEnabled(False)
        self.calcKBtn.setEnabled(False)
        self.sinRadio.setEnabled(False)
        self.squareRadio.setEnabled(False)
        self.triangleRadio.setEnabled(False)
        self.root_plot_graph.sigMouseClicked.disconnect()
        self.k_plot_graph.sigMouseClicked.disconnect()

    def enable_widgets(self):
        self.kxLine.setEnabled(True)
        self.kvLine.setEnabled(True)
        self.l1Line.setEnabled(True)
        self.l2Line.setEnabled(True)
        self.aLine.setEnabled(True)
        self.freqLine.setEnabled(True)
        self.calcLambdaBtn.setEnabled(True)
        self.calcKBtn.setEnabled(True)
        self.sinRadio.setEnabled(True)
        self.squareRadio.setEnabled(True)
        self.triangleRadio.setEnabled(True)
        self.root_plot_graph.sigMouseClicked.connect(self.root_plot_clicked)
        self.k_plot_graph.sigMouseClicked.connect(self.k_plot_clicked)

    def draw_root_field(self, line, alpha, delta):
        line.clear()
        p_im = 50 * np.tan(alpha)
        field_points_re = [-50, -delta, -50]
        field_points_im = [p_im, 0, -p_im]
        line.setData(field_points_re, field_points_im)

    def draw_k_curves(self):
        self.k1, self.k2, self.k3 = self.servo.calc_k_curves(K_RANGE, 0.1)
        self.k1_line.setData(self.k1[0], self.k1[1])
        self.k2_line.setData(self.k2[0], self.k2[1])
        self.k3_line.setData(self.k3[0], self.k3[1])

    def draw_k(self, kx, kv):
        self.k_line.setData([kx], [kv])

    def plot_line(self, graph, name, time, data, pen, brush, symbol_size=0.0):
        return graph.plot(
            time,
            data,
            name=name,
            pen=pen,
            symbol="o",
            symbolSize=symbol_size,
            symbolBrush=brush,
        )

    def set_model_params(self, J, B):
        self.model_J = J
        self.model_B = B
        self.servo.set_model_params(self.model_J, self.model_B)
        self.model.set_identification_params(self.model_J, self.model_B, 0.0)

        


if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)

    window = ServoWidget()
    window.show()
    app.exec()