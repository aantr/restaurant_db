import sqlite3
import sys
from typing import Type

from PyQt5.QtCore import QDateTime

from base_window import BaseWindow
from menu_widget import MenuWidget
from table_data import DishData, IngredientData, DishTypeData, DishIngredientData, \
    CookData, WaiterData, OrderData, OrderDishData, UnitData
from PyQt5.QtWidgets import QApplication, QMainWindow, QMessageBox


class App(QMainWindow):
    def __init__(self):
        super().__init__()

        # Constants
        self.DB_FILENAME = 'restaurant_db.sqlite'
        self.ACCESS_TABLES_FILENAME = 'admin/access.bin'
        self.PASSWORD_KEY_FILENAME = 'admin/key.bin'
        self.PASSWORD_SALT_FILENAME = 'admin/salt.bin'
        self.LOG_ADMIN_FILENAME = 'admin/log.txt'

        # TableData
        self.TABLE_DATA_CLASSES = [
            OrderData, OrderDishData, IngredientData, DishData, DishIngredientData,
            DishTypeData, CookData, WaiterData, UnitData
        ]

        # Parse all table names in database
        con = sqlite3.connect(self.DB_FILENAME)
        table_names_parse = list(map(lambda x: x[0], con.cursor().execute('''
        select name from sqlite_master where type='table' ''').fetchall()[1:]))
        parse_lower = list(map(str.lower, table_names_parse))
        con.close()
        # Convert table names from TableData to CamelCase
        for i, j in enumerate(self.TABLE_DATA_CLASSES):
            if j.table_name.lower() in parse_lower:
                j.table_name = table_names_parse[parse_lower.index(j.table_name)]

        # Banned tables for user
        self.banned_for_user_table_data = []
        with open(self.ACCESS_TABLES_FILENAME, 'rb') as f:
            for i in f.readlines():
                self.banned_for_user_table_data.append([])
                for j in i.strip(b'\n'):
                    self.banned_for_user_table_data[-1].append(bool(j))

        self.login_as_admin = False
        self.stack_widgets = []

    def show(self):
        self._set(MenuWidget)

    def _set(self, widget_class: Type[BaseWindow]):
        widget = widget_class(self)
        widget.show()
        self.stack_widgets.append(widget)

    def push(self, widget_class: Type[BaseWindow]):
        """Add current widget and hide previous"""
        assert self.stack_widgets
        self.stack_widgets[-1].hide()
        self._set(widget_class)

    def pop(self):
        """Close current widget and show previous"""
        assert self.stack_widgets
        if len(self.stack_widgets) > 1:
            self.stack_widgets.pop(-1).close()

            # Init and show previous showed widget
            self.stack_widgets[-1].__init__(self)
            self.stack_widgets[-1].show()
        else:
            # Exit if current widget is last in stack
            ans = QMessageBox.question(self, 'Question', 'Are you sure you want to exit?',
                                       QMessageBox.Yes, QMessageBox.No)
            if ans == QMessageBox.Yes:
                self.stack_widgets.pop(-1).close()


if __name__ == '__main__':
    def except_hook(cls, exception, traceback):
        sys.__excepthook__(cls, exception, traceback)


    sys.excepthook = except_hook
    app = QApplication(sys.argv)
    ex = App()
    ex.show()
    sys.exit(app.exec())
