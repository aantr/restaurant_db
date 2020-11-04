from PyQt5 import uic
from base_window import BaseWindow
from edit_db_widget import EditDatabaseWidget
from reports_widget import ReportsWidget


class MenuWidget(BaseWindow):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.init_ui()

    def init_ui(self):
        uic.loadUi('menu.ui', self)
        self.setFixedSize(self.size())
        super().init_ui()

        self.btn_exit.clicked.connect(self.exit)

    def get_window_transition(self):
        return [(self.btn_input.clicked,
                 EditDatabaseWidget(MenuWidget)),
                (self.btn_reports.clicked,
                 ReportsWidget(MenuWidget))]
