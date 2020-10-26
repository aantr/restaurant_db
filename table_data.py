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
    table_name = None

    def __init__(self, widget, cur: sqlite3.Cursor):
        super().__init__(widget, cur)
        self.exclude_cols = 1
        self.replace_cols = {}

    def update(self):
        self.cur.execute(f'select * from {self.table_name}')
        col_names = list(map(lambda x: x[0], self.cur.description))
        que = f'''select {', '.join([f'{self.table_name}.{i.lower()}'
                                     for i in col_names])} from {self.table_name}'''
        for k, v in self.replace_cols.items():
            old_col, new_col, table, table_col, replace_col = map(str.lower, [k] + list(v))
            que = que.replace(f'{self.table_name}.{old_col}',
                              f'{table}.{table_col} as {new_col}')
            que += f''' left join {table} on {table}.{replace_col} = 
                    {self.table_name}.{old_col}'''
        return que

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
        que = f'''insert into {self.table_name}({', '.join(col_names[self.exclude_cols:])})
                                     values({', '.join([f'"{i}"' for i in res])})'''
        print(que)
        return que

    def dialog_items(self, row):  # row: [id, field1, field2]
        pass

    def generate_dialog(self, items_conditions, row=None):
        exclude_cols = self.exclude_cols
        self.cur.execute(f'select * from {self.table_name}')
        col_names = list(map(lambda x: x[0], self.cur.description))[exclude_cols:]
        if row is None:
            row = [None] * len(col_names)
        else:
            row = row[exclude_cols:]
        if len(items_conditions) != len(col_names) or len(row) != len(col_names):
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


class IngredientData(BaseRestaurantTableData):
    table_name = 'ingredient'

    def __init__(self, widget, cur: sqlite3.Cursor):
        super().__init__(widget, cur)

    def update(self, replace=()):
        return super().update()

    def dialog_items(self, row=None):
        items = self.generate_dialog(
            [(CustomDialogText, lambda x: x != ''),
             (CustomDialogText, lambda x: int(x) > 0)],
            row=row)
        return items


class DishData(BaseRestaurantTableData):
    table_name = 'dish'

    def __init__(self, widget, cur: sqlite3.Cursor):
        super().__init__(widget, cur)
        self.replace_cols = {'typeid': ('type', 'dishtype', 'title', 'id')}

    def update(self, replace=()):
        return super().update()

    def dialog_items(self, row=None):
        items = self.generate_dialog(
            [(CustomDialogText, lambda x: x != ''),
             (CustomDialogText, lambda x: int(x) > 0),
             (CustomDialogList, ('dishtype', 'title'), ('dishtype', 'id'), None)],
            row=row)
        return items


class DishTypeData(BaseRestaurantTableData):
    table_name = 'dishtype'

    def __init__(self, widget, cur: sqlite3.Cursor):
        super().__init__(widget, cur)

    def update(self, replace=()):
        return super().update()

    def dialog_items(self, row=None):
        items = self.generate_dialog(
            [(CustomDialogText, lambda x: x != '')],
            row=row)
        return items


class DishIngredientData(BaseRestaurantTableData):
    table_name = 'dishingredient'

    def __init__(self, widget, cur: sqlite3.Cursor):
        super().__init__(widget, cur)
        self.replace_cols = {'dishid': ('dish', 'dish', 'title', 'id'),
                             'ingredientid': ('ingredient', 'ingredient', 'title', 'id')}

    def update(self):
        return super().update()

    def dialog_items(self, row=None):
        items = self.generate_dialog(
            [(CustomDialogList, ('dish', 'title'), ('dish', 'id'), None),
             (CustomDialogList, ('ingredient', 'title'), ('ingredient', 'id'), None),
             (CustomDialogText, lambda x: float(x) > 0)],
            row=row)
        return items
