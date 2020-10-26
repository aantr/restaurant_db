import sys
from PyQt5 import uic
from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QApplication, QMainWindow, QTableWidgetItem, \
    QTableWidget, QMessageBox, QTabWidget, QWidget, QLayout, QBoxLayout, QFormLayout, QPushButton, QVBoxLayout, \
    QHBoxLayout, QGridLayout
from custom_dialog import CustomDialog
from table_data import *
import sqlite3


class App(QMainWindow):
    def __init__(self):
        super().__init__()
        self.init()

    def init(self):
        # uic.loadUi('main.ui', self)
        self.setWindowTitle('Title')
        self.setFixedSize(720, 480)

        self.con = sqlite3.connect('restaurant_db.sqlite')
        self.cur = self.con.cursor()

        self.tab_widget = QTabWidget(self)
        self.tab_widget.resize(self.size())

        self.table_data_types = [IngredientData, DishData, DishTypeData, DishIngredientData]
        self.table_names = [i.table_name for i in self.table_data_types]

        for table_name, table_data_type in zip(self.table_names, self.table_data_types):
            exec(f'self.{table_name} = QTableWidget(self)')
            current_table = eval(f'self.{table_name}')
            btn_table_add = QPushButton('Add item', self)
            btn_table_edit = QPushButton('Edit item', self)
            btn_table_delete = QPushButton('Delete items', self)

            tab = QWidget()
            layout = QGridLayout()
            n_cols = 20
            layout.addWidget(current_table, 1, 0, 1, n_cols)
            layout.addWidget(btn_table_add, 0, 0)
            layout.addWidget(btn_table_edit, 0, 1)
            layout.addWidget(btn_table_delete, 0, 2)
            layout.addWidget(QWidget(), 0, n_cols - 1)
            tab.setLayout(layout)
            self.tab_widget.addTab(tab, table_name.capitalize())

            table_data = table_data_type(current_table, self.cur)
            for i, j in zip([btn_table_add, btn_table_edit, btn_table_delete],
                            [self.table_add_clicked, self.table_edit_clicked, self.table_delete_clicked]):
                i.clicked.connect(self.add_arguments(j, table_data))
            self.table_update(table_data)

    def table_add_clicked(self, table_data):
        table_data.widget.clearSelection()
        w = CustomDialog(self, *table_data.dialog_items(),
                         window_title='Add item')
        res = w.result()
        if res:
            self.cur.execute(table_data.add(res))
            self.con.commit()
        self.table_update(table_data)

    def table_edit_clicked(self, table_data):
        rows = self.get_selected_rows(table_data.widget)
        if not rows:
            return
        i, row = rows[0]
        table_data.widget.selectRow(i)
        w = CustomDialog(self, *table_data.dialog_items(row),
                         window_title='Edit item')
        res = w.result()
        if res:
            res.insert(0, row[0])
            print(table_data.edit(res))
            self.cur.execute(table_data.edit(res))
            self.con.commit()
        self.table_update(table_data)

    def table_delete_clicked(self, table_data):
        rows = self.get_selected_rows(table_data.widget)
        if not rows:
            return
        rows = list(map(lambda x: x[1], rows))
        ans = QMessageBox.question(
            self, '', 'Are you sure you want to delete all selected rows?',
            QMessageBox.Yes, QMessageBox.No)
        if ans == QMessageBox.Yes:
            self.cur.execute(table_data.delete(rows))
            self.con.commit()
        self.table_update(table_data)

    def table_update(self, table_data):
        data = self.cur.execute(table_data.update()).fetchall()
        head = list(map(lambda x: x[0].capitalize(), self.cur.description))
        self.fill_table(table_data.widget, head, data)

    @staticmethod
    def add_arguments(f, *args):
        def decorated():
            return f(*args)

        return decorated

    @staticmethod
    def get_selected_rows(table: QTableWidget):
        n_rows = set([i.row() for i in table.selectedItems()])
        rows = [(i, [table.item(i, j).text() for
                     j in range(table.columnCount())]) for i in n_rows]
        return rows

    @staticmethod
    def fill_table(table, title=(), data=()):
        table.clear()
        table.setColumnCount(len(title))
        table.setHorizontalHeaderLabels(title)
        table.setRowCount(len(data))
        for i, row in enumerate(data):
            for j in range(len(row)):
                elem = row[j]
                item = QTableWidgetItem(str(elem))
                item.setFlags(Qt.ItemIsSelectable | Qt.ItemIsEnabled)
                table.setItem(i, j, item)


def except_hook(cls, exception, traceback):
    sys.__excepthook__(cls, exception, traceback)


if __name__ == '__main__':
    sys.excepthook = except_hook
    app = QApplication(sys.argv)
    ex = App()
    ex.show()
    sys.exit(app.exec())
