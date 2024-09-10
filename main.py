#!/home/yoggi/Labs/dc_motor/.venv/bin/python3

import sys
import yaml
import os
import qtawesome as qta
from PyQt5 import QtWidgets, uic
from PyQt5 import QtGui
from PyQt5.QtCore import Qt, QTimer
from forms.main_form import Ui_Dialog
from ident_window import IdentWidget
from servo_window import ServoWidget
from PyQt5.QtWidgets import QPushButton, QHBoxLayout, QVBoxLayout, QSpacerItem, QSizePolicy

GLOBAL_STYLE = """QPushButton {
    color: red; 
}"""


class MainWindow(QtWidgets.QDialog, Ui_Dialog):
    def __init__(self, *args, obj=None, **kwargs):
        super(MainWindow, self).__init__(*args, **kwargs)
        self.setupUi(self)
        self.setWindowFlags(Qt.Window)
        self.showMaximized()
        

        current_working_directory = os.path.dirname(__file__)

        # icon = QtGui.QIcon()
        # icon.addPixmap(QtGui.QPixmap(current_working_directory + '/icons/icon.png'), QtGui.QIcon.Selected, QtGui.QIcon.On)
        # self.setWindowIcon(icon)

        # icon = qta.icon("fa.check", color='green')
        # self.setWindowIcon(icon)

        self.setWindowIcon(QtGui.QIcon(current_working_directory + '/icons/icon.png'))
        # print(current_working_directory + '/icons/icon.png')



        config_path = current_working_directory+'/config/config.yaml'
        try:
            with open(config_path, 'r') as file:
                config = yaml.safe_load(file)
            self.theme = config['theme']
            self.font_size = config['font_size']
        except:
            self.theme = 'light'
            self.font_size = 10

        if self.theme == 'dark':
            self.setStyleSheet("QWidget {" + f"color: rgb(230, 230, 230); font-size: {self.font_size}pt; background-color: rgb(24,24,24);" + "} " + 
                                "QRadioButton::indicator {" + f"border: 1px solid white; height: {self.font_size*0.65}px; width: {self.font_size*0.65}px; border-radius: {self.font_size*0.65/2}px;" + "} " + 
                                "QRadioButton::indicator:checked {background: rgb(230, 230, 230);}" + 
                                "QLineEdit {border: 1px solid rgb(90, 90, 90);}" +
                                "QPushButton::disabled {color: rgb(80, 80, 80)}") 
        else:
            self.setStyleSheet(f"font-size: {self.font_size}pt;") 

        self.identWidget = IdentWidget()
        self.servoWidget = ServoWidget()

        self.identWidget.setVisible(True)
        self.servoWidget.setVisible(False)

        self.mainLay.addWidget(self.identWidget)
        self.mainLay.addWidget(self.servoWidget)

        self.identModeBtn.clicked.connect(self.identModeBtn_clicked)
        self.servoModeBtn.clicked.connect(self.servoModeBtn_clicked)
        
    def identModeBtn_clicked(self):
        self.identWidget.setVisible(True)
        self.servoWidget.setVisible(False)

    def servoModeBtn_clicked(self):
        J, B, k = self.identWidget.get_model_params()
        self.servoWidget.set_model_params(J, B, 0)
        self.identWidget.setVisible(False)
        self.servoWidget.setVisible(True)

if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)

    window = MainWindow()
    window.show()
    app.exec()