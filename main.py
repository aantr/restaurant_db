import sys
from PyQt5.QtWidgets import QApplication, QMainWindow, QWidget, \
    QPushButton
import sqlite3
from input_restaurant_widget import InputRestaurantWidget


class App(QMainWindow):
    def __init__(self):
        super().__init__()
        self.init()

    def init(self):
        self.setWindowTitle('Restaurant database')
        self.setFixedSize(720, 480)
        self.top_indent = 30

        self.btn_back = QPushButton('<- Back', self)
        self.btn_back.setGeometry(3, 3, 70, self.top_indent - 6)
        self.btn_back.clicked.connect(self.back_clicked)

        self.widget_stack = []
        main_menu = MainMenuWidget(self)
        main_menu.btn_input.clicked.connect(self.input_clicked)
        main_menu.btn_reports.clicked.connect(self.reports_clicked)
        self.set_widget(main_menu)

    def input_clicked(self):
        self.set_widget(InputRestaurantWidget(self))

    def reports_clicked(self):
        self.set_widget(ReportsWidget(self))

    def back_clicked(self):
        self.pop_widget()

    def set_widget(self, widget):
        widget.resize(self.width(), self.height() - self.top_indent)
        widget.move(0, self.top_indent)
        widget.show()
        self.widget_stack.append(widget)
        self.btn_back.setVisible(len(self.widget_stack) > 1)
        for i in self.widget_stack[:-1]:
            i.setVisible(False)

    def pop_widget(self):
        widget = self.widget_stack.pop(-1)
        widget.close()
        self.btn_back.setVisible(len(self.widget_stack) > 1)
        self.widget_stack[-1].setVisible(True)


class MainMenuWidget(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)

        self.init_ui()

    def init_ui(self):
        self.btn_input = QPushButton('Input database', self)
        self.btn_input.resize(150, 70)

        self.btn_reports = QPushButton('Reports', self)
        self.btn_reports.resize(150, 70)

        self.resize(self.size())

    def resize(self, *args):
        super().resize(*args)
        self.btn_input.move((self.width() - self.btn_input.width()) // 2,
                            (self.height() - self.btn_input.height()) // 2 - 50)
        self.btn_reports.move((self.width() - self.btn_reports.width()) // 2,
                              (self.height() - self.btn_reports.height()) // 2 + 30)


class ReportsWidget(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)

        self.con = sqlite3.connect('restaurant_db.sqlite')
        self.cur = self.con.cursor()

        self.init_ui()

    def init_ui(self):
        # пример кнопки, можно удалить
        self.btn = QPushButton('1212', self)
        self.btn.move(100, 100)

        # сделать, например, график заказов за опр. время


def except_hook(cls, exception, traceback):
    sys.__excepthook__(cls, exception, traceback)


if __name__ == '__main__':
    sys.excepthook = except_hook
    app = QApplication(sys.argv)
    ex = App()
    ex.show()
    sys.exit(app.exec())
