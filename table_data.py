from PyQt5.QtCore import QTime

from custom_dialog import CustomDialogText, CustomDialogList, \
    CustomDialogDateTime, CustomDialogTime
import sqlite3

from utils import time_format


class TableData:
    """Used for working with table in database
    that class use CustomDialog for input data"""

    def __init__(self, widget, cur: sqlite3.Cursor):
        self.widget = widget
        self.cur = cur

    def update(self):
        """Returns str sqlite request for update table"""
        pass

    def delete(self, rows):
        """Returns str sqlite request for delete rows in table"""
        pass

    def edit(self, res):
        """Returns str sqlite request for edit rows in table"""
        pass

    def add(self, res):
        """Returns str sqlite request for add row in table"""
        pass

    def dialog_items(self, row):
        """Returns list of CustomDialogItem"""
        pass


class BaseTableData(TableData):
    """Use table name to work with table"""
    table_name = None

    def __init__(self, widget, cur: sqlite3.Cursor):
        super().__init__(widget, cur)

        # Don`t use the column "Id"
        self.exclude_cols = 1

        # Replace real column names and data for better displaying
        self.replace_cols = {}

        # Tables which use this table
        self.usage = []

    def update(self):
        self.cur.execute(f'select * from {self.table_name}')
        col_names = list(map(lambda x: x[0], self.cur.description))

        que = f'''select {', '.join([f'{self.table_name}.{i.lower()}'
                                     for i in col_names])} from ({self.table_name}'''
        for k, v in self.replace_cols.items():
            old_col, new_col, table, table_col, repl_col = map(str.lower, [k] + list(v))
            que = que.replace(f'{self.table_name}.{old_col}',
                              f'{table}.{table_col} as {new_col}')
            que += f''' left join {table} on {table}.{repl_col} = 
                    {self.table_name}.{old_col}'''
        que += ')'
        return que

    def check_usage(self, rows):  # row: [id, field1, field2]
        ids = list(map(lambda x: str(x[0]), rows))
        for i in self.usage:
            usage_ids = list(map(lambda x: str(x[0]), self.cur.execute(f'''
                            select {i[1]} from {i[0]}''').fetchall()))
            for id in ids:
                if id in usage_ids:
                    return True
        return False

    def delete(self, rows):  # row: [id, field1, field2]
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
        que = f'''insert into {self.table_name}
                ({', '.join(col_names[self.exclude_cols:])})
                values({', '.join([f'"{i}"' for i in res])})'''
        return que

    def dialog_items(self, row):  # row: [id, field1, field2]
        pass

    def generate_dialog_items(self, items_conditions, row=None):
        """Returns list of CustomDialogItem"""
        exclude_cols = self.exclude_cols
        self.cur.execute(f'select * from {self.table_name}')
        col_names = list(map(lambda x: x[0], self.cur.description))[exclude_cols:]
        if row is None:
            row = [None] * len(col_names)
        else:
            row = row[exclude_cols:]
        if len(items_conditions) != len(col_names) or \
                len(row) != len(col_names):
            raise IndexError('Length does not match length of items')
        items = []
        for i, j in enumerate(items_conditions):
            new_j = []  # replace tuples with SQL select columns
            for elem in j:
                if type(elem) == tuple:
                    new_j.append(list(map(lambda x: x[0], self.cur.execute(f'''
        select {elem[1]} from {elem[0]}''').fetchall())))
                else:
                    new_j.append(elem)
            j = new_j
            label = col_names[i].lower()
            if label in self.replace_cols:
                label = self.replace_cols[label][0]
            items.append(j[0](label.capitalize(), *j[1:],
                              default=row[i]))
        return items


class IngredientData(BaseTableData):
    table_name = 'ingredient'

    def __init__(self, widget, cur: sqlite3.Cursor):
        super().__init__(widget, cur)
        self.replace_cols = {'unitid': ('unit', 'unit', 'title', 'id')}
        self.usage = [('dishingredient', 'ingredientid')]

    def update(self, replace=()):
        que = super().update()
        que += f' order by {self.table_name}.title'
        return que

    def dialog_items(self, row=None):
        items = self.generate_dialog_items(
            [(CustomDialogText, lambda x: x),
             (CustomDialogText, lambda x: float(x) > 0),
             (CustomDialogList, ('unit', 'title'), ('unit', 'id'), None)],
            row=row)
        return items


class DishData(BaseTableData):
    table_name = 'dish'

    def __init__(self, widget, cur: sqlite3.Cursor):
        super().__init__(widget, cur)
        self.replace_cols = {'typeid': ('type', 'dishtype', 'title', 'id')}
        self.usage = [('orderdish', 'dishid'),
                      ('dishingredient', 'dishid')]

    def update(self, replace=()):
        return super().update()

    def dialog_items(self, row=None):
        items = self.generate_dialog_items(
            [(CustomDialogText, lambda x: x),
             (CustomDialogText, lambda x: float(x) > 0),
             (CustomDialogList, ('dishtype', 'title'), ('dishtype', 'id'), None),
             (CustomDialogTime, None)],
            row=row)
        return items


