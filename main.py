import sys
from PyQt5.QtWidgets import QApplication, QMainWindow

from edit_db_widget import EditDatabaseWidget
from menu_widget import MenuWidget


class App(QMainWindow):
    def __init__(self):
        super().__init__()

    def show(self):
        self.widget = MenuWidget()

        for event, new_widget in self.widget.get_window_transition():
            event.connect(self.create_new(self.widget, new_widget))
        self.widget.show()

    def create_new(self, w1, w2):
        def decorated():
            for event, new_widget in w2.get_window_transition():
                event.connect(self.create_new(w2, new_widget))
            w2.show()
            w1.close()

        return decorated


if __name__ == '__main__':
    def except_hook(cls, exception, traceback):
        sys.__excepthook__(cls, exception, traceback)


    sys.excepthook = except_hook
    app = QApplication(sys.argv)
    ex = App()
    ex.show()
    sys.exit(app.exec())
