import openpyxl
from openpyxl.styles import Font, Alignment
from datetime import datetime, timedelta
import calendar
import pathlib

from loader import db

def create_excel(period: str) -> str:
    # Список данных
    data_list: list = [] 
    start_date: str = ''
    end_date: str = '' 

    if period == 'all':
        data_list = db.get_report_list_for_excel_all()
        start_date = data_list[0][0] if data_list else 'Нет данных'
        end_date = data_list[-1][0] if data_list else 'excel пустой'
    elif period == '7':
        today = datetime.today()
        current_weekday = today.weekday()
        start_date = (today - timedelta(days=current_weekday)).strftime('%d.%m.%Y')
        end_date = today.strftime('%d.%m.%Y')
        data_list = db.get_report_list_for_excel_period(start_date=start_date, 
                                                 end_date=end_date)
    elif period == '30':
        today = datetime.today()
        days_on_month = calendar.monthrange(today.year, today.month)[-1]
        start_date = today.replace(day=1).strftime('%d.%m.%Y')
        end_date = today.replace(day=days_on_month).strftime('%d.%m.%Y')
        data_list = db.get_report_list_for_excel_period(start_date=start_date, 
                                                 end_date=end_date)
    # Создаем новую книгу Excel и выбираем активный лист
    wb = openpyxl.Workbook()
    ws = wb.active

    # Задаем шрифт и выравнивание для заголовков
    title_font = Font(bold=True)
    alignment = Alignment(horizontal='center')

    # Заголовки для столбцов
    headers = [
        "ДАТА", "ИМЯ", "ОБР ЗАПРОСЫ", "ВЫСТ СЧЕТА",
        "ОПЛ СЧЕТА", "МАРЖА", "ВЫРУЧКА", "КОНВ ЗАПР В СЧЁТ",
        "КОНВ СЧЕТ В ОПЛ", "ПРОЦЕНТ НАЦЕНКИ"
    ]

    # Устанавливаем заголовки и форматирование
    for col_num, header in enumerate(headers, 1):
        cell = ws.cell(row=1, column=col_num, value=header)
        cell.font = title_font
        cell.alignment = alignment

    # Заполняем данные
    for row_num, row_data in enumerate(data_list, 2):
        for col_num, value in enumerate(row_data, 1):
            cell = ws.cell(row=row_num, column=col_num, value='-' if None else value)
            # Выравнивание по центру для всех ячеек
            cell.alignment = alignment

    folder = 'folder_to_reports'
    path_root = pathlib.Path(folder).parent.resolve()
    file = f'{path_root}/{folder}/Отчет {start_date} - {end_date}.xlsx'
    # Сохраняем Excel-файл
    wb.save(filename=file)
    return file
