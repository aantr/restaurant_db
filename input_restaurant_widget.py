from PyQt5.QtCore import Qt
from PyQt5 import uic
from PyQt5.QtWidgets import QMessageBox, QWidget, QPushButton, QGridLayout, QTableWidget
from table_data import DishData, IngredientData, DishTypeData, DishIngredientData, \
    CookData, WaiterData, OrderData, OrderDishData
from custom_dialog import CustomDialog
import sqlite3

from utils import add_arguments, fill_table, get_selected_rows, add_shadow


class InputRestaurantWidgetBackButton(QWidget):
    def __init__(self, main_menu_widget):
        super().__init__()
        self.main_menu_widget = main_menu_widget

        self.con = sqlite3.connect('restaurant_db.sqlite')
        self.cur = self.con.cursor()

        self.init_ui()

    def init_ui(self):
        uic.loadUi('input_restaurant.ui', self)
        self.setFixedSize(self.size())

        # Turn off frame
        self.setWindowFlag(Qt.FramelessWindowHint)
        self.setAttribute(Qt.WA_TranslucentBackground)
        # Drop shadow
        self.shadow = add_shadow(self, self.frame)

        self.cur.execute('''select name from sqlite_master where type='table' ''')
        # Parse all table names in database
        table_names_parse = list(map(lambda x: x[0], self.cur.fetchall()[1:]))
        parse_lower = list(map(str.lower, table_names_parse))

        # TableData
        self.table_data_types = [DishData, IngredientData, DishTypeData, DishIngredientData,
                                 CookData, WaiterData, OrderData, OrderDishData]

        # Table names from TableData
        self.table_names = [i.table_name for i in self.table_data_types]
        for i, j in enumerate(self.table_names.copy()):
            if j.lower() in parse_lower:
                self.table_names[i] = table_names_parse[parse_lower.index(j)]

        for table_name, table_data_type in zip(self.table_names, self.table_data_types):
            exec(f'self.{table_name} = QTableWidget(self)')
            current_table: QTableWidget = eval(f'self.{table_name}')
            btn_table_add = QPushButton('Add item', self)
            btn_table_edit = QPushButton('Edit item', self)
            btn_table_delete = QPushButton('Delete items', self)

            # Add, Edit, Delete buttons
            tab = QWidget()
            layout = QGridLayout()
            n_cols = 20
            layout.addWidget(current_table, 1, 0, 1, n_cols)
            layout.addWidget(btn_table_add, 0, 0)
            layout.addWidget(btn_table_edit, 0, 1)
            layout.addWidget(btn_table_delete, 0, 2)
            layout.addWidget(QWidget(), 0, n_cols - 1)
            tab.setLayout(layout)
            self.tab_widget.addTab(tab, table_name)

            # Create TableData object
            table_data = table_data_type(current_table, self.cur)
            for i, j in zip([btn_table_add, btn_table_edit, btn_table_delete],
                            [self.table_add_clicked, self.table_edit_clicked,
                             self.table_delete_clicked]):
                i.clicked.connect(add_arguments(j, table_data))

            # Edit if double clicked on item
            current_table.doubleClicked.connect(add_arguments(
                self.table_edit_clicked, table_data))

            self.table_update(table_data)

    def get_connects(self):
        return [(self.btn_back.clicked, self.main_menu_widget())]

    def close(self):
        super().close()
        self.con.close()

    def table_add_clicked(self, table_data):
        """Add a row in table with TableData"""
        table_data.widget.clearSelection()
        w = CustomDialog(self, *table_data.dialog_items(),
                         window_title='Add item')
        res = w.result()
        if res:  # If ok pressed
            self.cur.execute(table_data.add(res))
            self.con.commit()
        self.table_update(table_data)

    def table_edit_clicked(self, table_data):
        """Edits selected rows in table with TableData"""
        rows = get_selected_rows(table_data.widget)
        if not rows:
            # If rows not selected
            QMessageBox.information(self, 'Information',
                                    f'No selected rows')
            return
        i, row = rows[0]
        table_data.widget.selectRow(i)
        w = CustomDialog(self, *table_data.dialog_items(row),
                         window_title='Edit item')
        res = w.result()
        if res:  # If ok pressed
            res.insert(0, row[0])
            self.cur.execute(table_data.edit(res))
            self.con.commit()
        self.table_update(table_data)

    def table_delete_clicked(self, table_data):
        """Deletes selected rows in table with TableData"""
        rows = get_selected_rows(table_data.widget)
        if not rows:
            # If rows not selected
            QMessageBox.information(self, 'Information',
                                    f'No selected rows')
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
        """Fill table with TableData"""
        data = self.cur.execute(table_data.update()).fetchall()
        head = list(map(lambda x: x[0].capitalize(), self.cur.description))
        fill_table(table_data.widget, head, data)