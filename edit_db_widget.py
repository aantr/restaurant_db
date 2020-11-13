from PyQt5 import uic
from PyQt5.QtWidgets import QMessageBox, QWidget, QPushButton, QGridLayout, QTableWidget, QTabWidget

from base_window import BaseWindow
from table_data import BaseTableData
from custom_dialog import CustomDialog
import sqlite3

from utils import add_arguments, fill_table, get_selected_rows, permission_denied_msg


class EditDatabaseWidget(BaseWindow):
    def __init__(self, app):
        super().__init__(app)

        self.con = sqlite3.connect(self.app.DB_FILENAME)
        self.cur = self.con.cursor()

        self.tables = []

        self.init_ui()

    def init_ui(self):
        uic.loadUi('UI/edit_db.ui', self)
        super().init_ui()

        for table_data_type in self.app.TABLE_DATA_CLASSES:
            table_name = table_data_type.table_name
            exec(f'self.{table_name} = QTableWidget(self)')
            current_table: QTableWidget = eval(f'self.{table_name}')

            # Add, Edit, Delete buttons
            btn_table_add = QPushButton('Add item', self)
            btn_table_edit = QPushButton('Edit item', self)
            btn_table_delete = QPushButton('Delete items', self)

            # Tab
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
            for i, j in zip(enumerate([btn_table_add, btn_table_edit, btn_table_delete]),
                            [self.table_add_clicked, self.table_edit_clicked,
                             self.table_delete_clicked]):
                # Create permission control
                i[1].clicked.connect(add_arguments(
                    self.permission_control(j, table_data, i[0])))
                # i.clicked.connect(add_arguments(j, table_data))

            # Edit if double clicked on item
            current_table.doubleClicked.connect(add_arguments(
                self.permission_control(self.table_edit_clicked, table_data, 1)))

            self.tables.append(table_data)

        # Update if tab changed
        def tab_changed(index):
            self.table_update(self.tables[index])

        self.tab_widget.currentChanged.connect(tab_changed)
        tab_changed(self.tab_widget.currentIndex())

        self.btn_back.clicked.connect(self.app.pop)

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

    def table_edit_clicked(self, table_data: BaseTableData):
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

    def table_delete_clicked(self, table_data: BaseTableData):
        """Deletes selected rows in table with TableData"""
        rows = get_selected_rows(table_data.widget)
        if not rows:
            # If rows not selected
            QMessageBox.information(self, 'Information',
                                    f'No selected rows')
            return
        rows = list(map(lambda x: x[1], rows))
        ans = QMessageBox.question(
            self, 'Question', f'Are you sure you want to delete '
                              f'{len(rows)} selected row{"s" * int(len(rows) > 1)}\n'
                              f'and all records with this item?',
            QMessageBox.Yes, QMessageBox.No)
        if ans == QMessageBox.Yes:
            if table_data.check_usage(rows):
                QMessageBox.critical(
                    self, 'Error', f'Selected items are used in another table',
                    QMessageBox.Ok)
                ans = False

        if ans == QMessageBox.Yes:
            self.cur.execute(table_data.delete(rows))
            self.con.commit()
            self.table_update(table_data)

    def table_update(self, table_data: BaseTableData):
        """Fill table with TableData"""
        data = self.cur.execute(table_data.update()).fetchall()
        head = list(map(lambda x: x[0].capitalize(), self.cur.description))

        fill_table(table_data.widget, head, data)

    def permission_control(self, f, table_data: BaseTableData, btn):
        """Check for permission before call the function"""

        def decorated():
            if not self.app.login_as_admin and \
                    self.app.banned_for_user_table_data[btn][
                        self.app.TABLE_DATA_CLASSES.index(type(table_data))]:
                permission_denied_msg(self)
                return
            f(table_data)

        return decorated
