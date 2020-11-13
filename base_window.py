from PyQt5.QtCore import Qt, QPoint
from PyQt5.QtGui import QColor, QIcon, QPixmap
from PyQt5.QtWidgets import QWidget, QGraphicsDropShadowEffect, QMessageBox, \
    QFrame, QMainWindow


class BaseWindow(QMainWindow):
    """Base class of all window widgets"""
    frame: QFrame

    def __init__(self, app):
        super().__init__()
        self.app = app

    def init_ui(self):
        self.setWindowTitle('Restaurant app')

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

        # White background on QMessageBox and QDialog
        self.setStyleSheet('QMessageBox{background: #fff;} '
                           'QDialog{background: #fff;}')

    # Drag window
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

    # Back return on ESC press
    def keyPressEvent(self, event):
        if event.key() == Qt.Key_Escape:
            self.app.pop()
