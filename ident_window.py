import numpy as np
import sys
from forms.ident_form import Ui_Form
import pyqtgraph as pg
# from pyqtgraph import PlotWidget, plot
from random import randint
import time
import threading
import qtawesome as qta
import yaml
import os

from PyQt5 import QtWidgets, uic
from PyQt5.QtCore import Qt, QTimer
from PyQt5.QtWidgets import QPushButton, QHBoxLayout, QVBoxLayout, QLabel
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *

from freq_resp import FreqResponce
from device import Device
from plot_widget import PlotWidget

# X_TIME_RANGE = 20
X_FREQ_RANGE = 5
STEP_DELTA = 0.05

MODEL = 0
DEVICE = 1

FRIC_K = 0.82
FRIC_OFFSET = 0

N_PERIODS = 5

class IdentWidget(QtWidgets.QWidget, Ui_Form):
    def __init__(self, *args, obj=None, **kwargs):
        super().__init__(*args, **kwargs)
        self.setupUi(self)
        self.setWindowTitle("Identification")
        # self.setStyleSheet("background-color: yellow;") 

        # current_working_directory = os.getcwd()
        current_working_directory = os.path.dirname(__file__)
        config_path = current_working_directory+'/config/config.yaml'
        try:
            with open(config_path, 'r') as file:
                config = yaml.safe_load(file)
            self.sin_A = config['A']
            self.sin_freq = config['freq']

            self.mot_J = config['J']
            self.mot_B = config['B']
            self.mot_k = config['k']

            self.theme = config['theme']
            self.plot_font_size = config['plot_font_size']
            self.plot_point_size = config['plot_point_size']
            self.plot_line_width = config['plot_line_width']
            self.ident_plot_range = config['ident_plot_range']
            self.icon_size = config['icon_size']
            self.font_size = config['font_size']
            self.freq_plot_range = config['freq_plot_range']
        except:
            self.sin_A = 10.0
            self.sin_freq = 1.0

            self.mot_J = 1.0
            self.mot_B = 1.0
            self.mot_k = 1.0

            self.theme = "light"
            self.font_size = 20
            self.plot_font_size = 36
            self.plot_point_size = 20
            self.plot_line_width = 3
            self.ident_plot_range = 20.0
            self.icon_size = 40
            self.freq_plot_range = 3.0

        if self.theme == "dark":
            self.plot_color = [10, 10, 10]
            self.ref_line_color = [254, 105, 40]
            self.real1_line_color = [19, 169, 254]
            self.real2_line_color = [242,15,233]
        else:
            self.plot_color = [255, 255, 255]
            self.ref_line_color = [0, 190, 0]
            self.real1_line_color = [0, 0, 190]
            self.real2_line_color = [190,0,0]


        # sin stuff
        self.t = 0
        self.rate = 200
        self.ts = 1/self.rate

        self.acceptable_sin = (N_PERIODS)/(self.sin_freq*self.ts)
        self.len_sin_points = 0
        self.sin_plot_vec = [[0.0],[0.0]]
        self.amp_model_vec = []
        self.phase_model_vec = []
        self.omega_model_vec = []
        self.amp_device_vec = []
        self.phase_device_vec = []
        self.omega_device_vec = []
        self.sin_sig = [0]*2
        self.sin_sig_vec = [[],[],[]]
        self.stop_gen_sin = True
        self.sin_type = MODEL
        self.device = Device()

        # UI stauff
        self.startModel_toggled = False
        self.startDevice_toggled = False
        self.draw_pressed = False
        self.init_time_plot()
        self.init_amp_plot()
        self.init_phase_plot()
        self.init_ui()

        # freq responce stuff
        self.fr = FreqResponce(self.ts)
        self.fr.set_model_params(self.mot_J, self.mot_B, self.mot_k)

        # Add a timer for time plot
        self.tim_rate = 100
        self.timer = QTimer()
        self.timer.setInterval(int(1/self.tim_rate * 1000))
        self.timer.timeout.connect(self.update_time_plot)

        # Create signals
        self.startModelBtn.clicked.connect(self.startModelBtn_clicked)
        self.startDeviceBtn.clicked.connect(self.startDeviceBtn_clicked)
        self.drawBtn.clicked.connect(self.drawBtn_clicked)
        self.clearBtn.clicked.connect(self.clearBtn_clicked)
        self.putPointBtn.clicked.connect(self.putPointBtn_clicked)

    def init_ui(self):
        self.k_lineEdit.setText(f"{self.mot_k}")
        self.a_lineEdit.setText(f"{self.sin_A}")
        self.freq_lineEdit.setText(f"{self.sin_freq}")
        self.j_lineEdit.setText(f"{self.mot_J}")
        self.b_lineEdit.setText(f"{self.mot_B}")

    def read_line_edits(self):
        self.mot_k = float(self.k_lineEdit.text())
        self.sin_A = float(self.a_lineEdit.text())
        self.sin_freq = float(self.freq_lineEdit.text())
        self.mot_J = float(self.j_lineEdit.text())
        self.mot_B = float(self.b_lineEdit.text())

    def enable_line_edits(self):
        self.k_lineEdit.setEnabled(True)
        self.a_lineEdit.setEnabled(True)
        self.freq_lineEdit.setEnabled(True)
        self.j_lineEdit.setEnabled(True)
        self.b_lineEdit.setEnabled(True)

    def disable_line_edits(self):
        self.k_lineEdit.setEnabled(False)
        self.a_lineEdit.setEnabled(False)
        self.freq_lineEdit.setEnabled(False)
        self.j_lineEdit.setEnabled(False)
        self.b_lineEdit.setEnabled(False)

    def init_time_plot(self):
        self.x_time_range = self.ident_plot_range
        self.time_plot_graph = PlotWidget()#pg.PlotWidget()
        self.time_plot_graph.sigMouseClicked.connect(self.time_plot_clicked)
        self.leftLay.addWidget(self.time_plot_graph)
        # 
        self.time_plot_vb = self.time_plot_graph.getViewBox()
        self.time_plot_vb.setBackgroundColor(self.plot_color)
        
        if self.theme == "dark":
            styles = {"color": "white", "font-size": f"{self.plot_font_size}px"}
        else:
            self.time_plot_graph.setBackground("w")
            styles = {"color": "black", "font-size": f"{self.plot_font_size}px"}

        self.time_plot_graph.addLegend(labelTextSize=f'{self.font_size}pt', labelTextColor=None)
        self.time_plot_graph.setLabel("bottom", "Time (sec)", **styles)
        self.time_plot_graph.showGrid(x=True, y=True, alpha=0.1)
        self.time_plot_graph.setYRange(-self.sin_A*1.1, self.sin_A*1.1+5.5)
        self.time_plot_graph.setXRange(0, self.x_time_range)

        pen = [pg.mkPen(color=tuple(self.ref_line_color), width=self.plot_line_width-1), pg.mkPen(color=tuple(self.real1_line_color), width=self.plot_line_width)]

        self.time = [0]
        self.time_line = [self.plot_line(self.time_plot_graph, "Voltage [v]", self.time, self.sin_plot_vec[0], pen[0], None),
                    self.plot_line(self.time_plot_graph, "Shaft Angle [rad]", self.time, self.sin_plot_vec[1], pen[1], None)]
        
        xMouseLbl = QLabel("X: ")
        yMouseLbl = QLabel("Y: ")
        self.xPosMouseLbl = QLabel("1.5")
        self.yPosMouseLbl = QLabel("0.2")
        self.xPosMouseLbl.setMinimumWidth(100)
        self.yPosMouseLbl.setMinimumWidth(100)
        hSpacer = QtWidgets.QSpacerItem(1, 1, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum) 

        self.taskbarLay = QHBoxLayout()
        self.taskbarLay.addWidget(xMouseLbl)
        self.taskbarLay.addWidget(self.xPosMouseLbl)
        self.taskbarLay.addWidget(yMouseLbl)
        self.taskbarLay.addWidget(self.yPosMouseLbl)
        self.taskbarLay.addItem(hSpacer)
        self.leftLay.addLayout(self.taskbarLay)

        self.sinProgress = QProgressBar()
        self.taskbarLay.addWidget(self.sinProgress)
        self.sinProgress.setMaximumHeight(20)
        self.sinProgress.setVisible(False)

        iconSize = QSize(self.icon_size, self.icon_size)
        icon = qta.icon("fa.check", color='green')
        self.okLbl = QLabel()
        self.okLbl.setPixmap(icon.pixmap(iconSize))
        self.okLbl.setMinimumHeight(20)
        self.okLbl.setMinimumWidth(20)
        self.okLbl.setVisible(False)
        self.taskbarLay.addWidget(self.okLbl)


    def init_amp_plot(self):
        self.x_freq_range = X_FREQ_RANGE
        self.amp_plot_graph = PlotWidget()
        self.rightLay.addWidget(self.amp_plot_graph)
        # self.amp_plot_graph.setBackground("w")
        if self.theme == "dark":
            styles = {"color": "white", "font-size": f"{self.plot_font_size}px"}
        else:
            self.amp_plot_graph.setBackground("w")
            styles = {"color": "black", "font-size": f"{self.plot_font_size}px"}
        self.amp_plot_graph.setLabel("left", "Amplitude", **styles)
        self.amp_plot_graph.setLabel("bottom", "Freq (hz)", **styles)
        self.amp_plot_graph.addLegend(labelTextSize=f'{self.font_size}pt', labelTextColor=None, offset=(0, 10))
        self.amp_plot_graph.showGrid(x=True, y=True, alpha=0.1)
        self.amp_plot_graph.setYRange(0, 1.2)
        self.amp_plot_graph.setXRange(0, self.freq_plot_range)
        self.amp_plot_graph.setMouseEnabled(x=False, y=False)
        self.amp_plot_vb = self.amp_plot_graph.getViewBox()
        self.amp_plot_vb.setBackgroundColor(self.plot_color)

        amp_pen = pg.mkPen(None)

        self.freq = [0]
        self.amp_model_line = self.plot_line(self.amp_plot_graph, "Model", self.time, self.amp_model_vec, amp_pen, tuple(self.real1_line_color), self.plot_point_size)
        self.amp_device_line = self.plot_line(self.amp_plot_graph, "Device", self.time, self.amp_device_vec, amp_pen, (210, 0, 0), self.plot_point_size)

    def init_phase_plot(self):
        self.x_freq_range = X_FREQ_RANGE
        self.phase_plot_graph = PlotWidget()
        pg.setConfigOptions(antialias = True)
        self.rightLay.addWidget(self.phase_plot_graph)
        # self.phase_plot_graph.setBackground("w")
        if self.theme == "dark":
            styles = {"color": "white", "font-size": f"{self.plot_font_size}px"}
        else:
            self.phase_plot_graph.setBackground("w")
            styles = {"color": "black", "font-size": f"{self.plot_font_size}px"}
        self.phase_plot_graph.setLabel("left", "Phase Lag", **styles)
        self.phase_plot_graph.setLabel("bottom", "Freq (hz)", **styles)
        self.phase_plot_graph.showGrid(x=True, y=True, alpha=0.1)
        self.phase_plot_graph.setYRange(-3.14, 0)
        self.phase_plot_graph.setXRange(0, self.freq_plot_range)
        self.phase_plot_graph.setMouseEnabled(x=False, y=False)
        self.phase_plot_vb = self.phase_plot_graph.getViewBox()
        self.phase_plot_vb.setBackgroundColor(self.plot_color)

        phase_pen = pg.mkPen(None)

        # self.freq = [0]
        self.phase_model_line = self.plot_line(self.phase_plot_graph, "Model", self.time, self.phase_model_vec, phase_pen, tuple(self.real1_line_color), self.plot_point_size)
        self.phase_device_line = self.plot_line(self.phase_plot_graph, "Device", self.time, self.phase_device_vec, phase_pen, (210, 0, 0), self.plot_point_size)

        
    def reset_time_plot(self):
        self.sin_plot_vec = [[],[]]
        self.time = []
        self.time_plot_graph.setXRange(0, self.x_time_range)
        self.time_line[0].clear()

    def reset_freq_plots(self):
        self.amp_model_line.clear()
        self.phase_model_line.clear()
        self.amp_model_line.setData([], [])
        self.phase_model_line.setData([], [])
        self.amp_device_line.setData([], [])
        self.phase_device_line.setData([], [])
        
    def startModelBtn_clicked(self):
        if self.startModel_toggled == False:
            self.stop_gen_sin = False
            self.startModel_toggled = True
            self.sin_sig_vec = [[],[],[]]

            self.read_line_edits()
            self.disable_line_edits()
            self.startDeviceBtn.setEnabled(False)
            self.putPointBtn.setEnabled(False)
            self.drawBtn.setEnabled(False)
            self.clearBtn.setEnabled(False)
            self.sinProgress.setVisible(False)
            self.okLbl.setVisible(False)
            self.startModelBtn.setText("Stop Model")
            self.fr.set_sin_params(self.sin_A, self.sin_freq)
            self.fr.set_model_params(self.mot_J, self.mot_B, self.mot_k)
            self.time_plot_graph.setYRange(-self.sin_A*1.1, self.sin_A*1.3)

            self.fr.reset()
            self.reset_time_plot()
            
            th1 = threading.Thread(target=self.gen_sin, daemon=True)
            th1.start()
            self.timer.start()
        else:
            self.stop_gen_sin = True
            self.startModel_toggled = False
            self.sin_type = MODEL
            self.timer.stop()
            
            self.enable_line_edits()
            self.startModelBtn.setText("Start Model")
            self.startDeviceBtn.setEnabled(True)
            self.putPointBtn.setEnabled(True)
            self.drawBtn.setEnabled(True)
            self.clearBtn.setEnabled(True)

    def startDeviceBtn_clicked(self):
        if self.startDevice_toggled == False:
            self.stop_gen_sin = False
            self.startDevice_toggled = True

            self.startModelBtn.setEnabled(False)
            self.putPointBtn.setEnabled(False)
            self.drawBtn.setEnabled(False)
            self.clearBtn.setEnabled(False)
            self.drawBtn.setEnabled(False)
            self.disable_line_edits()
            self.startDeviceBtn.setText("Stop Device")
            self.sinProgress.setVisible(True)
            self.okLbl.setVisible(False)

            self.reset_time_plot()

            self.sin_sig_vec = [[],[],[]]
            self.read_line_edits()
            self.time_plot_graph.setYRange(-self.sin_A*1.1, self.sin_A*1.3)
            self.fr.set_sin_params(self.sin_A, self.sin_freq)
            self.acceptable_sin = (N_PERIODS)/(self.sin_freq*self.ts)
            self.len_sin_points = 0
            self.device.connect()
            time.sleep(0.1)
            self.device.stop()
            self.device.set_k(16, 0)
            self.device.set_fric(FRIC_K, FRIC_OFFSET)
            # self.device.start_step(0)
            # self.device.wait_step(STEP_DELTA)
            # time.sleep(0.2)
            self.device.set_k(self.mot_k, 0)
            self.device.start_sin_u(self.sin_A, self.sin_freq)

            th1 = threading.Thread(target=self.gen_sin, daemon=True)
            th1.start()
            self.timer.start()

            print("Start Device")
        else:
            self.startDevice_toggled = False
            self.stop_gen_sin = True
            self.sin_type = DEVICE
            self.timer.stop()

            self.device.stop()
            time.sleep(0.005)
            self.device.disconnect()

            self.startModelBtn.setEnabled(True)
            self.putPointBtn.setEnabled(True)
            self.drawBtn.setEnabled(True)
            self.clearBtn.setEnabled(True)
            self.drawBtn.setEnabled(True)
            self.sinProgress.setVisible(False)
            self.startDeviceBtn.setText("Start Device")
            self.enable_line_edits()

            # cut from the end until ref signal crosses zero
            # import matplotlib.pyplot as plt

            last_zero = 0
            for i in range(len(self.sin_sig_vec[0])-1, -1, -1):
                if np.abs(self.sin_sig_vec[0][i]) <= self.sin_A/70:
                    last_zero = i
                    break
            if self.sin_sig_vec[2][0] > self.sin_sig_vec[2][1]:
                self.sin_sig_vec[0] = self.sin_sig_vec[0][1:last_zero]
                self.sin_sig_vec[1] = self.sin_sig_vec[1][1:last_zero]
                self.sin_sig_vec[2] = self.sin_sig_vec[2][1:last_zero]
            else:
                self.sin_sig_vec[0] = self.sin_sig_vec[0][:last_zero]
                self.sin_sig_vec[1] = self.sin_sig_vec[1][:last_zero]
                self.sin_sig_vec[2] = self.sin_sig_vec[2][:last_zero]

            # plt.plot(self.sin_sig_vec[2], self.sin_sig_vec[0])
            # plt.plot(self.sin_sig_vec[2], self.sin_sig_vec[1])
            # plt.show()

            print("Stop Device")

    def putPointBtn_clicked(self):
        self.read_line_edits()
        if self.sin_type == MODEL:
            self.fr.set_model_params(self.mot_J, self.mot_B, self.mot_k)
            amp, phase = self.fr.calc_point_model(self.sin_freq*(2*np.pi), self.mot_J, self.mot_B, self.mot_k)
            self.amp_model_vec.append(amp)
            self.phase_model_vec.append(phase)
            self.omega_model_vec.append(self.sin_freq)
            self.amp_model_line.setData(self.omega_model_vec, self.amp_model_vec)
            self.phase_model_line.setData(self.omega_model_vec, self.phase_model_vec)
        elif self.sin_type == DEVICE:
            amp, phase = self.fr.calc_point_real(sig1=self.sin_sig_vec[0], 
                                                 sig2=self.sin_sig_vec[1], 
                                                 t=self.sin_sig_vec[2], 
                                                 period=1/self.sin_freq)
            print(1/self.sin_freq)
            if phase > 0:
                phase = -(2 - phase/np.pi) * np.pi
            self.amp_device_vec.append(amp)
            self.phase_device_vec.append(phase)
            self.omega_device_vec.append(self.sin_freq)
            self.amp_device_line.setData(self.omega_device_vec, self.amp_device_vec)
            self.phase_device_line.setData(self.omega_device_vec, self.phase_device_vec)

        self.freq_plots_autoscale()

    def drawBtn_clicked(self):
        self.draw_pressed = True
        self.read_line_edits()
        self.fr.set_model_params(self.mot_J, self.mot_B, self.mot_k)

        self.amp_model_vec, self.phase_model_vec, self.omega_model_vec = self.fr.freq_resp_model()
        for i in range(len(self.omega_model_vec)):
            self.omega_model_vec[i] /= (2*np.pi)
        self.amp_model_line.setData(self.omega_model_vec, self.amp_model_vec)
        self.phase_model_line.setData(self.omega_model_vec, self.phase_model_vec)

        self.freq_plots_autoscale()

    def freq_plots_autoscale(self):
        # amv = self.amp_plot_graph.getViewBox()
        self.amp_plot_vb.enableAutoRange(axis='y', enable=True)
        # amv.enableAutoRange(axis='x', enable=True)

        # pmv = self.phase_plot_graph.getViewBox()
        # pmv.enableAutoRange(axis='y', enable=True)
        # pmv.enableAutoRange(axis='x', enable=True)

    def clearBtn_clicked(self):
        self.draw_pressed = False
        self.amp_model_vec = []
        self.phase_model_vec = []
        self.omega_model_vec = []
        self.amp_device_vec = []
        self.phase_device_vec = []
        self.omega_device_vec = []
        self.reset_freq_plots()

    def time_plot_clicked(self, e):
        mousePoint = self.time_plot_graph.getPlotItem().vb.mapSceneToView(e.pos())
        self.xPosMouseLbl.setText(f"{mousePoint.x():.2f}")
        self.yPosMouseLbl.setText(f"{mousePoint.y():.2f}")
    
    def append_sig_vectors(self):
        if self.t >= 0.0:
            self.sin_sig_vec[0].append(self.sin_sig[0])
            self.sin_sig_vec[1].append(self.sin_sig[1])
            self.sin_sig_vec[2].append(self.t)
            self.len_sin_points += 1
            # print(f"{self.acceptable_sin} {len(self.sin_sig_vec[0])}")
            if len(self.sin_sig_vec[0]) > self.acceptable_sin:
                self.sin_sig_vec[0] = self.sin_sig_vec[0][1:]
                self.sin_sig_vec[1] = self.sin_sig_vec[1][1:]
                self.sin_sig_vec[2] = self.sin_sig_vec[2][1:]
        else:
            print("warning: t=-1")
    
    def gen_sin(self):
        while self.stop_gen_sin == False:
            # print("gen_sin")
            if self.startModel_toggled == True:
                self.sin_sig[0], self.sin_sig[1], self.t = self.fr.step_sin_model()
                self.append_sig_vectors()
            elif self.startDevice_toggled == True:
                while True:
                    self.sin_sig[0], self.sin_sig[1], self.t, d_ref = self.device.get_data()
                    self.append_sig_vectors()
                    if self.device.get_data_lag() <= 2:
                        break
                    time.sleep(0.0001)
            time.sleep(self.ts)
            

    def update_time_plot(self):
        if self.t >= 0:
            # print("update_time_plot")
            self.time.append(self.t)
            while (self.time[-1] - self.time[0]) > self.x_time_range:
                self.time = self.time[1:]
                self.sin_plot_vec[0] = self.sin_plot_vec[0][1:]
                self.sin_plot_vec[1] = self.sin_plot_vec[1][1:]
                self.time_plot_graph.setXRange(self.time[0]-0.1, self.time[-1]+0.1)
            
            # sin stuff
            for i in range(2):
                self.sin_plot_vec[i].append(self.sin_sig[i])
                self.time_line[i].setData(self.time, self.sin_plot_vec[i])

            progress = int(100*self.len_sin_points/(1.3*self.acceptable_sin))
            self.sinProgress.setValue(progress)
            if progress >= 99:
                self.sinProgress.setVisible(False)
                self.sinProgress.setValue(0)
                self.okLbl.setVisible(True)
        

    def plot_line(self, graph, name, time, data, pen, brush, symbol_size=0.0):
        if self.theme == 'dark':
            symbolPen = 'black'
        else:
            symbolPen = 'white'

        return graph.plot(
            time,
            data,
            name=name,
            pen=pen,
            symbol="o",
            symbolPen =symbolPen,
            symbolSize=symbol_size,
            symbolBrush=brush,
        )
    
    def get_model_params(self):
        return self.mot_J, self.mot_B, self.mot_k



if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)

    window = IdentWidget()
    window.show()
    app.exec()