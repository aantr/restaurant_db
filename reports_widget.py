import sqlite3
from PyQt5 import uic

from base_window import BaseWindow


class ReportsWidget(BaseWindow):
    def __init__(self, main_menu_widget):
        super().__init__()
        self.previous_widget = main_menu_widget

        self.con = sqlite3.connect('restaurant_db.sqlite')
        self.cur = self.con.cursor()

        self.init_ui()

    def init_ui(self):
        uic.loadUi('reports.ui', self)
        super().init_ui()

    def get_window_transition(self):
        return [(self.btn_back.clicked, self.previous_widget())]

    @staticmethod
    def add_arguments(f, *args):
        def decorated():
            return f(*args)

        return decorated
