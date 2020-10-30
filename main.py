import sys
from PyQt5.QtWidgets import QApplication, QMainWindow
from main_menu_widget import MainMenuWidget


class App(QMainWindow):
    def __init__(self):
        super().__init__()

    def show(self):
        self.main_menu = MainMenuWidget()
        self.create_new(None, self.main_menu)()

    def create_new(self, w1, w2):
        def decorated():
            for i in w2.get_connects():
                i[0].connect(self.create_new(w2, i[1]))
            w2.show()
            if w1:
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
