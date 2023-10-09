from reports.report import Report


class Manager:
    def __init__(self, 
                name: str = 'default', 
                nickname:str = 'default',
                id: str = '000000') -> None:
        self._name = name
        self._nickname = nickname
        self._id = id
        self._role = 'Manager'

    def set_name(self, name: str):
        self._name = name

    def set_id(self, id: str):
        self._id = id

    @property
    def nickname(self) -> str:
        return self._nickname

    @property
    def name(self) -> str:
        return self._name
    
    @property
    def id(self) -> str:
        return self._id
    
    @property
    def role(self) -> str:
        return self._role

    def create_report(self, data: dict) -> Report:
        try:
            self._report = Report(**data)
            return self._report
        except Exception as e:
            raise Exception(f"Ошибка при создании отчета: {str(e)}")


class SuperManager(Manager):
    def __init__(self, name: str, nickname:str, id: str) -> None:
        super().__init__(name, nickname, id)
        self._role = 'SuperManager'

 
    @staticmethod
    def report_list_to_dict(report_from_db: list) -> dict:
        return {
            'Дата создания': report_from_db[1],
            'Имя': report_from_db[2],
            'Заказов обработано': report_from_db[4],
            'Счетов выставлено': report_from_db[5],
            'Счетов оплачено': report_from_db[6],
            'Маржа': report_from_db[7],
            'Выручка': report_from_db[8],
            'Конверсия': report_from_db[9],
            'Конверсия счета в оплату': report_from_db[10],
            'Процент наценки': report_from_db[11]
        }
