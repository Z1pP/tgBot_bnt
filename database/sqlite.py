import sqlite3
from reports.report import Report


class DataBase:
    def __init__(self, db_name: str = 'test.db') -> None:
        self._db_name = db_name
        self._connection = self.create_connection()
        self._cursor = self._connection.cursor()

    def create_connection(self):
        try:
            conn = sqlite3.connect(self._db_name)
        except sqlite3.Error as e:
            print(e)
        return conn

    def create_tables_or_get_exists(self):
        self._cursor.execute("""CREATE TABLE IF NOT EXISTS reports 
                        (id INTEGER PRIMARY KEY AUTOINCREMENT,date TEXT, name TEXT,tg_id TEXT,
                        orders INTEGER, invoices INTEGER, paid_invoices INTEGER, margine REAL, 
                        revenue REAL, conversion REAL, conversion_paid REAL, 
                        markup_percentage REAL)""")

        self._cursor.execute("""CREATE TABLE IF NOT EXISTS managers 
                        (id TEXT PRIMARY KEY, nickname TEXT, name TEXT, role TEXT)""")
        self._connection.commit()

    def get_managers(self) -> list:
        self._cursor.execute("""SELECT * FROM managers""")
        return self._cursor.fetchall()

    def add_report_to_db(self, report: Report):
        try:
            self._cursor.execute("""INSERT INTO reports (date, name, tg_id, orders, invoices, paid_invoices, margine,
                                      revenue, conversion, conversion_paid, markup_percentage)
                  VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)""",
                                 (report.date, report.manager, report.id, report.orders, report.invoices,
                                  report.paid_invoices, report.margin, report.revenue, round(report.conversion, 2),
                                  round(report.conversion_paid, 2), round(report.markup_percentage, 2)))

            self._connection.commit()

        except sqlite3.OperationalError as e:
            raise e

    def add_managers_to_db(self, id, name, tg_name, role):
        self._cursor.execute(f"""INSERT INTO managers (id,nickname, name, role) 
                        VALUES ('{id}','{tg_name}',
                                '{name}', '{role}')""")
        self._connection.commit()

    def get_manager_to_id(self, id: str) -> list:
        self._cursor.execute(f"""SELECT * FROM managers WHERE id == {id}""")
        return self._cursor.fetchall()

    def get_report_list(self) -> list:
        self._cursor.execute("""SELECT * FROM reports""")
        return self._cursor.fetchall()

    def get_report_list_for_excel_period(self, start_date:str, end_date: str) -> list:
        self._cursor.execute("""
                            SELECT date, name, orders, invoices, paid_invoices, margine,
                            revenue, conversion, conversion_paid, markup_percentage FROM reports
                            WHERE date BETWEEN ? AND ?""", (start_date, end_date))
        return self._cursor.fetchall()

    def get_report_list_for_excel_all(self) -> list:
        self._cursor.execute("""
                            SELECT date, name, orders, invoices, paid_invoices, margine,
                            revenue, conversion, conversion_paid, markup_percentage FROM reports
                             """)
        return self._cursor.fetchall()
    
    def get_report_list_by_date(self, date: str) -> list:
        self._cursor.execute(f"""SELECT * FROM reports WHERE date == '{date}'""")
        return self._cursor.fetchall()

    def get_reports_date(self):
        self._cursor.execute("""SELECT DISTINCT date FROM reports""")
        return self._cursor.fetchall()

    def change_manager_role(self, id, current_role: str) -> str:
        if current_role == 'SuperManager':
            self._cursor.execute(f"""UPDATE managers SET role = 'Manager' WHERE id == '{id}'""")
            self._connection.commit()
            return 'Manager'

        self._cursor.execute(f"""UPDATE managers SET role = 'SuperManager' WHERE id == '{id}'""")
        self._connection.commit()
        return 'SuperManager'

    def change_manager_name(self, new_name, id):
        try:
            self._cursor.execute(f"""UPDATE managers SET name = '{new_name}' WHERE id == '{id}'""")
            self._connection.commit()
        except sqlite3.OperationalError as e:
            raise e

    def delete_report_from_db(self, id):
        self._cursor.execute(f"""DELETE FROM reports WHERE id == {id}""")
        self._connection.commit()

    def delete_manager_from_db(self, id):
        self._cursor.execute(f"""DELETE FROM managers WHERE id == {id}""")
        self._connection.commit()