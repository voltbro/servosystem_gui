#!/home/yoggi/Labs/dc_motor/.venv/bin/python3

# TODO: 
# OK 1. При переходе на servo system передавать J и B из identification
# OK 2. Проверить последнюю сашину прошивку
# 3. Разобраться с увеличением окна при переходе из серво в идентификацию
# OK 4. Зарзобраться с накапливающейся задержкой по сериал 
# 5. Сделать исключение, если нет сериал порта


import sys
import yaml
from PyQt5 import QtWidgets, uic
from PyQt5.QtCore import Qt, QTimer
from forms.main_form import Ui_Dialog
from ident_window import IdentWidget
from servo_window import ServoWidget
from PyQt5.QtWidgets import QPushButton, QHBoxLayout, QVBoxLayout, QSpacerItem, QSizePolicy


class MainWindow(QtWidgets.QDialog, Ui_Dialog):
    def __init__(self, *args, obj=None, **kwargs):
        super(MainWindow, self).__init__(*args, **kwargs)
        self.setupUi(self)
        self.setWindowFlags(Qt.Window)
        self.showMaximized()

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