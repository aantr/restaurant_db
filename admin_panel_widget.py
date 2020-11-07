import os

from PyQt5 import uic
import hashlib

from PyQt5.QtCore import Qt, QDateTime
from PyQt5.QtWidgets import QMessageBox, QLineEdit, QDateTimeEdit

from base_window import BaseWindow
from utils import date_time_format


class AdminPanelWidget(BaseWindow):
    def __init__(self, app):
        super().__init__(app)

        self.hash_name = 'sha256'
        self.iterations = 10 ** 6

        self.init_ui()

    def init_ui(self):
        uic.loadUi('UI/admin_panel.ui', self)
        super().init_ui()

        self.btn_login.clicked.connect(self.login_clicked)
        self.line_login.returnPressed.connect(self.login_clicked)
        self.btn_change.clicked.connect(self.change_clicked)
        self.update_widgets_enabled()

    def check_password(self, password):
        with open('admin/key.hash', 'rb') as f:
            key = f.read()
        with open('admin/salt.hash', 'rb') as f:
            salt = f.read()
        new_key = hashlib.pbkdf2_hmac(self.hash_name, password.encode('utf-8'),
                                      salt, self.iterations)
        return key == new_key

    def apply_new_password(self, password):
        salt = os.urandom(32)
        key = hashlib.pbkdf2_hmac(self.hash_name, password.encode('utf-8'),
                                  salt, self.iterations)
        with open('admin/key.hash', 'wb') as f:
            f.write(key)
        with open('admin/salt.hash', 'wb') as f:
            f.write(salt)

    def login_clicked(self):
        correct = self.check_password(self.line_login.text())
        self.clear_lines()
        if correct:
            self.app.login_as_admin = True
            self.update_widgets_enabled()
            self.add_log()
            QMessageBox.information(self, 'Information',
                                    'Successful logged in')
        else:
            QMessageBox.critical(self, 'Error',
                                 'Incorrect password')

    def change_clicked(self):
        line1 = self.line_current.text()
        line2 = self.line_new1.text()
        line3 = self.line_new2.text()
        self.clear_lines()
        if not self.check_password(line1):
            QMessageBox.critical(self, 'Error',
                                 'Incorrect current password')
            return
        if line2 != line3:
            QMessageBox.critical(self, 'Error',
                                 'New passwords don`t match')
            return
        password = line2
        if len(password) < 4:
            QMessageBox.critical(self, 'Error',
                                 'Length of password must be greater then 3')
            return
        self.apply_new_password(password)
        QMessageBox.information(self, 'Information',
                                'Successful changed password')

    def update_widgets_enabled(self):
        b = self.app.login_as_admin
        for i in [self.line_login, self.btn_login]:
            i.setDisabled(b)
        for i in [self.line_current, self.line_new1,
                  self.line_new2, self.btn_change]:
            i.setDisabled(not b)

    def clear_lines(self):
        for i in [self.line_login, self.line_current,
                  self.line_new1, self.line_new2]:
            i.setText('')

    def add_log(self):
        with open('admin/log.txt', 'a') as f:
            f.write(QDateTime.currentDateTime().toString(
                date_time_format()))
            f.write('\n')

    def get_window_transition(self):
        return [(self.btn_back.clicked, self.app.get_previous_widget())]
