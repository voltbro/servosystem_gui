#!/home/yoggi/Labs/dc_motor/.venv/bin/python3
import numpy as np
import pyqtgraph as pg
import time
import threading
import yaml
import os

import sys
from PyQt5 import QtWidgets, uic
from PyQt5.QtCore import Qt, QTimer
from forms.servo_form import Ui_Form
from ident_window import IdentWidget
from PyQt5.QtWidgets import QPushButton, QHBoxLayout, QVBoxLayout, QSpacerItem, QSizePolicy, QMessageBox, QLabel
# from pyqtgraph.Qt import QtGui, QtCore
from PyQt5 import QtGui

from plot_widget import PlotWidget
from servo_analysys import ServoAnalysys
from signal_generator import SignalGenerator
from motor_dynamics import MotorDynamics
from device import Device

# try:
#     import OpenGL
#     pg.setConfigOption('useOpenGL', True)
#     pg.setConfigOption('enableExperimental', True)
# except Exception as e:
#     print(f"Enabling OpenGL failed with {e}. Will result in slow rendering. Try installing PyOpenGL.")

X_ROOT_RANGE = 12.0
Y_ROOT_RANGE = 11.5
X_K_RANGE = 21
Y_K_RANGE = 12
# X_RESP_RANGE = 10
Y_RESP_RANGE = 5
STEP_DELTA = 0.05

# DELTA = 1
# ALPHA = np.pi/4
K_RANGE = 40

