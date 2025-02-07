from PyQt5.QtCore import QObject, pyqtSignal

class ConnectStatu(QObject):
    valueChanged = pyqtSignal()
    def __init__(self, parent=None):
        super().__init__(parent)
        self._statu = 0 #0为未连接，1为连接

    @property
    def value(self):
        return self._statu

    @value.setter
    def value(self, new_value):
        self._statu = new_value
        self.valueChanged.emit()