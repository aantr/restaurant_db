import sqlite3
from PyQt5 import uic

from base_window import BaseWindow


class ReportsWidget(BaseWindow):
    def __init__(self, app):
        super().__init__(app)

        self.con = sqlite3.connect(self.app.DB_FILENAME)
        self.cur = self.con.cursor()

        self.init_ui()

    def init_ui(self):
        uic.loadUi('UI/reports.ui', self)
        super().init_ui()

    def get_window_transition(self):
        return [(self.btn_back.clicked, self.app.get_previous_widget())]
