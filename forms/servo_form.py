# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'servo_form.ui'
#
# Created by: PyQt5 UI code generator 5.15.11
#
# WARNING: Any manual changes made to this file will be lost when pyuic5 is
# run again.  Do not edit this file unless you know what you are doing.


from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_Form(object):
    def setupUi(self, Form):
        Form.setObjectName("Form")
        Form.resize(1285, 410)
        self.horizontalLayout_9 = QtWidgets.QHBoxLayout(Form)
        self.horizontalLayout_9.setObjectName("horizontalLayout_9")
        self.splitter = QtWidgets.QSplitter(Form)
        self.splitter.setOrientation(QtCore.Qt.Horizontal)
        self.splitter.setHandleWidth(10)
        self.splitter.setObjectName("splitter")
        self.layoutWidget = QtWidgets.QWidget(self.splitter)
        self.layoutWidget.setObjectName("layoutWidget")
        self.leftLay = QtWidgets.QVBoxLayout(self.layoutWidget)
        self.leftLay.setSizeConstraint(QtWidgets.QLayout.SetNoConstraint)
        self.leftLay.setContentsMargins(0, 0, 0, 0)
        self.leftLay.setSpacing(6)
        self.leftLay.setObjectName("leftLay")
        self.horizontalLayout_6 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_6.setObjectName("horizontalLayout_6")
        spacerItem = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout_6.addItem(spacerItem)
        self.groupBox = QtWidgets.QGroupBox(self.layoutWidget)
        self.groupBox.setMinimumSize(QtCore.QSize(0, 0))
        self.groupBox.setTitle("")
        self.groupBox.setObjectName("groupBox")
        self.verticalLayout = QtWidgets.QVBoxLayout(self.groupBox)
        self.verticalLayout.setObjectName("verticalLayout")
        self.horizontalLayout = QtWidgets.QHBoxLayout()
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.label = QtWidgets.QLabel(self.groupBox)
        font = QtGui.QFont()
        font.setPointSize(12)
        font.setBold(True)
        font.setWeight(75)
        self.label.setFont(font)
        self.label.setObjectName("label")
        self.horizontalLayout.addWidget(self.label)
        self.kxLine = QtWidgets.QLineEdit(self.groupBox)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.kxLine.sizePolicy().hasHeightForWidth())
        self.kxLine.setSizePolicy(sizePolicy)
        self.kxLine.setObjectName("kxLine")
        self.horizontalLayout.addWidget(self.kxLine)
        self.label_3 = QtWidgets.QLabel(self.groupBox)
        font = QtGui.QFont()
        font.setPointSize(12)
        font.setBold(True)
        font.setWeight(75)
        self.label_3.setFont(font)
        self.label_3.setObjectName("label_3")
        self.horizontalLayout.addWidget(self.label_3)
        self.kvLine = QtWidgets.QLineEdit(self.groupBox)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.kvLine.sizePolicy().hasHeightForWidth())
        self.kvLine.setSizePolicy(sizePolicy)
        self.kvLine.setObjectName("kvLine")
        self.horizontalLayout.addWidget(self.kvLine)
        self.calcLambdaBtn = QtWidgets.QPushButton(self.groupBox)
        self.calcLambdaBtn.setObjectName("calcLambdaBtn")
        self.horizontalLayout.addWidget(self.calcLambdaBtn)
        self.verticalLayout.addLayout(self.horizontalLayout)
        self.horizontalLayout_2 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_2.setObjectName("horizontalLayout_2")
        self.label_2 = QtWidgets.QLabel(self.groupBox)
        font = QtGui.QFont()
        font.setPointSize(12)
        font.setBold(True)
        font.setWeight(75)
        self.label_2.setFont(font)
        self.label_2.setObjectName("label_2")
        self.horizontalLayout_2.addWidget(self.label_2)
        self.l1Line = QtWidgets.QLineEdit(self.groupBox)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.l1Line.sizePolicy().hasHeightForWidth())
        self.l1Line.setSizePolicy(sizePolicy)
        self.l1Line.setObjectName("l1Line")
        self.horizontalLayout_2.addWidget(self.l1Line)
        self.label_4 = QtWidgets.QLabel(self.groupBox)
        font = QtGui.QFont()
        font.setPointSize(12)
        font.setBold(True)
        font.setWeight(75)
        self.label_4.setFont(font)
        self.label_4.setObjectName("label_4")
        self.horizontalLayout_2.addWidget(self.label_4)
        self.l2Line = QtWidgets.QLineEdit(self.groupBox)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.l2Line.sizePolicy().hasHeightForWidth())
        self.l2Line.setSizePolicy(sizePolicy)
        self.l2Line.setObjectName("l2Line")
        self.horizontalLayout_2.addWidget(self.l2Line)
        self.calcKBtn = QtWidgets.QPushButton(self.groupBox)
        self.calcKBtn.setObjectName("calcKBtn")
        self.horizontalLayout_2.addWidget(self.calcKBtn)
        self.verticalLayout.addLayout(self.horizontalLayout_2)
        self.horizontalLayout_3 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_3.setObjectName("horizontalLayout_3")
        spacerItem1 = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout_3.addItem(spacerItem1)
        self.verticalLayout.addLayout(self.horizontalLayout_3)
        self.horizontalLayout_6.addWidget(self.groupBox)
        spacerItem2 = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout_6.addItem(spacerItem2)
        self.leftLay.addLayout(self.horizontalLayout_6)
        self.label_5 = QtWidgets.QLabel(self.layoutWidget)
        self.label_5.setAlignment(QtCore.Qt.AlignCenter)
        self.label_5.setObjectName("label_5")
        self.leftLay.addWidget(self.label_5)
        self.widget = QtWidgets.QWidget(self.splitter)
        self.widget.setObjectName("widget")
        self.rightLay = QtWidgets.QVBoxLayout(self.widget)
        self.rightLay.setContentsMargins(0, 0, 0, 0)
        self.rightLay.setObjectName("rightLay")
        self.horizontalLayout_8 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_8.setObjectName("horizontalLayout_8")
        spacerItem3 = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout_8.addItem(spacerItem3)
        self.groupBox_2 = QtWidgets.QGroupBox(self.widget)
        self.groupBox_2.setMinimumSize(QtCore.QSize(300, 0))
        self.groupBox_2.setTitle("")
        self.groupBox_2.setObjectName("groupBox_2")
        self.horizontalLayout_7 = QtWidgets.QHBoxLayout(self.groupBox_2)
        self.horizontalLayout_7.setObjectName("horizontalLayout_7")
        self.verticalLayout_4 = QtWidgets.QVBoxLayout()
        self.verticalLayout_4.setObjectName("verticalLayout_4")
        self.horizontalLayout_4 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_4.setObjectName("horizontalLayout_4")
        self.label_7 = QtWidgets.QLabel(self.groupBox_2)
        self.label_7.setObjectName("label_7")
        self.horizontalLayout_4.addWidget(self.label_7)
        self.aLine = QtWidgets.QLineEdit(self.groupBox_2)
        self.aLine.setObjectName("aLine")
        self.horizontalLayout_4.addWidget(self.aLine)
        self.verticalLayout_4.addLayout(self.horizontalLayout_4)
        self.horizontalLayout_5 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_5.setObjectName("horizontalLayout_5")
        self.label_8 = QtWidgets.QLabel(self.groupBox_2)
        self.label_8.setObjectName("label_8")
        self.horizontalLayout_5.addWidget(self.label_8)
        self.freqLine = QtWidgets.QLineEdit(self.groupBox_2)
        self.freqLine.setObjectName("freqLine")
        self.horizontalLayout_5.addWidget(self.freqLine)
        self.verticalLayout_4.addLayout(self.horizontalLayout_5)
        self.horizontalLayout_7.addLayout(self.verticalLayout_4)
        self.verticalLayout_2 = QtWidgets.QVBoxLayout()
        self.verticalLayout_2.setObjectName("verticalLayout_2")
        self.sinRadio = QtWidgets.QRadioButton(self.groupBox_2)
        self.sinRadio.setChecked(True)
        self.sinRadio.setObjectName("sinRadio")
        self.verticalLayout_2.addWidget(self.sinRadio)
        self.squareRadio = QtWidgets.QRadioButton(self.groupBox_2)
        self.squareRadio.setObjectName("squareRadio")
        self.verticalLayout_2.addWidget(self.squareRadio)
        self.triangleRadio = QtWidgets.QRadioButton(self.groupBox_2)
        self.triangleRadio.setObjectName("triangleRadio")
        self.verticalLayout_2.addWidget(self.triangleRadio)
        self.horizontalLayout_7.addLayout(self.verticalLayout_2)
        self.verticalLayout_3 = QtWidgets.QVBoxLayout()
        self.verticalLayout_3.setObjectName("verticalLayout_3")
        self.startModelBtn = QtWidgets.QPushButton(self.groupBox_2)
        self.startModelBtn.setObjectName("startModelBtn")
        self.verticalLayout_3.addWidget(self.startModelBtn)
        self.startDeviceBtn = QtWidgets.QPushButton(self.groupBox_2)
        self.startDeviceBtn.setObjectName("startDeviceBtn")
        self.verticalLayout_3.addWidget(self.startDeviceBtn)
        self.horizontalLayout_7.addLayout(self.verticalLayout_3)
        self.horizontalLayout_8.addWidget(self.groupBox_2)
        spacerItem4 = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout_8.addItem(spacerItem4)
        self.rightLay.addLayout(self.horizontalLayout_8)
        self.label_6 = QtWidgets.QLabel(self.widget)
        self.label_6.setAlignment(QtCore.Qt.AlignCenter)
        self.label_6.setObjectName("label_6")
        self.rightLay.addWidget(self.label_6)
        self.horizontalLayout_9.addWidget(self.splitter)

        self.retranslateUi(Form)
        QtCore.QMetaObject.connectSlotsByName(Form)

    def retranslateUi(self, Form):
        _translate = QtCore.QCoreApplication.translate
        Form.setWindowTitle(_translate("Form", "Servo System"))
        self.label.setText(_translate("Form", "<html><head/><body><p><img src=\"data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAABIAAAAWCAYAAADNX8xBAAAAAXNSR0IArs4c6QAAAZlJREFUOE+l1DtIV2EYx/GPiUOYDdplKFCCMiEKotmWKCIIAikDo4ZoCkfpAo1BBAYJlYtUdBOKpiCCEDehNRWtxUSsISKQaoiKJ55TfyT1/Ps/cOA97/ue7/k91zp/rQG7cQTn8bPibMVlXd44gOM4iXHsWPHLRRcKUGyvwhfcxZlaQB2YwCncqQUUrj3AVrytBXQl1WxMSLjag724h5Hl4JUxeo6vmbW1eIItmMRVjJYFzaMfN/AYtzFc1sVC0WbMohNncQlTZSFxrwAdzbRfwzlsw5v/AQ1koLtxH9dTVWlWoeh1Koj2GMQhtOF7WVKA1uMDTqSaPXiV75H2xbYTM/icB43YEKBjeITtFQEewzrsx0HcxA/0ZTJi3Y5NeBY/DtAtHM7NouP34QWeohdz2Yu7supDUSQosnwZjQFqxqd/jI0WfFwiRlFfTejKRv+T/rIxLe5dyKo/XWxUtkhZ2Jqs/nAznt9WDSj67l1Oz6HshJgUYe+rAb1EqIkymc5p0IqLeFgNKJISE/RbqliNeixU69qyMfwFv29L+NjpHvMAAAAASUVORK5CYII=\" width=\"18\" height=\"22\"/></p></body></html>"))
        self.label_3.setText(_translate("Form", "<html><head/><body><p><img src=\"data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAABMAAAAWCAYAAAAinad/AAAAAXNSR0IArs4c6QAAAaBJREFUOE+l1E9oz3Ecx/HHlHZzmJkDZSlrymXLTXERSckcxsq/lVYruSm0aJeVFEUNBzViEXJxkJKcKAepIdmNJYc1Jy7a9K73t323aN/vfu/Dt+/3+3m/n5/X+/15vz9N5m0lutGDs5grrVV6bUqv3ejDMXzAlkrRi5wKWPxegV+4g4FGYZvxEcdxu1FYpDmOTZhsFHYxVa1NUKR9GDtwFy+X2qBcs2f4nae5Co+xEZ9wCa/qwL7jMkbxCGN4sBSgvF4oW4+v2I6TOI/PdUDhW8B6syWu4Aw68GW5sGtZ/EO4h6uprhavUDaRSmKUbmIv2vGnDi1ga/ADR1LVVrzN72iJKhacuXgcxH10lor+Bq3YhT24noN/FKfxNGsbGw2jC/sCdiNesK50U+zEczzBKUxhQ/Zh1HMGgyk5REQvtgWsJRcXXzmrMf2PHN9hBA9zrTn9WsoTUKU2MWrfss4/M2Ab+nGiLuwAziEOqbBb2UZTdWFDCdqfpLhMQ+mL8gRUSTF8ov9iZi9gFq/xvgiuqyzi2nIMozcX2HJg/83iL+XRTTIR/VBmAAAAAElFTkSuQmCC\" width=\"19\" height=\"22\"/></p></body></html>"))
        self.calcLambdaBtn.setText(_translate("Form", "OK"))
        self.label_2.setText(_translate("Form", "<html><head/><body><p><img src=\"data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAABUAAAAWCAYAAAAvg9c4AAAAAXNSR0IArs4c6QAAAXFJREFUSEvN1L9LVnEUx/GXUgYtCU6h4dDgEPlr8AcE5RA4RVFIQiAKLm0ODoHgIKLYIAQtkn+Ai+bS0NAWFi01NToUFEgFioIQJke+wsP1XvPyPINnPee87/l8z+fcOqdHHf79p+ZEOpqycR1jeIIm3MRmGXAe9Bp+YwQv8QCvq4Ue91/BL0xisVbQ4ITsmHKiltD3+IFHtYIOYwZb6K8F9E5aUCwsnNBaLTS2/wr3MIoXuFTGr1lLXcRbPMVX3McaruJnwbSXcSv1HZVkobPYwXwC9OID+vAxA+3AeFIUz9R5nK+E9mAZXfibClrwDY+xUgGNvjiMpZQbzIM24DOeYb2i+QL2MYepAvmhKhc6jSHcyGn8jl08xO00YWVZLrQNn9LVhPxsvMMAVpMbtjMFudBm7OFPgbzwaCO+lJVfxtvZ2sI3PXfQhbT99jyflp22G3fTAYSfn2MDb/L+/GeFx0nXp0M5QHg9Yr8aaOHHDwFZIEEXMiX2hgAAAABJRU5ErkJggg==\" width=\"21\" height=\"22\"/></p></body></html>"))
        self.label_4.setText(_translate("Form", "<html><head/><body><p><img src=\"data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAABUAAAAWCAYAAAAvg9c4AAAAAXNSR0IArs4c6QAAAalJREFUSEut1D9IllEUx/GPmEktCdEQFQUhClEQSP+G/mxOURmRIEQ11RbkEBQOEQoNUSBCFG2Cg5XiZBItQVFDDhJB0FCQERoUCWL/OHCfeHh7XvN9fS88y73n933uOed3bp3FVx1+/yfmn+MQla6tOIMurMV2vKsEXATdhFmcQj+O4uFyoZl+DWbQjRu1ggYn0o5bXqgl9Ck+4nitoJ24is/YWwvowdSgaFg4YfNyodH9OziM07iFxkr8WmqpBozjPF7jCB5gPaYLbtuK5lSil/gRMaXQa/iGvgTYjWfYg+c56GqMYkeK34K3aA/H5KG7cBc7sz9iI97jJIZy0Ig9h7P4hTY8xgSOZdCVeIVLGMmJV2Aevbic29+PT3iT27uHfWjJoD04gW0FdfuA7+jAgTS6RWYYTA3tCGgLXqSpifRLV6R1CPeTG74WxKzDVIqbCugGzOFLGS+GR5swWea8PjnkNsaKul+JxzP9AB5hOBMXPX1LBYf2Jp6k0vzVVQsNXdww7BavWJQg+6arhV7HxTIpXakWuipN408sIPwcIx68+Wqhi9b9D0NdTbQIs2P4AAAAAElFTkSuQmCC\" width=\"21\" height=\"22\"/></p></body></html>"))
        self.calcKBtn.setText(_translate("Form", "OK"))
        self.label_5.setText(_translate("Form", "Root Locus"))
        self.label_7.setText(_translate("Form", "A[rad]"))
        self.label_8.setText(_translate("Form", "freq [Hz]"))
        self.sinRadio.setText(_translate("Form", "Sine"))
        self.squareRadio.setText(_translate("Form", "Square"))
        self.triangleRadio.setText(_translate("Form", "Triangle"))
        self.startModelBtn.setText(_translate("Form", "Start Model"))
        self.startDeviceBtn.setText(_translate("Form", "Start Device"))
        self.label_6.setText(_translate("Form", "Responce"))
