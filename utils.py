from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QTableWidget, QTableWidgetItem, QMessageBox, QDateTimeEdit


def add_arguments(f, *args):
    def decorated():
        return f(*args)

    return decorated


def permission_denied_msg(w):
    QMessageBox.critical(w, 'Error', 'Permission denied')


def date_time_format():
    return 'yyyy/MM/dd hh:mm'


def get_selected_rows(table: QTableWidget):
    """Returns selected rows in QTableWidget in format:
    [(3, [el1, el2, el3]),
    (4, [el1, el2, el3]),
    (5, [el1, el2, el3])
    ...]"""
    n_rows = set([i.row() for i in table.selectedItems()])
    rows = [(i, [table.item(i, j).text() for
                 j in range(table.columnCount())]) for i in n_rows]
    return rows


def fill_table(table: QTableWidget, head=(), data=()):
    """Clear table and fill with title and data"""
    table.clear()
    table.setColumnCount(len(head))
    table.setHorizontalHeaderLabels(head)
    table.setRowCount(len(data))
    for i, row in enumerate(data):
        for j in range(len(row)):
            elem = row[j]
            item = QTableWidgetItem(str(elem))
            item.setFlags(Qt.ItemIsSelectable | Qt.ItemIsEnabled)
            table.setItem(i, j, item)
    table.resizeColumnsToContents()
    for i in range(table.colorCount()):
        table.setColumnWidth(i, table.columnWidth(i) + 50)
