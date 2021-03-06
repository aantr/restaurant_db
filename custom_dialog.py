from PyQt5.QtCore import Qt, QDateTime, QTime
from PyQt5.QtWidgets import QWidget, QLineEdit, QComboBox, QDialog, \
    QPushButton, QLabel, QMessageBox, QDateTimeEdit, QTimeEdit

from utils import date_time_format, time_format


class CustomDialogItem:
    def __init__(self, name, widget_type, correct=None, enabled=True, default=None):
        self.name = name
        self.widget_type = widget_type
        self.widget: QWidget = None
        self.default = default
        self.enabled = enabled

        # Function that define correct input data
        self.correct_func = correct if correct is not None else lambda x: True

    def _set_widget(self, parent):
        """Setup input widget"""
        self.widget = self.widget_type(parent)
        self.widget.setDisabled(not self.enabled)
        self.init_widget()
        self.set_default_data(self.default)

    def correct(self):
        """Calls correct_func and returns if data correct"""
        try:
            return self.correct_func(self.get_data())
        except ValueError as e:
            return False

    def init_widget(self):
        """Init widget"""
        pass

    def get_data(self):
        """Get input data from widget"""
        pass

    def set_default_data(self, data):
        """Set default input data into widget"""
        pass


class CustomDialogText(CustomDialogItem):
    def __init__(self, name, correct=None, enabled=True, default=None):
        super().__init__(name, QLineEdit, correct, enabled, default)

    def get_data(self):
        return self.widget.text().strip()

    def set_default_data(self, data):
        if data is None:
            return
        self.widget.setText(data.strip())


class CustomDialogList(CustomDialogItem):
    def __init__(self, name, items_list, match=None, correct=None,
                 reversed_sort=False, enabled=True, default=None):
        super().__init__(name, QComboBox, correct, enabled, default)
        self.reversed_sort = reversed_sort
        self.list = list(map(str, items_list))
        self.match = match

    def get_data(self):
        if self.match is not None:
            return self.match[self.list.index(self.widget.currentText())]
        return self.widget.currentText()

    def init_widget(self):
        all_int = all(map(str.isdigit, self.list))
        self.widget.addItems(sorted(self.list, key=lambda x: int(x) if all_int else x,
                                    reverse=self.reversed_sort))

    def set_default_data(self, data):
        if data is None:
            return
        self.widget.setCurrentText(data)


class CustomDialogDateTime(CustomDialogItem):
    def __init__(self, name, correct=None, enabled=True, default=None):
        super().__init__(name, QDateTimeEdit, correct, enabled, default)
        self.format = date_time_format()

    def init_widget(self):
        self.widget.setDateTime(QDateTime.currentDateTime())
        self.widget.setDisplayFormat(self.format)

    def get_data(self):
        self.widget: QDateTimeEdit
        return self.widget.dateTime().toString(self.format)

    def set_default_data(self, data):
        if data is None:
            return
        self.widget: QDateTimeEdit
        self.widget.setDateTime(QDateTime.fromString(data, self.format))


class CustomDialogTime(CustomDialogItem):
    def __init__(self, name, correct=None, enabled=True, default=None):
        super().__init__(name, QTimeEdit, correct, enabled, default)
        self.format = time_format()

    def init_widget(self):
        self.widget.setTime(QTime.currentTime())
        self.widget.setDisplayFormat(self.format)

    def get_data(self):
        self.widget: QTimeEdit
        return self.widget.time().toString(self.format)

    def set_default_data(self, data):
        if data is None:
            return
        self.widget: QTimeEdit
        self.widget.setTime(QTime.fromString(data, self.format))


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

        self.resize(indent * 2 + widget_width + label_indent + right_indent,
                    len(items) * items_dist + indent + bottom_indent)
        self.setFixedSize(self.width(), self.height())

        # Widgets
        self.items = items
        for j, item in enumerate(items):
            item._set_widget(self)
            QLabel(item.name, self).setGeometry(
                indent, indent + items_dist * j, label_indent, widget_height)
            item.widget.setGeometry(
                indent + label_indent, indent + items_dist * j,
                widget_width, widget_height)

        # Buttons
        self.pushButton = QPushButton('Ok', self)
        self.pushButton.move(self.width() - indent - 150,
                             self.height() - indent - 25)
        self.pushButton.clicked.connect(self.clicked)

        self.cancelButton = QPushButton('Cancel', self)
        self.cancelButton.move(self.width() - indent - 70,
                               self.height() - indent - 25)
        self.cancelButton.clicked.connect(self.canceled)

        self.info = QLabel('', self)
        self.info.setGeometry(indent, self.height() - indent - 25,
                              self.width() // 2, 25)
        self.info.setStyleSheet('color: red')

    def clicked(self):
        for i in self.items:
            if i.correct():
                ...
            else:  # Incorrect data
                QMessageBox.information(self, 'Information',
                                        f'Incorrect data in \'{i.name}\'')
                break
        else:  # Correct data
            self.succeed = True
            self.close()

    def canceled(self):
        self.close()

    def result(self) -> list:
        """Returns list of input data in widgets if data correct else False"""
        self.exec()
        if self.succeed:
            return [i.get_data() for i in self.items]
        return False
