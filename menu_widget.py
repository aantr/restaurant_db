from PyQt5 import uic
from PyQt5.QtGui import QColor, QPalette
from PyQt5.QtWidgets import QStyle

from admin_panel_widget import AdminPanelWidget
from base_window import BaseWindow
from edit_db_widget import EditDatabaseWidget
from help_widget import HelpWidget
from reports_widget import ReportsWidget


class MenuWidget(BaseWindow):
    def __init__(self, app):
        super().__init__(app)
        self.init_ui()

    def init_ui(self):
        uic.loadUi('UI/menu.ui', self)
        super().init_ui()

        if self.app.login_as_admin:
            self.label_info.setText('Logged in as: <b>Admin</b>')
        else:
            self.label_info.setText('Logged in as: <b>User</b>')

        self.btn_admin.clicked.connect(self.admin_clicked)
        self.btn_exit.clicked.connect(self.exit)

    def admin_clicked(self):
        if self.app.login_as_admin:
            ...
        else:
            ...

    def get_window_transition(self):
        return [(self.btn_input.clicked,
                 EditDatabaseWidget),
                (self.btn_reports.clicked,
                 ReportsWidget),
                (self.btn_help.clicked,
                 HelpWidget),
                (self.btn_admin.clicked,
                 AdminPanelWidget)]
