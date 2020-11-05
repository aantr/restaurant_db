from PyQt5.QtCore import Qt, QPoint
from PyQt5.QtGui import QColor, QIcon, QPixmap
from PyQt5.QtWidgets import QWidget, QGraphicsDropShadowEffect, QMessageBox, QFrame, QMainWindow


class BaseWindow(QMainWindow):
    """Base class of all window widgets, ex. ReportsWidget"""
    frame: QFrame

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

        # Design
        # White background on QMessageBox and QDialog
        self.setStyleSheet('QMessageBox{background: #fff;} '
                           'QDialog{background: #fff;}')

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

    def keyPressEvent(self, event):
        if event.key() == Qt.Key_Escape:
            self.exit()

    def exit(self):
        ans = QMessageBox.question(self, 'Question', 'Are you sure you want to exit?',
                                   QMessageBox.Yes, QMessageBox.No)
        if ans == QMessageBox.Yes:
            self.close()

    def get_window_transition(self):
        pass