class DishTypeData(BaseTableData):
    table_name = 'dishtype'

    def __init__(self, widget, cur: sqlite3.Cursor):
        super().__init__(widget, cur)
        self.usage = [('dish', 'typeid')]

    def update(self, replace=()):
        return super().update()

    def dialog_items(self, row=None):
        items = self.generate_dialog_items(
            [(CustomDialogText, lambda x: x)],
            row=row)
        return items


class DishIngredientData(BaseTableData):
    table_name = 'dishingredient'

    def __init__(self, widget, cur: sqlite3.Cursor):
        super().__init__(widget, cur)
        self.replace_cols = {'dishid': ('dish', 'dish', 'title', 'id'),
                             'ingredientid': ('ingredient', 'ingredient', 'title', 'id')}

    def update(self):
        return super().update()

    def dialog_items(self, row=None):
        items = self.generate_dialog_items(
            [(CustomDialogList, ('dish', 'title'), ('dish', 'id'), None),
             (CustomDialogList, ('ingredient', 'title'), ('ingredient', 'id'), None),
             (CustomDialogText, lambda x: float(x) > 0)],
            row=row)
        return items


class CookData(BaseTableData):
    table_name = 'cook'

    def __init__(self, widget, cur: sqlite3.Cursor):
        super().__init__(widget, cur)
        self.usage = [('orderdish', 'cookid')]

    def update(self):
        que = super().update()
        que += f' order by {self.table_name}.name'
        return que

    def dialog_items(self, row=None):
        items = self.generate_dialog_items(
            [(CustomDialogText, lambda x: x),
             (CustomDialogText, lambda x: int(x) >= 0)],
            row=row)
        return items


class WaiterData(BaseTableData):
    table_name = 'waiter'

    def __init__(self, widget, cur: sqlite3.Cursor):
        super().__init__(widget, cur)
        self.usage = [('order', 'waiterid')]

    def update(self):
        que = super().update()
        que += f' order by {self.table_name}.name'
        return que

    def dialog_items(self, row=None):
        items = self.generate_dialog_items(
            [(CustomDialogText, lambda x: x)],
            row=row)
        return items


class OrderData(BaseTableData):
    table_name = 'orderclient'

    def __init__(self, widget, cur: sqlite3.Cursor):
        super().__init__(widget, cur)
        self.replace_cols = {'waiterid': ('waiter', 'waiter', 'name', 'id')}
        self.usage = [('orderdish', 'orderid')]

    def update(self):
        que = super().update()
        que += f' order by datetime desc'
        return que

    def dialog_items(self, row=None):
        items = self.generate_dialog_items(
            [(CustomDialogList, ('waiter', 'name'), ('waiter', 'id'), None),
             (CustomDialogDateTime, None)],
            row=row)
        return items


class OrderDishData(BaseTableData):
    table_name = 'orderdish'

    def __init__(self, widget, cur: sqlite3.Cursor):
        super().__init__(widget, cur)
        self.replace_cols = {'orderid': ('orderclient', 'orderclient', 'id', 'id'),
                             'cookid': ('cook', 'cook', 'name', 'id'),
                             'dishid': ('dish', 'dish', 'title', 'id')}

    def update(self):
        que = super().update()
        que += f' order by orderclient.datetime desc, orderdish.id desc'
        return que

    def add(self, res):
        # Add WorkMinute
        dishcookminte = self.cur.execute(f'select cooktime from dish where id = '
                                         f'{res[2]}').fetchone()[0]
        dishcookminte = QTime.fromString(dishcookminte, time_format())
        dishcookminte = dishcookminte.hour() * 60 + dishcookminte.minute() * int(res[3])
        self.cur.execute(f'''update cook set
                        workminute = workminute + {dishcookminte}
                        where id = {res[1]}''')
        return super().add(res)

    def dialog_items(self, row=None):
        if row is None:
            # Auto fill Cook on Add
            row = [None] * 5  # Count field with id
            cook = self.cur.execute('''select name from cook where workminute=
                                    (select min(workminute) from cook)''').fetchone()[0]

            row[2] = cook  # Set default value for cook

            items = self.generate_dialog_items(
                [(CustomDialogList, ('orderclient', 'id'), ('orderclient', 'id'),
                  None, True, False),  # Select orderclient id by date reverse and disable choice
                 (CustomDialogList, ('cook', 'name'), ('cook', 'id'),
                  None, False, False),  # Disable choice
                 (CustomDialogList, ('dish', 'title'), ('dish', 'id'), None),
                 (CustomDialogText, lambda x: int(x) > 0)],
                row=row)
        else:
            # Default on Edit
            items = self.generate_dialog_items(
                [(CustomDialogList, ('orderclient', 'id'), ('orderclient', 'id'), None, True),
                 (CustomDialogList, ('cook', 'name'), ('cook', 'id'), None),
                 (CustomDialogList, ('dish', 'title'), ('dish', 'id'), None),
                 (CustomDialogText, lambda x: int(x) > 0)],
                row=row)
        return items


class UnitData(BaseTableData):
    table_name = 'unit'

    def __init__(self, widget, cur: sqlite3.Cursor):
        super().__init__(widget, cur)
        self.usage = [('ingredient', 'unitid')]

    def update(self):
        return super().update()

    def dialog_items(self, row=None):
        items = self.generate_dialog_items(
            [(CustomDialogText, None)],
            row=row)
        return items
