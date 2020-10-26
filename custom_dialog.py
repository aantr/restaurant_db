from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QWidget, QLineEdit, QComboBox, QDialog, \
    QPushButton, QLabel, QMessageBox


class CustomDialogItem:
    def __init__(self, name, widget_type, correct, default):
        self.name = name
        self.widget_type = widget_type
        self.widget: QWidget = None
        self.default = default
        self.correct_func = correct if correct is not None else lambda x: True

    def _set_widget(self, parent):
        self.widget = self.widget_type(parent)
        self.init_widget()
        self.set_default_data(self.default)

    def correct(self):
        try:
            return self.correct_func(self.get_data())
        except Exception:
            return False

    def init_widget(self):
        pass

    def get_data(self):
        pass

    def set_default_data(self, data):
        pass


class CustomDialogText(CustomDialogItem):
    def __init__(self, name, correct=None, default=None):
        super().__init__(name, QLineEdit, correct, default)

    def get_data(self):
        return self.widget.text()

    def set_default_data(self, data):
        if data is None:
            return
        self.widget.setText(data)


class CustomDialogList(CustomDialogItem):
    def __init__(self, name, list, correct=None, default=None):
        super().__init__(name, QComboBox, correct, default)
        self.list = list

    def get_data(self):
        return self.widget.currentText()

    def init_widget(self):
        self.widget.addItems(self.list)

    def set_default_data(self, data):
        if data is None:
            return
        self.widget.setCurrentText(data)


class CustomDialog(QDialog):
    def __init__(self, parent, *items: CustomDialogItem, window_title='Dialog'):
        super().__init__(parent, Qt.WindowCloseButtonHint)
        self.setWindowTitle(window_title)

        self.succeed = False
        indent = 20
        label_indent = 70
        bottom_indent = 50
        right_indent = 70
        items_dist = 35
        widget_width = 200
        widget_height = 20

        self.setGeometry(500, 500, indent * 2 + widget_width + label_indent + right_indent,
                         len(items) * items_dist + indent + bottom_indent)
        self.setFixedSize(self.width(), self.height())

        self.items = items
        for j, item in enumerate(items):
            item._set_widget(self)
            QLabel(item.name, self).setGeometry(indent, indent + items_dist * j,
                                                label_indent, widget_height)
            item.widget.setGeometry(indent + label_indent, indent + items_dist * j,
                                    widget_width, widget_height)

        self.cancelButton = QPushButton('Cancel', self)
        self.cancelButton.move(self.width() - indent - 70,
                               self.height() - indent - 25)
        self.cancelButton.clicked.connect(self.canceled)

        self.pushButton = QPushButton('Ok', self)
        self.pushButton.move(self.width() - indent - 150,
                             self.height() - indent - 25)
        self.pushButton.clicked.connect(self.clicked)

        self.info = QLabel('', self)
        self.info.setGeometry(indent, self.height() - indent - 25,
                              self.width() // 2, 25)
        self.info.setStyleSheet('color: red')

    def clicked(self):
        for i in self.items:
            if i.correct():
                ...
            else:
                QMessageBox.information(self, 'Incorrect data',
                                        f'Incorrect data in \'{i.name}\'')
                # self.info.setText(f'Incorrect data in \'{i.name}\'')
                break
        else:
            self.succeed = True
            self.close()

    def canceled(self):
        self.close()

    def result(self) -> list:
        self.exec()
        if self.succeed:
            return [i.get_data() for i in self.items]
        return False
