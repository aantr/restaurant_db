import sys
from PyQt5.QtWidgets import QApplication, QMainWindow

from base_window import BaseWindow
from menu_widget import MenuWidget


class App(QMainWindow):
    def __init__(self):
        super().__init__()

        self.db_filename = 'restaurant_db.sqlite'
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
