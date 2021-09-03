import xlrd


def is_empty_row(row: list):
    for cl in row:
        if cl != '':
            return False

    return True


def is_load_file(func):
    """Проверят загружен ли файл"""

    def wrapper(self, *args, **kwargs):
        if self.xls:
            return func(self, *args, **kwargs)
        else:
            raise Exception("Не загружен файл")
    return wrapper


def clear_row(row: list) -> list:
    new_row = []
    for cl in row:
        if cl != '':
            if isinstance(cl, str):
                new_row.append(cl.strip())
            else:
                new_row.append(cl)
    return new_row


class BaseSupplier:

    name = ""
    id = None

    def __init__(self, filename):
        self.filename = filename
        self.xls = self._load_file(self.filename)

    def __str__(self):
        return f"{self.filename} - Страниц({len(self.xls.sheets())})" if self.xls else super().__str__()

    def _load_file(self, file_name: str) -> xlrd.book.Book:
        """
        Загружает файл по пути
        :param file_name: Путь к файлу
        :return: Объект xlrd
        """
        try:
            return xlrd.open_workbook(file_name)
        except Exception as e:
            raise Exception(str(e))

    def _get_rows(self,sheet_index=0, start_flags=['№', 'Кол-во', 'Цена'], end_flags=['Итого:'], is_empty_last_row=False) -> list:
        """
        Возвращает список строк самой таблицы с товарами
        :param sheet_index: Номер страницы где таблица (по дефолту 0)
        :param start_flags: Флаги для того, чтобы найти заголовок таблицы
        :param end_flags: Флаги для того, чтобы найти конец таблицы
        :param is_empty_last_row: Если строка после таблицы пустая
        :return:
        """
        rows = []
        sheet = self.xls.sheet_by_index(sheet_index)
        start_index = None
        end_index = None
        for rownum in range(sheet.nrows):
            row = sheet.row_values(rownum)
            if set(start_flags).issubset(row):
                start_index = rownum
            if not is_empty_last_row:
                if set(end_flags).issubset(row):
                    end_index = rownum

        if is_empty_last_row:
            row = sheet.row_values(start_index)
            while not is_empty_row(row):
                rows.append(row)
                start_index += 1
                row = sheet.row_values(start_index)
        else:
            if start_flags and end_index:
                for rownum in range(start_index, end_index):
                    rows.append(sheet.row_values(rownum))
            else:
                return None
        return rows

    @is_load_file
    def parse_file(self):
        """
        Парсит таблицу с товарами
        :return: Возвращает словарь, где ключ id товара в заказе
        name: Название товара
        quantity: Количество
        price: Цена за 1 Ед.
        """
        raise Exception("Не удалось получить данные")


class SupplierFactory:

    @staticmethod
    def get_class(name=None, id=None):
        if name:
            for _class in BaseSupplier.__subclasses__():
                if _class.name == name:
                    return _class

        if id:
            for _class in BaseSupplier.__subclasses__():
                if _class.id == id:
                    return _class

        return None


class SupplierVodoleiTreid(BaseSupplier):
    name = "Водолей-Трейд"
    id = 1

    @is_load_file
    def parse_file(self) -> dict:
        rows = self._get_rows(is_empty_last_row=True)
        data = {}
        for row in rows[1:]:
            row = clear_row(row)
            data[row[1]] = {'name': row[2], 'quantity': row[3], 'price': row[5]}

        return data

class SupplierGrotiK(BaseSupplier):
    name = "Грот и К"
    id = 2

    @is_load_file
    def parse_file(self):
        rows = self._get_rows()
        data = {}
        for row in rows[1:]:
            row = clear_row(row)
            data[row[0]] = {'name': row[1], 'quantity': row[2], 'price': row[5]}

        return data


class SupplierAviator(BaseSupplier):
    name = "Авиатор"
    id = 3

    @is_load_file
    def parse_file(self):
        rows = self._get_rows(is_empty_last_row=True)
        data = {}
        for row in rows[1:]:
            row = clear_row(row)
            data[row[0]] = {'name': row[1], 'quantity': row[2], 'price': row[4]}

        return data


class SupplierStroyComplect(BaseSupplier):
    name = "Стройкомплект"
    id = 4

    @is_load_file
    def parse_file(self):
        # TODO: Fix bug with encoding
        pass
        # rows = self._get_rows(is_empty_last_row=True)
        # data = {}
        # for row in rows[1:]:
        #     row = clear_row(row)
        #     data[row[0]] = {'name': row[1], 'quantity': row[2], 'price': row[4]}
        #
        # return data


# Supplier = SupplierFactory.get_class(id=1)
# supplier = Supplier('test_data.xls')
# Supplier = SupplierFactory.get_class(id=2)
# supplier = Supplier('test_data_2.xls')
# Supplier = SupplierFactory.get_class(id=3)
# supplier = Supplier('test_data_3.xls')
# Supplier = SupplierFactory.get_class(id=4)
# supplier = Supplier('test_data_4.xls')
# Supplier = SupplierFactory.get_class(name="Авиатор")
# supplier = Supplier('test_data_5.xls')
# print(supplier.parse_file())