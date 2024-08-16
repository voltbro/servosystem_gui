import pyqtgraph as pg
from PyQt5.QtCore import *
from PyQt5.QtGui import *

class PlotWidget(pg.PlotWidget):

    sigMouseClicked = pyqtSignal(object)

    def __init__(self, *args, **kwargs):
        super(PlotWidget, self).__init__(*args, **kwargs)

    def mousePressEvent(self, ev : QMouseEvent):
        super().mousePressEvent(ev)
        
        self.sigMouseClicked.emit(ev)

    def dragEnterEvent(self, ev):
        super().dragEnterEvent(ev)
        if ev.mouseButtons() == Qt.LeftButton:
            print("enter")
            ev.accept()
    
    def dragMoveEvent(self, e):
        pass
    
    def dropEvent(self, event : QDropEvent):
        dropped_item = event.source().currentItem().text()
        # print(f"id: {self.id}; dropped: {dropped_item}")
        self.sigDataDropped.emit(self.id, dropped_item)

    def get_id(self):
        return self.id