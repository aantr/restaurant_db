from custom_dialog import CustomDialogText, CustomDialogList
import sqlite3


class TableData:
    def __init__(self, widget, cur: sqlite3.Cursor):
        self.widget = widget
        self.cur = cur

    def update(self):
        pass

    def delete(self, rows):
        pass

    def edit(self, res):
        pass

    def add(self, res):
        pass

    def dialog_items(self, row):
        pass


class BaseRestaurantTableData(TableData):
    def __init__(self, widget, cur: sqlite3.Cursor):
        super().__init__(widget, cur)

    def update(self):
        return f'select * from {self.table_name}'

    def delete(self, rows):
        ids = list(map(lambda x: x[0], rows))
        return f'''delete from {self.table_name} where id in ({','.join(ids)})'''

    def edit(self, res):  # res: [id, field1, field2]
        self.cur.execute(f'select * from {self.table_name}')
        col_names = list(map(lambda x: x[0], self.cur.description))
        return f'''update {self.table_name} set
                {', '.join([f'{name.lower()} = "{res[i + 1]}"'
                            for i, name in enumerate(col_names[1:])])}
                where id = "{res[0]}"'''

    def add(self, res):  # res: [field1, field2]
        self.cur.execute(f'select * from {self.table_name}')
        col_names = list(map(lambda x: x[0], self.cur.description))
        return f'''insert into {self.table_name}({', '.join(col_names[1:])})
                                     values({', '.join([f'"{i}"' for i in res])})'''


class IngredientData(BaseRestaurantTableData):
    table_name = 'ingredient'

    def __init__(self, widget, cur: sqlite3.Cursor):
        super().__init__(widget, cur)

    def dialog_items(self, row=None):
        if row is None:
            row = [None] * 3
        items = (CustomDialogText('Title', lambda x: x != '', row[1]),
                 CustomDialogText('Price', lambda x: int(x) > 0, row[2]))
        return items


class DishData(BaseRestaurantTableData):
    table_name = 'dish'

    def __init__(self, widget, cur: sqlite3.Cursor):
        super().__init__(widget, cur)

    def dialog_items(self, row=None):
        if row is None:
            row = [None] * 3
        print(row)
        items = (CustomDialogText('Title', lambda x: x != '', row[1]),
                 CustomDialogText('Price', lambda x: int(x) > 0, row[2]),
                 CustomDialogList('Type', map(lambda x: x[0], self.cur.execute('''
                 select title from dishtype''').fetchall()),
                                  default=row[3]))
        return items
