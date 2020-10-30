from PyQt5 import uic
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QColor
from PyQt5.QtWidgets import QWidget, QGraphicsDropShadowEffect
from input_restaurant_widget import InputRestaurantWidgetBackButton
from reports_widget import ReportsWidgetBackButton
from utils import add_shadow


class MainMenuWidget(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.init_ui()

    def init_ui(self):
        uic.loadUi('menu.ui', self)
        self.setFixedSize(self.size())

        # Turn off frame
        self.setWindowFlag(Qt.FramelessWindowHint)
        self.setAttribute(Qt.WA_TranslucentBackground)
        # Drop shadow
        self.shadow = add_shadow(self, self.frame)

        self.btn_exit.clicked.connect(self.close)

    def get_connects(self):
        return [(self.btn_input.clicked,
                 InputRestaurantWidgetBackButton(MainMenuWidget)),
                (self.btn_reports.clicked,
                 ReportsWidgetBackButton(MainMenuWidget))]

    def keyPressEvent(self, event):
        if event.key() == Qt.Key_Escape:
            self.close()
