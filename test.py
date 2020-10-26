from PyQt5.QtCore import QSize
from PyQt5.QtWidgets import *
import sys
from PIL.ImageQt import ImageQt
from PyQt5 import uic
from PyQt5.QtGui import QPixmap
from PyQt5.QtWidgets import QApplication, QMainWindow, QTableWidgetItem
import PyQt5.QtWidgets as QtWidgets
import PyQt5.QtCore as QtCore

class Widget(QMainWindow):
    def __init__(self):
        super().__init__()
        self.init()

    def init(self):
        self.setWindowTitle('Title')
        self.resize(500, 300)
        self.tabs = QTabWidget(self)
        self.tabs.resize(400, 200)

        self.tab1 = QWidget()
        layout = QFormLayout()
        layout.addRow("Name", QLineEdit())
        layout.addRow("Address", QLineEdit())
        self.tab1.setLayout(layout)

        self.tab2 = QWidget()
        layout = QFormLayout()
        layout.addRow("Name", QLineEdit())
        layout.addRow("Address", QLineEdit())

        self.tabs.addTab(self.tab1, '1')
        self.tabs.addTab(self.tab2, '2')


    def clicked(self):
        ...

    def apply_image(self, label, image):
        label.setPixmap(QPixmap.fromImage(ImageQt.ImageQt(image)))

    def fill_table(self, title=(), data=()):
        self.table.clear()
        self.table.setColumnCount(len(title))
        self.table.setHorizontalHeaderLabels(title)
        self.table.setRowCount(len(data))
        for i, row in enumerate(data):
            for j in range(len(row)):
                elem = row[j]
                item = QTableWidgetItem(str(elem))
                self.table.setItem(i, j, item)


def except_hook(cls, exception, traceback):
    sys.__excepthook__(cls, exception, traceback)


if __name__ == '__main__':
    sys.excepthook = except_hook
    app = QApplication(sys.argv)
    ex = Widget()
    ex.show()
    sys.exit(app.exec())
