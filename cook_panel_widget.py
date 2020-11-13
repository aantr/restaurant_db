import sqlite3
from PyQt5 import uic
from PyQt5.QtCore import QDateTime, QTime
from PyQt5.QtGui import QColor
from PyQt5.QtWidgets import QListWidgetItem

from base_window import BaseWindow
from table_data import OrderData, OrderDishData
from utils import date_time_format, time_format
from PyQt5.QtCore import QTimer


class CookPanelWidget(BaseWindow):
    def __init__(self, app):
        super().__init__(app)

        self.con = sqlite3.connect(self.app.DB_FILENAME)
        self.cur = self.con.cursor()

        self.init_ui()

    def init_ui(self):
        uic.loadUi('UI/cook_panel.ui', self)
        super().init_ui()

        self.w1 = OrderDishData(None, self.cur)

        self.timer = QTimer()
        self.timer.timeout.connect(self.update_list)
        self.timer.start(1000)
        self.update_list()

        self.btn_back.clicked.connect(self.app.pop)

    def update_list(self):
        que = self.w1.update()
        rows = self.cur.execute(que).fetchmany(self.count_rows_spin.value())
        self.list_order.clear()
        self.list_order_2.clear()
        for i in rows:
            dish_time_s = self.cur.execute(f'''select cooktime from dish 
                                                    where id = (select dishid from orderdish
                                                    where id = ({i[0]}))''').fetchone()[0]
            date_time_s = self.cur.execute(f'''select datetime from orderclient
                                              where id = {i[1]}''').fetchone()[0]
            dish_count = int(i[4])
            date_time = QDateTime.fromString(date_time_s, date_time_format())
            dish_time = QTime.fromString(dish_time_s, time_format())
            dish_time_minutes = dish_time.hour() * 60 + dish_time.minute() * dish_count
            dish_time = QTime(dish_time_minutes // 60, dish_time_minutes % 60)

            secs_passed = date_time.secsTo(QDateTime.currentDateTime())
            hms = [dish_time.hour() - secs_passed // 3600,
                   dish_time.minute() - secs_passed // 60 % 60,
                   59 - secs_passed % 60]
            time_last = QTime(*hms)
            if time_last.isValid():
                order = [time_last.toString(time_format() + ':ss'), *i[2:]]
            else:
                order = ['Done', *i[2:]]
            item = QListWidgetItem(' - '.join(map(str, order)))
            if not time_last.isValid():
                item.setBackground(QColor(255, 220, 220))
                self.list_order_2.addItem(item)
            else:
                self.list_order.addItem(item)
