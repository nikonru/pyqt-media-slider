from PyQt5.QtWidgets import QSlider
from PyQt5.QtCore import Qt, pyqtSignal


def qSliderStyle():
    return """
QSlider {
    margin: 3px;
}

QSlider::groove:horizontal {
    border: 1px solid #999999;
    height: 3px;
    background: qlineargradient(x1:0, y1:0, x2:0, y2:1, stop:0 #B1B1B1, stop:1 #c4c4c4);
    margin: 2px;
}

QSlider::handle:horizontal {
    background: qlineargradient(x1:0, y1:0, x2:1, y2:1, stop:0 #b4b4b4, stop:1 #8f8f8f);
    border: 1px solid #5c5c5c;
    width: 6px;
    margin: -6px;
    border-radius: 3px;
}
    """


class MediaSlider(QSlider):
    pressed = pyqtSignal(int)
    dragged = pyqtSignal(int)
    released = pyqtSignal(int)

    def __init__(self, style=None):
        super().__init__()
        self.__pressed = False
        if not style:
            self.__initUi(qSliderStyle())
        else:
            self.__initUi(style)

    def __initUi(self, style):
        self.setOrientation(Qt.Horizontal)
        self.setStyleSheet(style)
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