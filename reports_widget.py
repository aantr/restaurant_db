import sqlite3
from PyQt5 import uic
from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QWidget

from utils import add_shadow


class ReportsWidgetBackButton(QWidget):
    def __init__(self, main_menu_widget):
        super().__init__()
        self.main_menu_widget = main_menu_widget

        self.con = sqlite3.connect('restaurant_db.sqlite')
        self.cur = self.con.cursor()

        self.init_ui()

    def init_ui(self):
        uic.loadUi('reports.ui', self)
        # Turn off frame
        self.setWindowFlag(Qt.FramelessWindowHint)
        self.setAttribute(Qt.WA_TranslucentBackground)
        # Drop shadow
        self.shadow = add_shadow(self, self.frame)

    def get_connects(self):
        return [(self.btn_back.clicked, self.main_menu_widget())]

    @staticmethod
    def add_arguments(f, *args):
        def decorated():
            return f(*args)

        return decorated
