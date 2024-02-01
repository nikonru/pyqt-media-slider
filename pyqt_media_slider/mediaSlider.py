from PyQt5.QtWidgets import QSlider
from PyQt5.QtCore import Qt, pyqtSignal

from style import QSlider as QSliderStyle

class MediaSlider(QSlider):
    pressed = pyqtSignal(int)
    dragged = pyqtSignal(int)
    released = pyqtSignal(int)

    def __init__(self):
        super().__init__()
        self.__pressed = False
        self.__initUi()

    def __initUi(self):
        self.setOrientation(Qt.Horizontal)
        self.setStyleSheet(QSliderStyle())
        self.setRange(0, 10000)

        self.setMouseTracking(True)

    def __setPositionAndGetValue(self, e):
        x = e.pos().x()

        mid = self.width() / 2

        if x > mid:
            x += min(3, (x - mid) / (mid / 3))
        elif mid > x > 0:
            x -= min(3, mid / x)

        value = self.minimum() + (self.maximum() - self.minimum()) * x / self.width()
        if value < 0:
            value = 0
        elif value >= self.maximum():
            value = self.maximum()
        value = int(value)
        self.setValue(value)
        return value

    def mousePressEvent(self, e):
        if e.button() == Qt.LeftButton:
            self.__pressed = True
            e.accept()
            value = int(self.__setPositionAndGetValue(e))
            self.pressed.emit(value)

    def mouseMoveEvent(self, e):
        if self.__pressed:
            e.accept()
            value = int(self.__setPositionAndGetValue(e))
            self.dragged.emit(value)
        return super().mouseMoveEvent(e)

    def mouseReleaseEvent(self, e):
        if e.button() == Qt.LeftButton:
            self.__pressed = False
            e.accept()
            value = int(self.__setPositionAndGetValue(e))
            self.released.emit(value)
        return super().mouseReleaseEvent(e)