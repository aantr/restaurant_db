import os

from PyQt5 import uic
import hashlib

from PyQt5.QtCore import Qt, QDateTime
from PyQt5.QtWidgets import QMessageBox, QLineEdit, QDateTimeEdit, QFrame, QCheckBox, QLabel, QListWidget, \
    QListWidgetItem

from base_window import BaseWindow
from utils import date_time_format


class AdminPanelWidget(BaseWindow):
    def __init__(self, app):
        super().__init__(app)

        self.hash_name = 'sha256'
        self.iterations = 10 ** 5 * 5

        self.init_ui()

    def init_ui(self):
        uic.loadUi('UI/admin_panel.ui', self)
        super().init_ui()

        self.access_check_boxes = [[], [], []]
        self.frame_access: QFrame

        for k in range(3):
            label = QLabel(['Add', 'Edit', 'Delete'][k], self.frame_access)
            label.move(125 + 35 * k, 40)

        for i, j in enumerate(self.app.TABLE_DATA_CLASSES):
            label = QLabel(j.table_name, self.frame_access)
            label.move(10, 70 + 25 * i)
            label.resize(90, 30)
            label.setAlignment(Qt.AlignRight)

            for k in range(3):
                cb = QCheckBox(self.frame_access)
                cb.move(130 + 35 * k, 70 + 25 * i)
                cb.setChecked(self.app.banned_for_user_table_data[k][i])
                cb.stateChanged.connect(self.check_box_changed(i, k))
                self.access_check_boxes[k].append(cb)

        self.fill_log()
        self.btn_login.clicked.connect(self.login_clicked)
        self.line_login.returnPressed.connect(self.login_clicked)
        self.line_login.setFocus()
        self.btn_change.clicked.connect(self.change_clicked)
        self.btn_logout.clicked.connect(self.logout_clicked)
        self.update_widgets_enabled()

        self.btn_back.clicked.connect(self.app.pop)

    def check_box_changed(self, table, cb):
        def decorated(value):
            self.app.banned_for_user_table_data[cb][table] = bool(value)
            self.write_banned_tables()

        return decorated

    def write_banned_tables(self):
        with open(self.app.ACCESS_TABLES_FILENAME, 'wb') as f:
            for i in self.app.banned_for_user_table_data:
                f.write(bytearray(map(int, i)))
                f.write(b'\n')

    def check_password(self, password):
        with open(self.app.PASSWORD_KEY_FILENAME, 'rb') as f:
            key = f.read()
        with open(self.app.PASSWORD_SALT_FILENAME, 'rb') as f:
            salt = f.read()
        new_key = hashlib.pbkdf2_hmac(self.hash_name, password.encode('utf-8'),
                                      salt, self.iterations)
        return key == new_key

    def apply_new_password(self, password):
        salt = os.urandom(32)
        key = hashlib.pbkdf2_hmac(self.hash_name, password.encode('utf-8'),
                                  salt, self.iterations)
        with open(self.app.PASSWORD_KEY_FILENAME, 'wb') as f:
            f.write(key)
        with open(self.app.PASSWORD_SALT_FILENAME, 'wb') as f:
            f.write(salt)

    def login_clicked(self):
        correct = self.check_password(self.line_login.text())
        self.clear_lines()
        if correct:
            self.app.login_as_admin = True
            self.update_widgets_enabled()
            self.add_log()
        else:
            QMessageBox.critical(self, 'Error',
                                 'Incorrect password')

    def logout_clicked(self):
        self.app.login_as_admin = False
        self.line_login.setFocus()
        self.update_widgets_enabled()

    def change_clicked(self):
        line1 = self.line_current.text()
        line2 = self.line_new1.text()
        line3 = self.line_new2.text()
        self.clear_lines()
        if not self.check_password(line1):
            QMessageBox.critical(self, 'Error', 'Incorrect current password')
            return
        if line2 != line3:
            QMessageBox.critical(self, 'Error', 'New passwords don`t match')
            return
        if self.check_password(line2):
            QMessageBox.critical(self, 'Error', 'New and old passwords are the same')
            return
        password = line2
        if len(password) < 4:
            QMessageBox.critical(self, 'Error', 'Length of password must be greater then 3')
            return
        self.apply_new_password(password)
        QMessageBox.information(self, 'Information', 'Successful changed password')

    def update_widgets_enabled(self):
        b = self.app.login_as_admin
        for i in [self.frame_login]:
            i.setDisabled(b)
        for i in [self.frame_access, self.frame_change]:
            i.setDisabled(not b)

    def clear_lines(self):
        for i in [self.line_login, self.line_current,
                  self.line_new1, self.line_new2]:
            i.setText('')

    def fill_log(self):
        self.list_log.clear()
        with open(self.app.LOG_ADMIN_FILENAME, 'r') as f:
            for i in f.readlines():
                dt = QDateTime.fromString(i.strip('\n'), date_time_format())
                if dt.isValid():
                    self.list_log.addItem(
                        QListWidgetItem(dt.toString(date_time_format())))

    def add_log(self):
        with open(self.app.LOG_ADMIN_FILENAME, 'a') as f:
            f.write(QDateTime.currentDateTime().toString(
                date_time_format()))
            f.write('\n')
        self.fill_log()
