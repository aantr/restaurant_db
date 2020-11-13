from PyQt5 import uic
from PyQt5.QtGui import QColor, QPalette
from PyQt5.QtWidgets import QStyle

from admin_panel_widget import AdminPanelWidget
from base_window import BaseWindow
from cook_panel_widget import CookPanelWidget
from edit_db_widget import EditDatabaseWidget
from reports_widget import ReportsWidget
from utils import permission_denied_msg


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

        self.btn_edit.clicked.connect(self.edit_clicked)
        self.btn_cook.clicked.connect(self.cook_clicked)
        self.btn_reports.clicked.connect(self.reports_clicked)
        self.btn_admin.clicked.connect(self.admin_clicked)

        self.btn_exit.clicked.connect(self.app.pop)

    def edit_clicked(self):
        self.app.push(EditDatabaseWidget)

    def cook_clicked(self):
        self.app.push(CookPanelWidget)

    def reports_clicked(self):
        if self.app.login_as_admin:
            self.app.push(ReportsWidget)
        else:
            permission_denied_msg(self)

    def admin_clicked(self):
        self.app.push(AdminPanelWidget)
