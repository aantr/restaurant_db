from PyQt5.QtCore import Qt, QPoint
from PyQt5.QtGui import QColor
from PyQt5.QtWidgets import QWidget, QGraphicsDropShadowEffect


class BaseWindow(QWidget):
    """Base class of all window widgets, ex. ReportsWidget"""

    def init_ui(self):
        self.setWindowTitle('Restaurant database')

        # Turn off frame
        self.setWindowFlag(Qt.FramelessWindowHint)
        self.setAttribute(Qt.WA_TranslucentBackground)
        # Drop shadow
        shadow = QGraphicsDropShadowEffect(self)
        shadow.setOffset(0, 0)
        shadow.setBlurRadius(15)
        shadow.setColor(QColor(0, 0, 0, 150))
        self.frame.setGraphicsEffect(shadow)
        # Frame move
        self.start_pos = None

    def mousePressEvent(self, event):
        if event.button() == Qt.LeftButton:
            self.start_pos = event.pos()

    def mouseMoveEvent(self, event):
        if self.start_pos:
            current_pos = event.pos()
            delta_pos = current_pos - self.start_pos
            self.move(self.pos() + delta_pos)

    def mouseReleaseEvent(self, event):
        if event.button() == Qt.LeftButton:
            self.start_pos = None

    def get_window_transition(self):
        pass
