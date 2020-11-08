import sqlite3
import sys
from PyQt5.QtWidgets import QApplication, QMainWindow

from base_window import BaseWindow
from menu_widget import MenuWidget
from table_data import DishData, IngredientData, DishTypeData, DishIngredientData, \
    CookData, WaiterData, OrderData, OrderDishData, UnitData


class App(QMainWindow):
    def __init__(self):
        super().__init__()

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
        self.create_new(None, MenuWidget)()

    def create_new(self, w1: BaseWindow, w2_class):
        def decorated():
            w2 = w2_class(self)
            for event, new_widget in w2.get_window_transition():
                event.connect(self.create_new(w2, new_widget))
            w2.show()
            if w1:
                w1.close()
            self.stack_widgets.append(w2_class)

        return decorated

    def change_window(self, w1, w2_class):
        w2 = w2_class(self)
        w2.show()
        if w1:
            w1.close()
        self.stack_widgets.append(w2_class)

    def get_previous_widget(self):
        return self.stack_widgets.pop(-1)


if __name__ == '__main__':
    def except_hook(cls, exception, traceback):
        sys.__excepthook__(cls, exception, traceback)


    sys.excepthook = except_hook
    app = QApplication(sys.argv)
    ex = App()
    ex.show()
    sys.exit(app.exec())