class ServoWidget(QtWidgets.QWidget, Ui_Form):
    def __init__(self, *args, obj=None, **kwargs):
        super().__init__(*args, **kwargs)
        self.setupUi(self)
        self.resize(2048, 1536)

        current_working_directory = os.path.dirname(__file__)
        config_path = current_working_directory+'/config/config.yaml'
        try:
            with open(config_path, 'r') as file:
                config = yaml.safe_load(file)

            self.delta = config['delta']
            self.alpha = config['alpha']
            self.kx = config['kx']
            self.kv = config['kv']

            self.plot_font_size = config['plot_font_size']
            self.plot_point_size = config['plot_point_size']
            self.plot_line_width = config['plot_line_width']
            self.servo_plot_range = config['servo_plot_range']
        except:
            self.delta = 1.0
            self.alpha = 0.7
            self.kx = 16.0
            self.kv = 0.0

            self.plot_font_size = 36
            self.plot_point_size = 20
            self.plot_line_width = 3
            self.servo_plot_range = 10.0

        self.servo = ServoAnalysys()
        self.servo.set_root_params(self.delta, self.alpha)

        self.model_J = 0.2
        self.model_B = 1.0
        self.sig_A = 1.0
        self.sig_freq = 0.25
        self.t = 0
        self.sig_rate = 200
        self.draw_rate = 40
        self.ts = 1/self.sig_rate
        self.sig_gen = SignalGenerator(ts=self.ts, A=self.sig_A, freq=self.sig_freq)
        self.model = MotorDynamics(ts=self.ts,
                            J=self.model_J,
                            B=self.model_B,
                            k=0.0,
                            model_type=1,
                            kx=self.kx,
                            kv=self.kv,
                            )
        self.device = Device()

        self.ref_plot_vec = []
        self.real_model_plot_vec = []
        self.real_device_plot_vec = []
        self.ref_sig = 0.0
        self.real_model_sig = 0.0
        self.real_device_sig = 0.0

        self.im_x_line = [0, 0]
        self.im_y_line = [50, -50]
        self.re_x_line = [-50, 50]
        self.re_y_line = [0, 0]
        self.root_pos_re = []
        self.root_pos_im = []

        # self.kx = 16.0
        # self.kv = 0.0
        self.lambda1, self.lambda2 = self.servo.calc_lambda(self.kx, self.kv)

        self.startModel_toggled = False
        self.startDevice_toggled = False
        self.startBoth_toggled = False
        self.stop_gen_sig = False
        self.sig_vec = [[],[],[]]
        self.sig_type = "sine"
        
        self.init_root_locus_plot()
        self.init_k_plot()
        self.init_resp_plot()
        self.splitter.setSizes([1000, 2000])
        self.kxLine.setText(f"{self.kx:.2f}")
        self.kvLine.setText(f"{self.kv:.2f}")
        self.l1Line.setText(f"{self.lambda1.real:.2f}{'+-'[int(self.lambda1.imag < 0)]}{np.abs(self.lambda1.imag):.2f}j")
        self.l2Line.setText(f"{self.lambda2.real:.2f}{'+-'[int(self.lambda2.imag < 0)]}{np.abs(self.lambda2.imag):.2f}j")
        self.aLine.setText(f"{self.sig_A}")
        self.freqLine.setText(f"{self.sig_freq}")

        self.draw_k(self.kx, self.kv)
        self.root_pos_re = [self.lambda1.real, self.lambda2.real]
        self.root_pos_im = [self.lambda1.imag, self.lambda2.imag]
        self.root_line.setData(self.root_pos_re, self.root_pos_im)

        self.calcKBtn.clicked.connect(self.calcKBtn_clicked)
        self.calcLambdaBtn.clicked.connect(self.calcLambdaBtn_clicked)
        self.startModelBtn.clicked.connect(self.startModelBtn_clicked)
        self.startDeviceBtn.clicked.connect(self.startDeviceBtn_clicked)
        self.startBothBtn.clicked.connect(self.startBothBtn_clicked)

        self.start = 0.0
        self.timer = QTimer()
        self.timer.setInterval(int(1000/self.draw_rate))
        self.timer.timeout.connect(self.update_resp_plot)
        self.first_timer_event = True

        self.timer2 = QTimer()
        self.timer2.setInterval(int(1000/self.sig_rate))
        self.timer2.timeout.connect(self.gen_sig)

        self.time_offset = 0.0
    
    def init_root_locus_plot(self):
        self.x_root_range = X_ROOT_RANGE
        self.y_root_range = Y_ROOT_RANGE
        self.root_plot_graph = PlotWidget()
        self.root_plot_graph.sigMouseClicked.connect(self.root_plot_clicked)
        self.leftLay.addWidget(self.root_plot_graph)
        self.root_plot_graph.setBackground("w")
        styles = {"color": "black", "font-size": f"{self.plot_font_size}px"}
        self.root_plot_graph.setLabel("left", "Im", **styles)
        self.root_plot_graph.setLabel("bottom", "Re", **styles)
        # self.root_plot_graph.addLegend()
        self.root_plot_graph.showGrid(x=True, y=True)
        self.root_plot_graph.setYRange(-self.y_root_range, self.y_root_range)
        self.root_plot_graph.setXRange(-self.x_root_range, 0.2)

        pen = pg.mkPen(None)
        pen_axis = pg.mkPen(color=(0, 0, 0), width=1)
        pen_field = pg.mkPen(color=(0, 0, 0), width=2)
        
        self.im_line = self.plot_line(self.root_plot_graph, "", self.im_x_line, self.im_y_line, pen_axis, "b", 0.0)
        self.re_line = self.plot_line(self.root_plot_graph, "", self.re_x_line, self.re_y_line, pen_axis, "b", 0.0)
        self.field_line = self.plot_line(self.root_plot_graph, "", [], [], pen_field, "b", 0.0)
        self.root_line = self.plot_line(self.root_plot_graph, "Roots", self.root_pos_re, self.root_pos_im, pen, "r", self.plot_point_size)
        self.draw_root_field(self.field_line, self.alpha, self.delta)

    def init_k_plot(self):
        self.x_k_range = X_K_RANGE
        self.y_k_range = Y_K_RANGE
        self.k_plot_graph = PlotWidget()
        self.k_plot_graph.sigMouseClicked.connect(self.k_plot_clicked)
        self.leftLay.addWidget(self.k_plot_graph)
        self.k_plot_graph.setBackground("w")
        styles = {"color": "black", "font-size": f"{self.plot_font_size}px"}
        self.k_plot_graph.setLabel("left", "k_v", **styles)
        self.k_plot_graph.setLabel("bottom", "k_x", **styles)
        # self.k_plot_graph.addLegend()
        self.k_plot_graph.showGrid(x=True, y=True)
        self.k_plot_graph.setYRange(0, self.y_k_range)
        self.k_plot_graph.setXRange(0, self.x_k_range)

        pen = pg.mkPen(None)
        pen_k = pg.mkPen(color=(0, 0, 0), width=2)

        self.root_pos_re = []
        self.k_line = self.plot_line(self.k_plot_graph, "1", [], [], pen_k, "r", self.plot_point_size)
        self.k1_line = self.plot_line(self.k_plot_graph, "1", self.root_pos_re, [], pen_k, "r", 0.0)
        self.k2_line = self.plot_line(self.k_plot_graph, "2", self.root_pos_re, [], pen_k, "g", 0.0)
        self.k3_line = self.plot_line(self.k_plot_graph, "3", self.root_pos_re, [], pen_k, "b", 0.0)
        self.draw_k_curves()

    def init_resp_plot(self):
        self.x_resp_range = self.servo_plot_range
        self.y_resp_range = Y_RESP_RANGE
        self.resp_plot_graph = PlotWidget()
        
        # self.resp_plot_graph.disableAutoRange()
        self.resp_plot_graph.setUpdatesEnabled = False
        self.resp_plot_graph.sigMouseClicked.connect(self.resp_plot_clicked)
        self.rightLay.addWidget(self.resp_plot_graph)
        self.resp_plot_graph.setBackground("w")
        styles = {"color": "black", "font-size": f"{self.plot_font_size}px"}
        self.resp_plot_graph.setLabel("left", "Angle [rad]", **styles)
        self.resp_plot_graph.setLabel("bottom", "Time [sec]", **styles)
        self.resp_plot_graph.addLegend()
        self.resp_plot_graph.showGrid(x=True, y=True)
        self.resp_plot_graph.setYRange(-self.y_resp_range, self.y_resp_range)
        self.resp_plot_graph.setXRange(-self.x_resp_range, 0.2)

        pen_ref = pg.mkPen(color=(0, 190, 0), width=self.plot_line_width)
        pen_model_real = pg.mkPen(color=(0, 0, 190), width=self.plot_line_width)
        pen_device_real = pg.mkPen(color=(190, 0, 0), width=self.plot_line_width)

        self.time = []

        self.ref_line = self.plot_line(self.resp_plot_graph, "Ref", self.time, [], pen_ref, "r", 0.0)
        self.real_model_line = self.plot_line(self.resp_plot_graph, "Model", self.time, [], pen_model_real, "g", 0.0)
        self.real_device_line = self.plot_line(self.resp_plot_graph, "Device", self.time, [], pen_device_real, "b", 0.0)

        xMouseLbl = QLabel("X: ")
        yMouseLbl = QLabel("Y: ")
        self.xPosMouseLbl = QLabel("1.5")
        self.yPosMouseLbl = QLabel("0.2")
        # xMouseLbl.setMaximumHeight(10)
        # yMouseLbl.setMaximumHeight(10)
        self.xPosMouseLbl.setMinimumWidth(100)
        self.yPosMouseLbl.setMinimumWidth(100)
        hSpacer = QtWidgets.QSpacerItem(1, 1, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum) 

        self.taskbarLay = QHBoxLayout()
        self.taskbarLay.addItem(hSpacer)
        self.taskbarLay.addWidget(xMouseLbl)
        self.taskbarLay.addWidget(self.xPosMouseLbl)
        self.taskbarLay.addWidget(yMouseLbl)
        self.taskbarLay.addWidget(self.yPosMouseLbl)
        self.rightLay.addLayout(self.taskbarLay)

    def update_resp_plot(self):
        if self.t >= 0:
            
            # print("update_resp_plot")
            if self.first_timer_event == True:
                self.first_timer_event = False    
            else:
                self.time.append(self.t - self.time_offset)
                if (self.time[-1] - self.time[0]) > self.x_resp_range:
                    self.time_offset += self.x_resp_range
                    self.time = [self.t - self.time_offset]
                    self.ref_plot_vec = []
                    self.real_model_plot_vec = []
                    self.real_device_plot_vec = []
                    # self.resp_plot_graph.setXRange(self.time[0]-0.1, self.time[-1]+0.1)
                # if (self.time[-1] - self.time[0]) > self.x_resp_range:
                #     self.time = self.time[1:]
                #     self.ref_plot_vec = self.ref_plot_vec[1:]
                #     self.real_model_plot_vec = self.real_model_plot_vec[1:]
                #     self.real_device_plot_vec = self.real_device_plot_vec[1:]
                #     # self.resp_plot_graph.setXRange(self.time[0]-0.1, self.time[-1]+0.1)
                
                
                
                # sig stuff
                
                self.resp_plot_graph.disableAutoRange()
                self.ref_plot_vec.append(self.ref_sig)
                # start = time.time()
                self.ref_line.setData(self.time, self.ref_plot_vec)
                # end = time.time() - start ## собственно время работы программы
                # print(f"{end:.5f}")
                if self.startBoth_toggled == True or self.startModel_toggled == True:
                    self.real_model_plot_vec.append(self.real_model_sig)
                    self.real_model_line.setData(self.time, self.real_model_plot_vec)
                if self.startBoth_toggled == True or self.startDevice_toggled == True:
                    self.real_device_plot_vec.append(self.real_device_sig)
                    self.real_device_line.setData(self.time, self.real_device_plot_vec)
                # self.resp_plot_graph.autoRange()
                
                
            

    def gen_sig(self):
        # while self.stop_gen_sig == False:
        # print("gen_sig")
        # start = time.time()
        if self.startBoth_toggled == True:
            while True:
                self.ref_sig, self.real_device_sig, self.t, d_sig = self.device.get_data()
                if self.device.get_data_lag() <= 2:
                    break
                time.sleep(0.0001)
            u = np.array([self.ref_sig, 0])
            self.real_model_sig = self.model.step(u)

        elif self.startModel_toggled == True:
            
            if self.sig_type == "square":
                self.ref_sig, self.t, d_sig = self.sig_gen.gen_square()
            elif self.sig_type == "sine":
                self.ref_sig, self.t, d_sig = self.sig_gen.gen_sin()
            elif self.sig_type == "triangle":
                self.ref_sig, self.t, d_sig = self.sig_gen.gen_triangle()
            u = np.array([self.ref_sig, d_sig])
            
            self.real_model_sig = self.model.step(u)
            

        elif self.startDevice_toggled == True:
            # if  self.device.is_ready() == True:
            while True:
                self.ref_sig, self.real_device_sig, self.t, d_sig = self.device.get_data()
                if self.device.get_data_lag() <= 2:
                    break
                time.sleep(0.0001)
            # self.device.reset_readiness()

        # time.sleep(self.ts)
            # end = time.time() - self.start ## собственно время работы программы
            # print(end) ## вывод времени
            # self.start = time.time()  
        # end = time.time() - start ## собственно время работы программы
        # print(f"{end:.5f}")

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
        # show results in plots and linedits
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
        # show results in polots and linedits
        self.draw_k(self.kx, self.kv)
        self.root_pos_re = [self.lambda1.real, self.lambda2.real]
        self.root_pos_im = [self.lambda1.imag, self.lambda2.imag]
        self.root_line.setData(self.root_pos_re, self.root_pos_im)
        self.l1Line.setText(f"{self.lambda1.real:.2f}{'+-'[int(self.lambda1.imag < 0)]}{np.abs(self.lambda1.imag):.2f}j")
        self.l2Line.setText(f"{self.lambda2.real:.2f}{'+-'[int(self.lambda2.imag < 0)]}{np.abs(self.lambda2.imag):.2f}j")
        self.kxLine.setText(f"{self.kx:.2f}")
        self.kvLine.setText(f"{self.kv:.2f}")

    def resp_plot_clicked(self, e):
        mousePoint = self.resp_plot_graph.getPlotItem().vb.mapSceneToView(e.pos())
        self.xPosMouseLbl.setText(f"{mousePoint.x():.2f}")
        self.yPosMouseLbl.setText(f"{mousePoint.y():.2f}")

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
            self.first_timer_event = True
            # self.sig_vec = [[],[],[]]

            self.sig_type = self.check_radio_btns()
            self.disable_widgets()
            self.startDeviceBtn.setEnabled(False)
            self.startBothBtn.setEnabled(False)
            self.startModelBtn.setText("Stop Model")

            self.sig_A = float(self.aLine.text())
            self.sig_freq = float(self.freqLine.text())
            self.sig_gen.reset()
            self.sig_gen.set_params(self.sig_A, self.sig_freq)
            print(f"J: {self.model.J} | B: {self.model.B} | k: {self.model.k}")
            self.model.reset_x()
            self.model.set_servo_params(self.kx, self.kv)
            # self.fr.set_sin_params(self.sin_A, self.sin_freq)
            # self.fr.set_model_params(self.mot_J, self.mot_B, self.mot_k)
            
            # self.fr.reset()
            self.resp_plot_graph.setMouseEnabled(x=False, y=False)
            self.reset_resp_plot()
            self.resp_plot_graph.setYRange(-self.sig_A*1.1, self.sig_A*1.3)
            
            self.timer.start()
            self.timer2.start()
            # th1 = threading.Thread(target=self.gen_sig, daemon=True)
            # th1.start()
            
        else:
            self.stop_gen_sig = True
            self.startModel_toggled = False

            self.timer.stop()
            self.timer2.stop()
            self.time_offset = 0.0
            
            self.enable_widgets()
            self.resp_plot_graph.setMouseEnabled(x=True, y=True)
            # self.startModelBtn.setEnabled(True)
            self.startModelBtn.setText("Start Model")
            self.startDeviceBtn.setEnabled(True)
            self.startBothBtn.setEnabled(True)
            

    def startDeviceBtn_clicked(self):
        if self.startDevice_toggled == False:
            try:
                self.device.connect()
            except:
                dlg = QMessageBox(self)
                dlg.setWindowTitle("Error")
                dlg.setText("Cannot connect to Serial Device!")
                dlg.setIcon(QMessageBox.Critical)
                button = dlg.exec()
                if button == QMessageBox.Ok:
                    print("OK")
                return

            self.stop_gen_sig = False
            self.startDevice_toggled = True
            self.first_timer_event = True
            # self.sig_vec = [[],[],[]]

            self.sig_type = self.check_radio_btns()
            self.disable_widgets()
            self.resp_plot_graph.setMouseEnabled(x=False, y=False)
            self.startModelBtn.setEnabled(False)
            self.startBothBtn.setEnabled(False)
            self.startDeviceBtn.setText("Stop Device")

            self.sig_A = float(self.aLine.text())
            self.sig_freq = float(self.freqLine.text())

            self.reset_resp_plot()
            self.resp_plot_graph.setYRange(-self.sig_A*1.1, self.sig_A*1.3)

            time.sleep(0.05)
            self.device.stop()
            self.device.set_k(16, 0)
            self.device.set_fric(1.0, 20)
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
            

            # th1 = threading.Thread(target=self.gen_sig, daemon=True)
            # th1.start()
            self.timer.start()
            self.timer2.start()

            print("Start Device")
        else:
            self.startDevice_toggled = False
            self.stop_gen_sig = True
            # self.sin_type = DEVICE
            self.timer.stop()
            self.timer2.stop()
            self.time_offset = 0.0

            # self.device.sp.data = b""
            self.device.stop()
            time.sleep(0.05)
            self.device.disconnect()

            self.enable_widgets()
            self.resp_plot_graph.setMouseEnabled(x=True, y=True)
            # self.startModelBtn.setEnabled(True)
            self.startDeviceBtn.setText("Start Device")
            self.startModelBtn.setEnabled(True)
            self.startBothBtn.setEnabled(True)
            print("Stop Device")

    def startBothBtn_clicked(self):
        if self.startBoth_toggled == False:
            try:
                self.device.connect()
            except:
                dlg = QMessageBox(self)
                dlg.setWindowTitle("Error")
                dlg.setText("Cannot connect to Serial Device!")
                dlg.setIcon(QMessageBox.Critical)
                button = dlg.exec()
                if button == QMessageBox.Ok:
                    print("OK")
                return

            self.stop_gen_sig = False
            self.startBoth_toggled = True
            self.first_timer_event = True
            # self.sig_vec = [[],[],[]]

            self.sig_type = self.check_radio_btns()
            self.disable_widgets()
            self.resp_plot_graph.setMouseEnabled(x=False, y=False)
            self.startModelBtn.setEnabled(False)
            self.startDeviceBtn.setEnabled(False)
            self.startBothBtn.setText("Stop")

            self.sig_A = float(self.aLine.text())
            self.sig_freq = float(self.freqLine.text())

            self.reset_resp_plot()
            self.resp_plot_graph.setYRange(-self.sig_A*1.1, self.sig_A*1.3)

            self.sig_gen.reset()
            self.sig_gen.set_params(self.sig_A, self.sig_freq)
            self.model.reset_x()
            self.model.set_servo_params(self.kx, self.kv)

            time.sleep(0.05)
            self.device.stop()
            self.device.set_k(16, 0)
            self.device.set_fric(1.0, 20)
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
            

            # th1 = threading.Thread(target=self.gen_sig, daemon=True)
            # th1.start()
            self.timer.start()
            self.timer2.start()

            print("Start Device")
        else:
            self.startBoth_toggled = False
            self.stop_gen_sig = True
            # self.sin_type = DEVICE
            self.timer.stop()
            self.timer2.stop()
            self.time_offset = 0.0

            # self.device.sp.data = b""
            self.device.stop()
            time.sleep(0.05)
            self.device.disconnect()

            self.enable_widgets()
            self.resp_plot_graph.setMouseEnabled(x=True, y=True)
            # self.startModelBtn.setEnabled(True)
            self.startBothBtn.setText("Start Both")
            self.startModelBtn.setEnabled(True)
            self.startDeviceBtn.setEnabled(True)
            print("Stop Device")


    def reset_resp_plot(self):
        self.ref_plot_vec = []
        self.real_model_plot_vec = []
        self.real_device_plot_vec = []
        self.time = []
        self.resp_plot_graph.setXRange(0, self.x_resp_range)
        self.ref_line.setData(self.time, self.ref_plot_vec)
        self.real_model_line.setData(self.time, self.real_model_plot_vec)
        self.real_device_line.setData(self.time, self.real_device_plot_vec)

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

    def set_model_params(self, J, B, k):
        self.model_J = J
        self.model_B = B
        self.model_k = k
        self.servo.set_model_params(self.model_J, self.model_B, self.model_k)
        self.model.set_identification_params(self.model_J, self.model_B, self.model_k)

        self.lambda1, self.lambda2 = self.servo.calc_lambda(self.kx, self.kv)
        self.draw_k(self.kx, self.kv)
        self.root_pos_re = [self.lambda1.real, self.lambda2.real]
        self.root_pos_im = [self.lambda1.imag, self.lambda2.imag]
        self.root_line.setData(self.root_pos_re, self.root_pos_im)
        self.kxLine.setText(f"{self.kx:.2f}")
        self.kvLine.setText(f"{self.kv:.2f}")
        self.l1Line.setText(f"{self.lambda1.real:.2f}{'+-'[int(self.lambda1.imag < 0)]}{np.abs(self.lambda1.imag):.2f}j")
        self.l2Line.setText(f"{self.lambda2.real:.2f}{'+-'[int(self.lambda2.imag < 0)]}{np.abs(self.lambda2.imag):.2f}j")

        


if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)

    window = ServoWidget()
    window.show()
    app.exec()