from PyQt5 import uic

from base_window import BaseWindow


class HelpWidget(BaseWindow):
    def __init__(self, app):
        super().__init__(app)

        self.init_ui()

    def init_ui(self):
        uic.loadUi('UI/help.ui', self)
        super().init_ui()

    def get_window_transition(self):
        return [(self.btn_back.clicked, self.app.get_previous_widget())]
